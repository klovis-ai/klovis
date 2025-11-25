"""
Pydantic models defining the structure of Klovis data objects.
All models include utility methods for serialization and export.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional, Dict, List
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


class Relationship(BaseModel):
    """Represents a relationship to another entity or chunk (for GraphRAG)."""
    target_id: str = Field(..., description="ID of the target chunk or entity.")
    type: str = Field(..., description="Type of relationship (e.g. 'next', 'parent', 'relates_to').")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class Chunk(KlovisBaseModel):
    """
    Represents a processed chunk of text ready for RAG.
    Includes support for vector embeddings and graph relationships.
    """
    text: str = Field(..., description="Chunk text content.")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Advanced RAG fields
    vector: Optional[List[float]] = Field(
        default=None, 
        description="Vector embedding of the chunk text."
    )
    parent_id: Optional[str] = Field(
        default=None, 
        description="ID of the parent document or parent chunk (for hierarchical RAG)."
    )
    relationships: List[Relationship] = Field(
        default_factory=list,
        description="List of relationships to other chunks (for GraphRAG)."
    )
