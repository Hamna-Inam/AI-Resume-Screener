import { useState, useEffect } from 'react';
import { getStats } from './api';

export default function StatsBar({ refreshTrigger }) {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getStats().then((res) => setStats(res.data));
  }, [refreshTrigger]);

  return (
    <>
      <p className="greeting">Here's how today's screening looks.</p>
      <div className="stats-bar">
        <div className="stat-card">
          <span className="stat-label">Resumes screened</span>
          <span className="stat-value">{stats ? stats.resumes_screened : '—'}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Strong matches</span>
          <span className="stat-value">{stats ? stats.strong_matches : '—'}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Avg. match score</span>
          <span className="stat-value">{stats ? `${stats.avg_match_score}%` : '—'}</span>
        </div>
      </div>
    </>
  );
}