import { useEffect, useState } from 'react';
import { createProduct, fetchProducts } from '../services/productService';

export function useProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      setProducts(await fetchProducts());
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const add = async (payload) => {
    setLoading(true);
    setError('');
    try {
      await createProduct({ ...payload, stock: Number(payload.stock), price: Number(payload.price), threshold: Number(payload.threshold) });
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create product');
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return { products, loading, error, add };
}
