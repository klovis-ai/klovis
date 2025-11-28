import json
from klovis.base import BaseMetadataGenerator
from klovis.models import Chunk
from klovis.utils import get_logger

logger = get_logger(__name__)


class EnrichedChunksGenerator(BaseMetadataGenerator):
    """
    Generates ONE enriched markdown chunk for each document.

    Sections supported:
      - title
      - summary
      - topics
      - faq
      - keywords
      - numerical_insights (NEW)

    Everything is produced in ONE LLM call returning RAW MARKDOWN.

    Args:
        llm_client: LLM client instance
        enabled: List of sections to enable (default: all sections)
        summary_sentences: Number of sentences in summary (default: 5)
        topics_count: Number of topics to extract (default: 8)
        faq_count: Number of FAQ pairs (default: 4)
        keywords_count: Number of keywords (default: 10)
        numerical_items: Number of numerical insights (default: 10)
        max_output_chars: Maximum output characters (default: None)
        lang: Language code for generated content (default: "en")
    """

    def __init__(
        self,
        llm_client,
        enabled=None,
        summary_sentences: int = 5,
        topics_count: int = 8,
        faq_count: int = 4,
        keywords_count: int = 10,
        numerical_items: int = 10,
        max_output_chars: int | None = None,
        lang: str = "en",
    ):
        self.llm = llm_client
        self.enabled = enabled or [
            "title",
            "summary",
            "topics",
            "faq",
            "keywords",
            "numerical_insights",
        ]

        self.summary_sentences = summary_sentences
        self.topics_count = topics_count
        self.faq_count = faq_count
        self.keywords_count = keywords_count
        self.numerical_items = numerical_items
        self.max_output_chars = max_output_chars
        self.lang = lang

        logger.debug(
            "EnrichedChunksGenerator initialized with: "
            f"enabled={self.enabled}, "
            f"summary_sentences={summary_sentences}, "
            f"topics_count={topics_count}, "
            f"faq_count={faq_count}, "
            f"keywords_count={keywords_count}, "
            f"numerical_items={numerical_items}, "
            f"max_output_chars={max_output_chars}, "
            f"lang={lang}"
        )

    # ---------------------------------------------------------------------

    def generate(self, document):
        logger.debug(f"Generating enriched chunk for document: {document.source}")

        # ---------- Build dynamic instructions ----------
        instruction_lines = []

        if "title" in self.enabled:
            instruction_lines.append("- Generate a markdown H1 title (# ...).")

        if "summary" in self.enabled:
            instruction_lines.append(
                f"- Write a {self.summary_sentences}-sentence markdown summary."
            )

        if "topics" in self.enabled:
            instruction_lines.append(
                f"- List {self.topics_count} main topics as bullet points."
            )

        if "faq" in self.enabled:
            instruction_lines.append(
                f"- Write {self.faq_count} FAQ entries in markdown (### Question / Answer...)."
            )

        if "keywords" in self.enabled:
            instruction_lines.append(
                f"- Extract {self.keywords_count} important keywords (bullet list)."
            )

        if "numerical_insights" in self.enabled:
            instruction_lines.append(
                f"- Extract and list {self.numerical_items} important numerical insights "
                "(percentages, capacities, prices, durations, quantities, statistics)."
            )

        instructions_text = "\n".join(instruction_lines)

        # ---------- Prompt ----------
        lang_instruction = f"- Generate all content (title, summary, topics, FAQ, keywords, numerical insights) in {self.lang} language." if self.lang != "en" else ""
        
        prompt = f"""
You are a markdown generator.

TASK:
Produce a single well-formatted Markdown document containing the following sections:

{instructions_text}

DOCUMENT TEXT:
\"\"\"
{document.content}
\"\"\"

IMPORTANT:
- Return **ONLY raw markdown**, no JSON, no comments.
- Use clear, readable markdown headings.
- Do NOT invent data. Only include numbers explicitly present or derivable from the text.
- Ensure sections appear logically ordered.
{lang_instruction}
"""

        # ---------- LLM CALL ----------
        try:
            raw = self.llm.generate(prompt)
            if not raw:
                raise ValueError("LLM returned empty response.")

            final_markdown = raw.strip()

        except Exception as e:
            logger.error(
                f"EnrichedChunksGenerator failed for document {document.source}: {e}"
            )
            return []

        # ---------- Character constraint ----------
        if self.max_output_chars and len(final_markdown) > self.max_output_chars:
            final_markdown = final_markdown[: self.max_output_chars].rstrip()
            logger.warning(
                f"Enriched output truncated to {self.max_output_chars} characters."
            )

        # ---------- Build enriched chunk ----------
        enriched_chunk = Chunk(
            text=final_markdown,
            metadata={
                "type": "enriched_document",
                "source": document.source,
                "summary_sentences": self.summary_sentences,
                "topics_count": self.topics_count,
                "faq_count": self.faq_count,
                "keywords_count": self.keywords_count,
                "numerical_items": self.numerical_items,
                "lang": self.lang,
            },
        )

        logger.info(f"Enriched chunk generated for document {document.source}")

        return [enriched_chunk]
