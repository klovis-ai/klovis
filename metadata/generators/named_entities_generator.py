from klovis.base import BaseMetadataGenerator
from klovis.utils import get_logger

logger = get_logger(__name__)


class NamedEntitiesGenerator(BaseMetadataGenerator):
    """
    Extracts named entities using a user-provided NLP model.
    
    The NLP model must implement:
        extract_entities(text: str) -> dict
    """

    def __init__(self, nlp_model):
        """
        Parameters
        ----------
        nlp_model : object
            Any object implementing `.extract_entities(text: str) -> dict`
        """
        self.model = nlp_model
        logger.debug("NamedEntitiesGenerator initialized with custom NLP model.")

    def generate(self, chunk):
        cid = chunk.metadata.get("chunk_id")
        logger.debug(f"Generating entities for chunk {cid}...")

        try:
            entities = self.model.extract_entities(chunk.text)

            # Minimal validation
            if not isinstance(entities, dict):
                logger.warning(f"NamedEntitiesGenerator: invalid result format for chunk {cid}")
                return {}

            logger.info(f"NamedEntitiesGenerator: extracted entities for chunk {cid}")
            return {"entities": entities}

        except Exception as e:
            logger.error(f"NamedEntitiesGenerator failed for chunk {cid}: {e}")
            return {}
