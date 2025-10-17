import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileAudio, X } from 'lucide-react';
import './FileUpload.css';

function FileUpload({ onFileSelect, loading, disabled }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setSelectedFile(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.wav', '.mp3', '.m4a', '.aac']
    },
    multiple: false,
    disabled: disabled || loading
  });

  const handleAnalyze = () => {
    if (selectedFile && onFileSelect) {
      onFileSelect(selectedFile);
    }
  };

  const handleClear = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
  };

  return (
    <div className="file-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />
        
        {!selectedFile ? (
          <div className="dropzone-content">
            <Upload size={64} className="upload-icon" />
            <h3>Drop your audio file here</h3>
            <p>or click to browse</p>
            <div className="supported-formats">
              <span>Supported: WAV, MP3, M4A, AAC</span>
            </div>
          </div>
        ) : (
          <div className="selected-file">
            <FileAudio size={48} className="file-icon" />
            <div className="file-info">
              <h4>{selectedFile.name}</h4>
              <p>{(selectedFile.size / 1024).toFixed(2)} KB</p>
            </div>
            <button
              className="clear-button"
              onClick={handleClear}
              disabled={loading}
            >
              <X size={20} />
            </button>
          </div>
        )}
      </div>

      {selectedFile && (
        <button
          className={`analyze-button ${loading ? 'loading' : ''}`}
          onClick={handleAnalyze}
          disabled={loading || disabled}
        >
          {loading ? (
            <>
              <div className="spinner"></div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              🎯 Predict Note
            </>
          )}
        </button>
      )}
    </div>
  );
}

export default FileUpload;
