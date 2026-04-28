import apiClient from './apiClient';

export const loginRequest = (payload) => apiClient.post('/auth/login', payload).then((r) => r.data);
export const registerRequest = (payload) => apiClient.post('/auth/register', payload).then((r) => r.data);
