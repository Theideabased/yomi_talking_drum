import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import FileUpload from './components/FileUpload';
import PredictionResult from './components/PredictionResult';
import ModelInfo from './components/ModelInfo';
import ErrorBoundary from './components/ErrorBoundary';
import './components/ErrorBoundary.css';
import { Music, AlertCircle, CheckCircle } from 'lucide-react';

// API URL configuration
const API_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : null);

function App() {
  const [modelStatus, setModelStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');
  const [audioFile, setAudioFile] = useState(null);

  // Check API health on mount
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    if (!API_URL) {
      setModelStatus({ 
        status: 'offline', 
        model_loaded: false, 
        message: 'Backend API not configured. This is a frontend-only demo.' 
      });
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/health`);
      setModelStatus(response.data);
    } catch (err) {
      setModelStatus({ 
        status: 'offline', 
        model_loaded: false, 
        message: 'Cannot connect to API. Backend may be offline.' 
      });
    }
  };

  const handleFileUpload = async (file) => {
    if (!API_URL) {
      setError('Backend API not available. This is a frontend-only demo.');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);
    setAudioFile(file); // Store the audio file

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error processing audio file');
      setAudioFile(null); // Clear audio file on error
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <Music size={48} className="logo-icon" />
            <div>
              <h1>Yoruba Talking Drum Translator</h1>
              <p className="subtitle">AI-Powered Tonic Solfa Recognition</p>
            </div>
          </div>
          
          <div className="status-badge">
            {modelStatus?.model_loaded ? (
              <span className="status-online">
                <CheckCircle size={20} />
                <span>Model Ready</span>
              </span>
            ) : (
              <span className="status-offline">
                <AlertCircle size={20} />
                <span>Model Not Loaded</span>
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          {/* Tabs */}
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
              onClick={() => setActiveTab('upload')}
            >
              📁 Upload Audio
            </button>
            <button
              className={`tab ${activeTab === 'info' ? 'active' : ''}`}
              onClick={() => setActiveTab('info')}
            >
              📚 Model Info
            </button>
          </div>

          {/* Tab Content */}
          <div className="tab-content">
            {activeTab === 'upload' && (
              <div className="upload-section">
                {!modelStatus?.model_loaded && (
                  <div className="alert alert-warning">
                    <AlertCircle size={24} />
                    <div>
                      <strong>Model Not Loaded</strong>
                      <p>Please export your trained model first. See documentation for instructions.</p>
                    </div>
                  </div>
                )}

                <FileUpload
                  onFileSelect={handleFileUpload}
                  loading={loading}
                  disabled={!modelStatus?.model_loaded}
                />

                {error && (
                  <div className="alert alert-error">
                    <AlertCircle size={24} />
                    <div>
                      <strong>Error</strong>
                      <p>{error}</p>
                    </div>
                  </div>
                )}

                {prediction && <PredictionResult prediction={prediction} audioFile={audioFile} />}
              </div>
            )}

            {activeTab === 'info' && <ModelInfo />}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Yoruba Talking Drum Translator • Powered by AI • 100% Accuracy Model</p>
        <p>Built with FastAPI + React.js</p>
      </footer>
    </div>
  );
}

function AppWithErrorBoundary() {
  return (
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  );
}

export default AppWithErrorBoundary;
