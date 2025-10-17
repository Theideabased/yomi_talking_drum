import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Award, Info } from 'lucide-react';
import './PredictionResult.css';

function PredictionResult({ prediction }) {
  if (!prediction) return null;

  const { predicted_note, confidence, all_confidences, cultural_info, audio_duration } = prediction;

  // Prepare data for chart
  const chartData = Object.entries(all_confidences).map(([note, conf]) => ({
    note,
    confidence: parseFloat(conf.toFixed(2)),
    fill: note === predicted_note ? '#FF6B35' : '#4ECDC4'
  }));

  const getConfidenceColor = (conf) => {
    if (conf >= 90) return 'high';
    if (conf >= 70) return 'medium';
    return 'low';
  };

  return (
    <div className="prediction-result">
      <div className="result-header">
        <Award size={32} className="award-icon" />
        <h2>Prediction Result</h2>
      </div>

      <div className="result-grid">
        {/* Main Prediction */}
        <div className="prediction-card main-prediction">
          <div className="note-badge">
            <span className="note-symbol">🎵</span>
            <span className="note-name">{predicted_note}</span>
          </div>
          <div className={`confidence-badge confidence-${getConfidenceColor(confidence)}`}>
            <span className="confidence-label">Confidence</span>
            <span className="confidence-value">{confidence.toFixed(2)}%</span>
          </div>
        </div>

        {/* Cultural Information */}
        <div className="prediction-card cultural-info">
          <div className="card-header">
            <Info size={20} />
            <h3>Cultural Context</h3>
          </div>
          <div className="info-item">
            <strong>Pitch:</strong>
            <span>{cultural_info.pitch}</span>
          </div>
          <div className="info-item">
            <strong>Frequency:</strong>
            <span>{cultural_info.frequency}</span>
          </div>
          <div className="info-item">
            <strong>Usage:</strong>
            <span>{cultural_info.usage}</span>
          </div>
          <div className="info-item">
            <strong>Cultural Significance:</strong>
            <span>{cultural_info.cultural}</span>
          </div>
        </div>
      </div>

      {/* Audio Info */}
      <div className="audio-info">
        <span>📊 Audio Duration: {audio_duration.toFixed(2)}s</span>
        <span>📈 Sample Rate: 22,050 Hz</span>
        <span>🎯 Features: 47 audio features</span>
      </div>

      {/* Confidence Chart */}
      <div className="chart-container">
        <h3>Confidence Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="note" />
            <YAxis label={{ value: 'Confidence (%)', angle: -90, position: 'insideLeft' }} />
            <Tooltip formatter={(value) => `${value}%`} />
            <Legend />
            <Bar dataKey="confidence" fill="#4ECDC4" name="Confidence" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Scores */}
      <div className="detailed-scores">
        <h3>Detailed Confidence Scores</h3>
        <div className="scores-grid">
          {Object.entries(all_confidences).map(([note, conf]) => (
            <div 
              key={note} 
              className={`score-item ${note === predicted_note ? 'predicted' : ''}`}
            >
              <span className="score-note">{note}</span>
              <div className="score-bar-container">
                <div 
                  className="score-bar" 
                  style={{ width: `${conf}%` }}
                ></div>
              </div>
              <span className="score-value">{conf.toFixed(2)}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default PredictionResult;
