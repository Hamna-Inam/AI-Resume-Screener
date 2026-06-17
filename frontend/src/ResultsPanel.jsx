import { useEffect, useRef, useState } from 'react';
import { WS_BASE, getResumes } from './api';
import Avatar from './Avatar';
import { matchTier, tierPillClass } from './scoring';

export default function ResultsPanel({ submissions, onUpdate }) {
  const socketsRef = useRef({});
  const requestIdRef = useRef(0);
  const [search, setSearch] = useState('');
  const [minScore, setMinScore] = useState('');
  const [serverResumes, setServerResumes] = useState(null);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    submissions.forEach((sub) => {
      if (socketsRef.current[sub.id]) return;
      if (sub.status === 'completed' || sub.status === 'failed') return;
      const ws = new WebSocket(`${WS_BASE}/v1/ws/resumes/${sub.id}`);
      ws.onmessage = (event) => onUpdate(sub.id, JSON.parse(event.data));
      ws.onerror = () => console.error(`WebSocket error for resume ${sub.id}`);
      socketsRef.current[sub.id] = ws;
    });
  }, [submissions]);

  // Close any open sockets when the panel unmounts (e.g. on logout).
  useEffect(() => {
    return () => {
      Object.values(socketsRef.current).forEach((ws) => ws.close());
    };
  }, []);

  useEffect(() => {
    if (!search && !minScore) {
      setServerResumes(null);
      return;
    }
    const requestId = ++requestIdRef.current;
    const timeout = setTimeout(() => {
      const params = {};
      if (search) params.search = search;
      if (minScore) params.min_score = minScore;
      getResumes(params).then((res) => {
        // Ignore this response if a newer search has since been kicked off.
        if (requestIdRef.current === requestId) {
          setServerResumes(res.data);
        }
      });
    }, 300);
    return () => clearTimeout(timeout);
  }, [search, minScore]);

  const displayed = serverResumes
    ? submissions.filter((sub) => serverResumes.some((r) => r.id === sub.id))
    : submissions;

  const toggle = (id) => setExpanded((current) => (current === id ? null : id));

  return (
    <div className="panel">
      <h3>Results</h3>

      <div className="filter-bar">
        <input
          className="input"
          placeholder="Search candidates..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select className="select" value={minScore} onChange={(e) => setMinScore(e.target.value)}>
          <option value="">All scores</option>
          <option value="80">Score: 80%+</option>
          <option value="60">Score: 60%+</option>
          <option value="40">Score: 40%+</option>
        </select>
      </div>

      {displayed.length === 0 && <p className="empty-state">No resumes submitted yet.</p>}

      {displayed.map((sub) => {
        const isOpen = expanded === sub.id;
        const tier = sub.result ? matchTier(sub.result.match_score) : null;
        return (
          <div
            key={sub.id}
            className="candidate-card"
            role="button"
            tabIndex={0}
            aria-expanded={isOpen}
            onClick={() => toggle(sub.id)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggle(sub.id);
              }
            }}
          >
            <div className="candidate-row">
              <Avatar name={sub.candidate_name} />
              <div className="candidate-info">
                <span className="candidate-name">{sub.candidate_name}</span>
                <span className="candidate-subtitle">
                  {sub.status === 'completed' && sub.result
                    ? sub.result.recommendation.split(';')[0]
                    : sub.status}
                </span>
              </div>
              {sub.status === 'completed' && sub.result ? (
                <span className={`score-pill ${tierPillClass(tier)}`}>
                  {sub.result.match_score}% match
                </span>
              ) : (
                <span className={`status-badge status-${sub.status}`}>{sub.status}</span>
              )}
              <svg className={`chevron ${isOpen ? 'chevron-open' : ''}`} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </div>

            {sub.result && (
              <div className={`result-detail ${isOpen ? 'result-detail-open' : ''}`}>
                <p><strong>Strengths:</strong> {sub.result.strengths}</p>
                <p><strong>Gaps:</strong> {sub.result.gaps}</p>
                <p><strong>Recommendation:</strong> {sub.result.recommendation}</p>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
