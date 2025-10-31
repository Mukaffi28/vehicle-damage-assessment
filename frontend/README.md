# Vehicle Damage Assessment - Frontend

A modern React-based frontend for the Vehicle Damage Assessment API.

## Features

- 🎨 Beautiful, modern UI with gradient designs
- 📤 Drag & drop image upload
- 🖼️ Image preview before analysis
- 📊 Comprehensive results display with color-coded severity
- 📱 Fully responsive design
- ⚡ Fast and intuitive user experience

## Tech Stack

- React 18
- Axios for API calls
- CSS3 with animations
- Modern ES6+ JavaScript

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── ImageUpload.js       # Drag & drop upload component
│   │   ├── ImageUpload.css
│   │   ├── ResultsDisplay.js    # Results visualization
│   │   ├── ResultsDisplay.css
│   │   ├── LoadingSpinner.js    # Loading indicator
│   │   └── LoadingSpinner.css
│   ├── App.js                   # Main application component
│   ├── App.css
│   ├── index.js                 # Entry point
│   └── index.css
├── package.json
└── README.md
```

## Usage

1. **Upload Image**: Drag and drop a vehicle image or click to browse
2. **Analyze**: Click the "Analyze Damage" button
3. **View Results**: See detailed damage assessment including:
   - Damage detection status
   - Severity level (Low/Medium/High)
   - Damage types detected
   - Location of damage
   - Detailed description

## API Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000`. The proxy is configured in `package.json` to handle CORS during development.

### API Endpoint

- **POST** `/api/assess-damage` - Upload image for damage assessment

## Supported Image Formats

- JPEG/JPG
- PNG
- WebP

**Maximum file size**: 10MB

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

### Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (one-way operation)

## Customization

### Colors

Main gradient colors can be customized in the CSS files:
- Primary: `#667eea` to `#764ba2`
- Header: `#1e3c72` to `#2a5298`

### Severity Colors

- **Low**: Green (`#4caf50`)
- **Medium**: Orange (`#ff9800`)
- **High**: Red (`#f44336`)

## Troubleshooting

### "Proxy error" or CORS issues
- Ensure the backend is running on `http://localhost:8000`
- Check the proxy setting in `package.json`

### Images not uploading
- Check file size (must be < 10MB)
- Verify file format (JPEG, PNG, or WebP only)
- Ensure backend API is running

## License

This project is provided as-is for educational and commercial use.
