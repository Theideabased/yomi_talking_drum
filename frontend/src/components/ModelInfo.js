import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, Cpu, Target, TrendingUp } from 'lucide-react';
import './ModelInfo.css';

const API_URL = 'http://localhost:8000';

function ModelInfo() {
  const [modelInfo, setModelInfo] = useState(null);
  const [notesInfo, setNotesInfo] = useState(null);

  useEffect(() => {
    fetchModelInfo();
    fetchNotesInfo();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/model-info`);
      setModelInfo(response.data);
    } catch (err) {
      console.error('Error fetching model info:', err);
    }
  };

  const fetchNotesInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/notes`);
      setNotesInfo(response.data);
    } catch (err) {
      console.error('Error fetching notes info:', err);
    }
  };

  if (!modelInfo) {
    return <div className="loading">Loading model information...</div>;
  }

  return (
    <div className="model-info">
      <div className="info-section">
        <div className="section-header">
          <Cpu size={24} />
          <h2>Model Architecture</h2>
        </div>
        <div className="info-grid">
          <div className="info-card">
            <span className="info-label">Architecture</span>
            <span className="info-value">{modelInfo.architecture}</span>
          </div>
          <div className="info-card">
            <span className="info-label">Input Features</span>
            <span className="info-value">{modelInfo.input_features}</span>
          </div>
          <div className="info-card">
            <span className="info-label">Classes</span>
            <span className="info-value">{modelInfo.num_classes}</span>
          </div>
          <div className="info-card highlight">
            <span className="info-label">Accuracy</span>
            <span className="info-value">{modelInfo.accuracy}</span>
          </div>
        </div>
      </div>

      <div className="info-section">
        <div className="section-header">
          <Target size={24} />
          <h2>Feature Engineering</h2>
        </div>
        <div className="features-list">
          <div className="feature-item">
            <span className="feature-badge">26</span>
            <div className="feature-details">
              <strong>MFCC Features</strong>
              <p>13 coefficients + 13 standard deviations</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-badge">6</span>
            <div className="feature-details">
              <strong>Spectral Features</strong>
              <p>Centroid, rolloff, bandwidth (mean & std)</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-badge">12</span>
            <div className="feature-details">
              <strong>Chroma Features</strong>
              <p>12 pitch class features</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-badge">3</span>
            <div className="feature-details">
              <strong>Temporal & Time Domain</strong>
              <p>Onset rate, RMS energy, zero-crossing rate</p>
            </div>
          </div>
        </div>
      </div>

      <div className="info-section">
        <div className="section-header">
          <Database size={24} />
          <h2>Dataset Information</h2>
        </div>
        <div className="dataset-stats">
          <div className="stat-card">
            <span className="stat-value">1,050</span>
            <span className="stat-label">Total Samples</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">150</span>
            <span className="stat-label">Per Class</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">100%</span>
            <span className="stat-label">Balance</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">22,050 Hz</span>
            <span className="stat-label">Sample Rate</span>
          </div>
        </div>
      </div>

      {notesInfo && (
        <div className="info-section">
          <div className="section-header">
            <TrendingUp size={24} />
            <h2>Tonic Solfa Notes</h2>
          </div>
          <div className="notes-grid">
            {notesInfo.notes.map((note) => {
              const info = notesInfo.cultural_info[note];
              return (
                <div key={note} className="note-card">
                  <div className="note-header">
                    <span className="note-icon">🎵</span>
                    <span className="note-name">{note}</span>
                  </div>
                  <div className="note-details">
                    <p className="note-pitch">{info.pitch}</p>
                    <p className="note-frequency">{info.frequency}</p>
                    <p className="note-usage">{info.usage}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="info-section">
        <div className="section-header">
          <h2>🌍 Cultural Significance</h2>
        </div>
        <div className="cultural-text">
          <p>
            Talking drums (Dùndún) are traditional Yoruba instruments that mimic the tonal 
            patterns of the Yoruba language. They serve as communication tools for long-distance 
            messaging, musical instruments in ceremonies, and cultural preservation mediums.
          </p>
          <p>
            This AI system preserves this endangered cultural heritage through technology, 
            making it accessible to new generations while maintaining respect for traditional 
            knowledge systems.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ModelInfo;
