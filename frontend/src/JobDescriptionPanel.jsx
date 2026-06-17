import { useState, useEffect } from 'react';
import { getJobDescriptions, createJobDescription } from './api';

export default function JobDescriptionPanel({ selectedJD, onSelectJD }) {
  const [jds, setJds] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchJDs();
  }, []);

  const fetchJDs = async () => {
    const res = await getJobDescriptions();
    setJds(res.data);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    const res = await createJobDescription(title, description);
    setJds([...jds, res.data]);
    onSelectJD(res.data.id);
    setTitle('');
    setDescription('');
    setShowForm(false);
  };

  return (
    <div className="panel">
      <h3>Job description</h3>

      <select
        className="select"
        value={selectedJD || ''}
        onChange={(e) => onSelectJD(e.target.value)}
      >
        <option value="">Select a job description</option>
        {jds.map((jd) => (
          <option key={jd.id} value={jd.id}>{jd.title}</option>
        ))}
      </select>

      <button className="btn" onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Cancel' : '+ New job description'}
      </button>

      {showForm && (
        <form onSubmit={handleCreate} style={{ marginTop: 12 }}>
          <input
            className="input"
            placeholder="Job title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <textarea
            className="textarea"
            placeholder="Job description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
          <button type="submit" className="btn btn-primary">Create</button>
        </form>
      )}
    </div>
  );
}