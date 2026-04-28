import apiClient from './apiClient';

export const sendChat = (payload) => apiClient.post('/ai/chat', payload).then((r) => r.data);
