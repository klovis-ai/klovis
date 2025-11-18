import json
from klovis.base import BaseMetadataGenerator
from klovis.utils import get_logger

logger = get_logger(__name__)


class LLMMetadataGenerator(BaseMetadataGenerator):
    """
    Generates all metadata types in a SINGLE LLM CALL.
    """

    def __init__(
        self,
        llm_client,
        enabled=None,
        max_questions=5,
        max_topics=5,
        max_summary_sentences=3,
        max_title_length=80,
    ):
        self.llm = llm_client
        self.enabled = enabled or ["faq", "summary", "topics", "title", "entities"]
        self.max_q = max_questions
        self.max_topics = max_topics
        self.max_summary_sentences = max_summary_sentences
        self.max_title_length = max_title_length

        logger.info(f"LLMMetadataGenerator enabled for: {self.enabled}")

    def generate(self, chunk):
        cid = chunk.metadata.get("chunk_id")
        logger.debug(f"LLMMetadataGenerator: processing chunk {cid}")

        # Build prompt dynamically
        request_parts = []

        if "faq" in self.enabled:
            request_parts.append(f"- FAQ (3 to {self.max_q} Q&A pairs)")
        if "summary" in self.enabled:
            request_parts.append(f"- Summary ({self.max_summary_sentences} sentences max)")
        if "title" in self.enabled:
            request_parts.append(f"- Title ({self.max_title_length} chars max)")
        if "topics" in self.enabled:
            request_parts.append(f"- Topics ({self.max_topics} max)")
        if "entities" in self.enabled:
            request_parts.append("- Entities (persons, organizations, locations, dates, numbers, products)")

        prompt = f"""
You are an expert assistant. Extract the following metadata from the text:

{chr(10).join(request_parts)}

TEXT:
\"\"\"
{chunk.text}
\"\"\"

Return ONLY a JSON object with the keys you were asked for.
"""

        try:
            response = self.llm.generate(prompt)
            text = response.strip()

            data = json.loads(text)  # strict JSON

            logger.info(f"LLM metadata generated for chunk {cid}")
            return data

        except json.JSONDecodeError:
            logger.error(
                f"LLMMetadataGenerator: Invalid JSON for chunk {cid}"
            )
            return {}

        except Exception as e:
            logger.error(f"LLMMetadataGenerator failed for chunk {cid}: {e}")
            return {}
