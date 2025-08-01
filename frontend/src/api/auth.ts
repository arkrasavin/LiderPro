import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export async function login(login: string, password: string) {
  const response = await axios.post(`${API_URL}/login`, new URLSearchParams({ login, password }), {
    withCredentials: true,
  });
  return response.data;
}

export async function logout() {
  await axios.get(`${API_URL}/logout`, { withCredentials: true });
}

export async function getCurrentUser() {
  const response = await axios.get(`${API_URL}/me`, { withCredentials: true });
  return response.data;
}
