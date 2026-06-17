import { useState, useEffect } from 'react';
import { getResumes } from './api';
import Login from './Login';
import JobDescriptionPanel from './JobDescriptionPanel';
import ResumeForm from './ResumeForm';
import ResultsPanel from './ResultsPanel';
import ChartPanel from './ChartPanel';
import StatsBar from './StatsBar';

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'));
  const [selectedJD, setSelectedJD] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [statsRefresh, setStatsRefresh] = useState(0);

  useEffect(() => {
    if (!loggedIn) return;
    getResumes()
      .then((res) => setSubmissions(res.data))
      .catch((err) => console.error('Failed to load existing resumes:', err));
  }, [loggedIn]);

  const handleSubmitted = (resume) => {
    setSubmissions((prev) => [...prev, resume]);
  };

  const handleUpdate = (resumeId, data) => {
    setSubmissions((prev) =>
      prev.map((sub) =>
        sub.id === resumeId
          ? { ...sub, status: data.status, result: data.result || sub.result }
          : sub
      )
    );
    if (data.status === 'completed' || data.status === 'failed') {
      setStatsRefresh((n) => n + 1);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setLoggedIn(false);
  };

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div className="app-shell">
      <div className="app-header">
        <h1>
          <span className="brand-mark" aria-hidden="true">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 20A7 7 0 0 1 4 13V8a1 1 0 0 1 1-1h5a7 7 0 0 1 7 7v1a5 5 0 0 1-5 5z" />
              <path d="M11 20v-9" />
            </svg>
          </span>
          Resume Screener
        </h1>
        <button className="btn" onClick={handleLogout}>Log out</button>
      </div>

      <StatsBar refreshTrigger={statsRefresh} />

      <JobDescriptionPanel selectedJD={selectedJD} onSelectJD={setSelectedJD} />
      <ResumeForm jobDescriptionId={selectedJD} onSubmitted={handleSubmitted} />

      <div className="main-grid">
        <ResultsPanel submissions={submissions} onUpdate={handleUpdate} />
        <ChartPanel submissions={submissions} />
      </div>
    </div>
  );
}