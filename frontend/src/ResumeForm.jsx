import { useState, useRef } from 'react';
import { submitResume } from './api';

const MAX_FILES = 20;

export default function ResumeForm({ jobDescriptionId, onSubmitted }) {
  const [files, setFiles] = useState([]);
  const [fileError, setFileError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);

  const addFiles = (fileList) => {
    const incoming = Array.from(fileList);
    const valid = incoming.filter((f) => /\.(pdf|docx)$/i.test(f.name));
    const rejectedType = incoming.length - valid.length;

    setFiles((prev) => {
      const room = Math.max(MAX_FILES - prev.length, 0);
      const accepted = valid.slice(0, room);
      const rejectedLimit = valid.length - accepted.length;

      if (rejectedType > 0 && rejectedLimit > 0) {
        setFileError(`${rejectedType} file(s) skipped (PDF/DOCX only) and ${rejectedLimit} skipped (${MAX_FILES} file limit reached).`);
      } else if (rejectedType > 0) {
        setFileError(`${rejectedType} file(s) skipped — only PDF or DOCX is supported.`);
      } else if (rejectedLimit > 0) {
        setFileError(`${rejectedLimit} file(s) skipped — ${MAX_FILES} file limit reached.`);
      } else {
        setFileError('');
      }

      return [...prev, ...accepted];
    });
  };

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
    setFileError('');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    addFiles(e.dataTransfer.files);
  };

  const handleSubmitAll = async () => {
    if (!jobDescriptionId) {
      alert('Select a job description first');
      return;
    }
    if (files.length === 0) return;

    setSubmitting(true);
    for (const file of files) {
      const candidateName = file.name.replace(/\.(pdf|docx)$/i, '');
      try {
        const res = await submitResume(jobDescriptionId, candidateName, file);
        onSubmitted(res.data);
      } catch (err) {
        console.error('Failed to submit resume:', err);
      }
    }
    setFiles([]);
    setSubmitting(false);
  };

  return (
    <div className="panel">
      <h3>Submit resumes</h3>

      <div
        className={`dropzone ${isDragging ? 'dropzone-active' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <div className="dropzone-text">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          <div>
            <strong>Drop resumes here, or browse</strong>
            <p>PDF or DOCX, up to {MAX_FILES} files</p>
          </div>
        </div>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => inputRef.current.click()}
        >
          Browse files
        </button>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          multiple
          hidden
          onChange={(e) => addFiles(e.target.files)}
        />
      </div>

      {fileError && <p className="error-text">{fileError}</p>}

      {files.length > 0 && (
        <div className="file-list">
          {files.map((file, index) => (
            <div key={index} className="file-chip">
              <span>{file.name}</span>
              <button onClick={() => removeFile(index)}>&times;</button>
            </div>
          ))}
        </div>
      )}

      <div className="form-actions">
        <button
          className="btn btn-primary"
          onClick={handleSubmitAll}
          disabled={submitting || files.length === 0}
        >
          {submitting ? 'Submitting...' : `Submit all (${files.length})`}
        </button>
      </div>
    </div>
  );
}
