import apiClient from './apiClient';

export const fetchProducts = () => apiClient.get('/products').then((r) => r.data);
export const createProduct = (payload) => apiClient.post('/products', payload).then((r) => r.data);
export const forecastProduct = (id) => apiClient.get(`/products/${id}/forecast`).then((r) => r.data);
