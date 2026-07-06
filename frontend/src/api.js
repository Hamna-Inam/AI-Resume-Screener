import axios from 'axios';

const api = axios.create({
  baseURL: '/',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (email, password) =>
  api.post('/v1/auth/login', { email, password });

export const getJobDescriptions = () =>
  api.get('/v1/job-descriptions');

export const createJobDescription = (title, description) =>
  api.post('/v1/job-descriptions', { title, description });

export const submitResume = (jobDescriptionId, candidateName, file) => {
  const formData = new FormData();
  formData.append('job_description_id', jobDescriptionId);
  formData.append('candidate_name', candidateName);
  formData.append('file', file);
  return api.post('/v1/resumes', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getResumes = (params = {}) =>
  api.get('/v1/resumes', { params });

export const getStats = () =>
  api.get('/v1/stats');

export const WS_BASE = window.location.origin.replace('http', 'ws');