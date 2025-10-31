import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';
import BoundingBoxes from './components/BoundingBoxes';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setImagePreview(URL.createObjectURL(file));
    setResults(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await axios.post('/api/assess-damage', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'An error occurred while analyzing the image. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>🚗 Vehicle Damage Assessment</h1>
          <p>AI-Powered Damage Detection & Analysis</p>
        </div>
      </header>

      <main className="App-main">
        <div className="container">
          {!imagePreview ? (
            <ImageUpload onImageSelect={handleImageSelect} />
          ) : (
            <div className="analysis-section">
              <div className="image-preview-section">
                <h2>Selected Image</h2>
                <div className="image-preview-container">
                  {results?.bboxes?.length ? (
                    <BoundingBoxes imageSrc={imagePreview} bboxes={results.bboxes} />
                  ) : (
                    (() => {
                      const displayedImage = results?.annotated_image_base64
                        ? `data:image/png;base64,${results.annotated_image_base64}`
                        : imagePreview;
                      return (
                        <img
                          src={displayedImage}
                          alt={results?.annotated_image_base64 ? 'Annotated vehicle' : 'Selected vehicle'}
                          className="preview-image"
                        />
                      );
                    })()
                  )}
                </div>
                <div className="action-buttons">
                  <button 
                    onClick={handleAnalyze} 
                    disabled={loading}
                    className="btn btn-primary"
                  >
                    {loading ? 'Analyzing...' : '🔍 Analyze Damage'}
                  </button>
                  <button 
                    onClick={handleReset}
                    disabled={loading}
                    className="btn btn-secondary"
                  >
                    🔄 Upload New Image
                  </button>
                </div>
              </div>

              {loading && <LoadingSpinner />}

              {error && (
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  <p>{error}</p>
                </div>
              )}

              {results && !loading && (
                <ResultsDisplay results={results} />
              )}
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Powered by Google Gemini AI | Built with React & FastAPI</p>
      </footer>
    </div>
  );
}

export default App;
