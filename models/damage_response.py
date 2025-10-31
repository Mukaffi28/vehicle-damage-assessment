from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class BBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class DamageResponse(BaseModel):
    """Response model for vehicle damage assessment"""
    
    damage_detected: Literal["Yes", "No"] = Field(
        description="Whether damage was detected in the image"
    )
    damage_type: List[str] = Field(
        description="List of damage types detected from predefined categories"
    )
    damage_location: str = Field(
        description="Specific car part where damage is located"
    )
    severity: Literal["None", "Low", "Medium", "High"] = Field(
        description="Severity level of the damage (None if no damage detected)"
    )
    description: str = Field(
        description="Short factual explanation based on visible evidence"
    )
    bboxes: Optional[List[BBox]] = None
    annotated_image_base64: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "damage_detected": "Yes",
                "damage_type": ["Dent", "Scratch"],
                "damage_location": "front bumper",
                "severity": "Medium",
                "description": "Visible dent and scratches on the front bumper area"
            }
        }
