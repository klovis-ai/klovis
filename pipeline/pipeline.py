from typing import List, Optional, Any
from pathlib import Path
from datetime import datetime
import json
import pandas as pd

from klovis.config import settings
from klovis.exceptions import KlovisError, MissingAPIKeyError, ProcessingError
from klovis.models import Document, Chunk
from klovis.utils import get_logger

logger = get_logger(__name__)


class KlovisPipeline:
    """
    Orchestrates a preprocessing workflow using Pydantic models,
    and optionally exports final results to multiple formats.
    """

    def __init__(
        self,
        loader: Optional[Any] = None,
        extractor: Optional[Any] = None,
        cleaner: Optional[Any] = None,
        chunker: Optional[Any] = None,
        metadata_generator: Optional[Any] = None,
        require_api_key: bool = True,
        export_results: bool = False,
        export_dir: str = "outputs",
        export_format: str = "json",  # 👈 JSON, CSV, or PARQUET
    ):
        self.loader = loader
        self.extractor = extractor
        self.cleaner = cleaner
        self.chunker = chunker
        self.metadata_generator = metadata_generator
        self.require_api_key = require_api_key
        self.export_results = export_results
        self.export_dir = Path(export_dir)
        self.export_format = export_format.lower()

        if self.require_api_key and not settings.has_api_key():
            raise MissingAPIKeyError("Klovis API key is missing or invalid.")

        # Ensure export directory exists
        if self.export_results:
            self.export_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"KlovisPipeline initialized (export_format={self.export_format.upper()}).")

    def run(self, sources: List[Any]) -> List[Chunk]:
        """
        Execute the pipeline sequentially with type-safe data flow.
        Optionally exports the final results as JSON, CSV, or Parquet.
        """
        try:
            data: List[Document] | List[Chunk] = sources
            start_time = datetime.now()
            logger.info("=== Starting KlovisPipeline Execution ===")

            if self.loader:
                logger.info("[1/5] Running loader...")
                data = self.loader.load(data)

            if self.extractor:
                logger.info("[2/5] Running extractor...")
                data = self.extractor.extract(data)

            if self.cleaner:
                logger.info("[3/5] Running cleaner...")
                data = self.cleaner.clean(data)

            if self.chunker:
                logger.info("[4/5] Running chunker...")
                data = self.chunker.chunk(data)

            if self.metadata_generator:
                logger.info("[5/5] Running metadata generator...")
                data = self.metadata_generator.generate(data)

            logger.info("Pipeline execution completed successfully.")

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Total processing time: {duration:.2f} seconds")

            if self.export_results:
                self._export_results(data)

            return data

        except KlovisError:
            logger.exception("Klovis-specific error occurred during pipeline execution.")
            raise
        except Exception as e:
            logger.exception("Unexpected error in pipeline.")
            raise ProcessingError(f"Pipeline execution failed: {e}") from e

    def _export_results(self, data: List[Chunk]) -> None:
        """Export final pipeline results to the chosen format in the export directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"klovis_output_{timestamp}"

        try:
            json_data = [chunk.to_dict() for chunk in data]

            # Select export format
            if self.export_format == "json":
                path = self.export_dir / f"{filename}.json"
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                logger.info(f"Exported results to {path}")

            elif self.export_format == "csv":
                path = self.export_dir / f"{filename}.csv"
                df = pd.DataFrame(json_data)
                df.to_csv(path, index=False)
                logger.info(f"Exported results to {path}")

            elif self.export_format in ("parquet", "pq"):
                path = self.export_dir / f"{filename}.parquet"
                df = pd.DataFrame(json_data)
                df.to_parquet(path, index=False, engine="pyarrow")
                logger.info(f"Exported results to {path}")

            else:
                logger.warning(f"Unsupported export format '{self.export_format}', defaulting to JSON.")
                fallback = self.export_dir / f"{filename}.json"
                with open(fallback, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                logger.info(f"Exported results to {fallback}")

        except Exception as e:
            logger.error(f"Failed to export results: {e}")
