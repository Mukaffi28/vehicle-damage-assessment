import os
import json
import google.generativeai as genai
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageOps
import io
import base64


class GeminiService:
    """Service for interacting with Google Gemini API for vehicle damage assessment"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini service
        
        Args:
            api_key: Google API key for Gemini. If None, reads from GEMINI_API_KEY env variable
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided or set as environment variable")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro') 
        
        # System instruction for damage assessment
        self.system_instruction = """You are an expert vehicle damage assessor working for an insurance company. Analyze the image of the vehicle and detect any type of damage. 
        Only use the following predefined damage categories:

Broken Glass, Broken Lights, Scratch, Dent, Crack, Punctured Tyre, Lost Parts, Torn, Non-Damaged

Provide output strictly in the following JSON format:

{
  "damage_detected": "Yes/No",
  "damage_type": ["one or more of the listed categories"],
  "damage_location": "specific car part (e.g., front bumper, rear door, windshield) or 'Not Applicable' if no damage",
  "severity": "None / Low / Medium / High" (use 'None' if no damage detected),
  "description": "short factual explanation based on visible evidence"
}"""

        self.image_prompt = """Analyze this vehicle image for damage. Return only JSON.

For bounding boxes, use NORMALIZED coordinates (0.0 to 1.0):
- x: left edge as fraction of image width (0.0 = left, 1.0 = right)
- y: top edge as fraction of image height (0.0 = top, 1.0 = bottom)  
- width: box width as fraction of image width
- height: box height as fraction of image height

Example: damage in center would be around x=0.4, y=0.4, width=0.2, height=0.2

{
  "damage_detected": "Yes/No",
  "damage_type": ["Broken Glass/Broken Lights/Scratch/Dent/Crack/Punctured Tyre/Lost Parts/Torn/Non-Damaged"],
  "damage_location": "specific car part or Not Applicable",
  "severity": "None/Low/Medium/High",
  "description": "brief description",
  "bboxes": [{"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}],
  "image_width": 0,
  "image_height": 0
}"""

    async def assess_damage(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Assess vehicle damage from an image
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            Dictionary containing damage assessment results
        """
        try:
            # Load image (apply EXIF orientation to match browser display)
            image = Image.open(io.BytesIO(image_bytes))
            image = ImageOps.exif_transpose(image)
            width, height = image.size
            
            # Generate content with Gemini
            prompt_text = (
                self.image_prompt
                + f"\n\nImageSize: width={width}, height={height} (pixels)"
            )
            response = self.model.generate_content([
                prompt_text,
                image
            ])
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            bboxes = result.get("bboxes", []) if isinstance(result, dict) else []
            valid_boxes = []
            try:
                for b in bboxes or []:
                    # Raw values may be normalized (0..1) or pixels. Detect and convert.
                    rx = b.get("x", 0)
                    ry = b.get("y", 0)
                    rw = b.get("width", 0)
                    rh = b.get("height", 0)

                    # If all values within [0,1.1], treat as normalized and scale to pixels
                    def _is_norm(v):
                        try:
                            fv = float(v)
                            return 0 <= fv <= 1.1
                        except Exception:
                            return False

                    if all(_is_norm(v) for v in (rx, ry, rw, rh)):
                        fx = float(rx) * width
                        fy = float(ry) * height
                        fw = float(rw) * width
                        fh = float(rh) * height
                    else:
                        fx, fy, fw, fh = rx, ry, rw, rh

                    x = max(0, int(round(float(fx))))
                    y = max(0, int(round(float(fy))))
                    w = max(0, int(round(float(fw))))
                    h = max(0, int(round(float(fh))))
                    if w <= 0 or h <= 0:
                        continue
                    if x >= width or y >= height:
                        continue
                    w = min(w, width - x)
                    h = min(h, height - y)
                    valid_boxes.append({"x": x, "y": y, "width": w, "height": h})
            except Exception:
                valid_boxes = []
            if isinstance(result, dict):
                result["bboxes"] = valid_boxes
                result["image_width"] = width
                result["image_height"] = height

            if valid_boxes:
                draw = ImageDraw.Draw(image)
                for b in valid_boxes:
                    x, y, w, h = b["x"], b["y"], b["width"], b["height"]
                    draw.rectangle([x, y, x + w, y + h], outline="red", width=4)
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                annotated_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                result["annotated_image_base64"] = annotated_b64
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during damage assessment: {str(e)}")
