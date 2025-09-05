import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export async function getEmployeeData() {
  const response = await axios.get(`${API_URL}/employee`, { withCredentials: true });
  return response.data;
}

export async function getProfile() {
  const response = await axios.get(`${API_URL}/profile`, { withCredentials: true });
  return response.data;
}
