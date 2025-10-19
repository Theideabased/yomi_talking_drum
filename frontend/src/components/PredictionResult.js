import React, { useState, useEffect, useRef } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Award, Info, Play, Pause, Volume2 } from 'lucide-react';
import './PredictionResult.css';

function PredictionResult({ prediction, audioFile }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);
  const [audioUrl, setAudioUrl] = useState(null);

  useEffect(() => {
    // Create a URL for the audio file
    if (audioFile) {
      const url = URL.createObjectURL(audioFile);
      setAudioUrl(url);
      
      // Cleanup function to revoke the URL when component unmounts
      return () => {
        URL.revokeObjectURL(url);
      };
    }
  }, [audioFile]);

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const handleSeek = (e) => {
    const seekTime = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = seekTime;
      setCurrentTime(seekTime);
    }
  };

  const formatTime = (time) => {
    if (isNaN(time)) return '0:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

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

      {/* Audio Player */}
      {audioUrl && (
        <div className="audio-player-container">
          <div className="audio-player">
            <audio
              ref={audioRef}
              src={audioUrl}
              onTimeUpdate={handleTimeUpdate}
              onLoadedMetadata={handleLoadedMetadata}
              onEnded={handleEnded}
            />
            
            <div className="audio-controls">
              <button 
                className="play-button" 
                onClick={togglePlayPause}
                aria-label={isPlaying ? 'Pause' : 'Play'}
              >
                {isPlaying ? <Pause size={24} /> : <Play size={24} />}
              </button>
              
              <div className="audio-progress">
                <span className="time-label">{formatTime(currentTime)}</span>
                <input
                  type="range"
                  min="0"
                  max={duration || 0}
                  value={currentTime}
                  onChange={handleSeek}
                  className="progress-slider"
                />
                <span className="time-label">{formatTime(duration)}</span>
              </div>
              
              <div className="volume-icon">
                <Volume2 size={20} />
              </div>
            </div>
            
            <div className="audio-info-badge">
              <span>🎵 Playing: {audioFile?.name || 'Audio File'}</span>
            </div>
          </div>
        </div>
      )}

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
