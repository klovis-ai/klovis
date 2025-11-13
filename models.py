"""
Pydantic models defining the structure of Klovis data objects.
All models include utility methods for serialization and export.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
import json


class KlovisBaseModel(BaseModel):
    """
    Base model for all Klovis data objects.
    Provides common serialization utilities.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a standard Python dictionary representation of the object.
        Equivalent to `model_dump()` but adds a consistent interface.
        """
        return self.model_dump()

    def to_json(self, indent: int = 2) -> str:
        """
        Return a JSON string representation of the object.
        Parameters
        ----------
        indent : int, optional
            Number of spaces used for indentation (default: 2).
        """
        return json.dumps(self.model_dump(), indent=indent, ensure_ascii=False)

    class Config:
        """Global configuration for all models."""
        arbitrary_types_allowed = True
        validate_assignment = True
        extra = "forbid"
        frozen = False  # Could be True if you want immutability
        str_strip_whitespace = True


class Document(KlovisBaseModel):
    """Represents a raw or loaded document."""
    source: Any = Field(..., description="Document source path, URL, or identifier.")
    content: str = Field(..., description="Raw or loaded document content.")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata (e.g., chunk_id, length, tags, etc.)."
    )


class Chunk(KlovisBaseModel):
    """Represents a processed chunk of text."""
    text: str = Field(..., description="Chunk text content.")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
