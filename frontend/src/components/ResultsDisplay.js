import React from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ results }) {
  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'none':
        return '#9e9e9e';
      case 'low':
        return '#4caf50';
      case 'medium':
        return '#ff9800';
      case 'high':
        return '#f44336';
      default:
        return '#757575';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity.toLowerCase()) {
      case 'none':
        return '✅';
      case 'low':
        return '✓';
      case 'medium':
        return '⚠️';
      case 'high':
        return '⚠️';
      default:
        return 'ℹ️';
    }
  };

  const getDamageIcon = (damageType) => {
    const iconMap = {
      'broken glass': '🔨',
      'broken lights': '💡',
      'scratch': '〰️',
      'dent': '⚫',
      'crack': '⚡',
      'punctured tyre': '🛞',
      'lost parts': '🔧',
      'torn': '✂️',
      'non-damaged': '✅'
    };
    
    return iconMap[damageType.toLowerCase()] || '🔍';
  };

  return (
    <div className="results-container">
      <h2>Analysis Results</h2>
      
      <div className="results-grid">
        {/* Damage Detection Status */}
        <div className={`result-card status-card ${results.damage_detected === 'Yes' ? 'damage-yes' : 'damage-no'}`}>
          <div className="card-header">
            <span className="card-icon">{results.damage_detected === 'Yes' ? '⚠️' : '✅'}</span>
            <h3>Damage Status</h3>
          </div>
          <div className="card-content">
            <p className="status-text">{results.damage_detected === 'Yes' ? 'Damage Detected' : 'No Damage Detected'}</p>
          </div>
        </div>

        {/* Severity */}
        <div className="result-card severity-card">
          <div className="card-header">
            <span className="card-icon">{getSeverityIcon(results.severity)}</span>
            <h3>Severity Level</h3>
          </div>
          <div className="card-content">
            <div 
              className="severity-badge"
              style={{ backgroundColor: getSeverityColor(results.severity) }}
            >
              {results.severity}
            </div>
          </div>
        </div>

        {/* Damage Types */}
        <div className="result-card damage-types-card">
          <div className="card-header">
            <span className="card-icon">🔍</span>
            <h3>Damage Type(s)</h3>
          </div>
          <div className="card-content">
            <div className="damage-types-list">
              {results.damage_type.map((type, index) => (
                <span key={index} className="damage-type-badge">
                  <span className="damage-type-icon">{getDamageIcon(type)}</span>
                  {type}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Location */}
        <div className="result-card location-card">
          <div className="card-header">
            <span className="card-icon">📍</span>
            <h3>Damage Location</h3>
          </div>
          <div className="card-content">
            <p className="location-text">{results.damage_location}</p>
          </div>
        </div>

        {/* Description */}
        <div className="result-card description-card full-width">
          <div className="card-header">
            <span className="card-icon">📝</span>
            <h3>Detailed Description</h3>
          </div>
          <div className="card-content">
            <p className="description-text">{results.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsDisplay;
