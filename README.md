# Vehicle Damage Assessment API

A FastAPI-based backend service that uses Google Gemini 2.5 Flash to detect and assess vehicle damage from uploaded images.

## Features

- 🚗 Automated vehicle damage detection
- 🤖 Powered by Google Gemini 2.5 Flash AI
- 📊 Categorizes damage into predefined types
- 📍 Identifies damage location on the vehicle
- ⚠️ Assesses damage severity (Low/Medium/High)
- 🔒 Secure file upload with validation
- 📝 Comprehensive API documentation

## Damage Categories

The API can detect the following types of damage:

- Broken Glass
- Broken Lights
- Scratch
- Dent
- Crack
- Punctured Tyre
- Lost Parts
- Torn
- Non-Damaged

## Project Structure

```
Car Dents/
├── main.py                 # FastAPI application entry point
├── models/
│   ├── __init__.py
│   └── damage_response.py  # Pydantic response models
├── services/
│   ├── __init__.py
│   └── gemini_service.py   # Gemini API integration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### 2. Installation

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

```bash
# Start the server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns API information and available endpoints.

### 2. Health Check
```
GET /health
```
Returns server health status and Gemini API configuration status.

### 3. Assess Damage
```
POST /api/assess-damage
```

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Supported Image Formats:**
- JPEG/JPG
- PNG
- WebP
- HEIC/HEIF

**File Size Limit:** 10MB

**Response:**
```json
{
  "damage_detected": "Yes",
  "damage_type": ["Dent", "Scratch"],
  "damage_location": "front bumper",
  "severity": "Medium",
  "description": "Visible dent and scratches on the front bumper area"
}
```

## Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/assess-damage" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/car-image.jpg"
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/assess-damage"
files = {"file": open("car-image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/assess-damage', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly.

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid file type or size)
- `500` - Internal Server Error (API configuration or processing errors)

Error responses include detailed messages:

```json
{
  "detail": "Error description here"
}
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `PORT` | Server port | No | 8000 |

## Security Considerations

- **API Key:** Never commit your `.env` file. Keep your Gemini API key secure.
- **CORS:** In production, configure specific allowed origins instead of `["*"]`
- **File Upload:** The API validates file types and sizes to prevent abuse
- **Rate Limiting:** Consider adding rate limiting for production use

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload on code changes.

### Testing

You can test the API using the built-in Swagger UI at `/docs` or use tools like:
- Postman
- Insomnia
- cURL
- Python requests

## Troubleshooting

### "GEMINI_API_KEY must be provided"
- Ensure you've created a `.env` file with your API key
- Verify the API key is valid

### "Invalid file type"
- Only image files are accepted (JPEG, PNG, WebP, HEIC/HEIF)
- Check the file extension and MIME type

### "File size exceeds 10MB limit"
- Compress or resize the image before uploading

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please check:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
