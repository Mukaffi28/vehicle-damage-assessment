import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p className="loading-text">Analyzing vehicle damage...</p>
      <p className="loading-subtext">This may take a few moments</p>
    </div>
  );
}

export default LoadingSpinner;
