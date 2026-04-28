import { useState } from 'react';
import { validateProductForm } from '../utils/validators';

const initialState = { name: '', sku: '', stock: 0, price: 0, threshold: 10, expiry: '' };

export default function ProductForm({ onSubmit }) {
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validateProductForm(form);
    if (validationError) {
      setError(validationError);
      return;
    }
    setError('');
    await onSubmit(form);
    setForm(initialState);
  };

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-3 bg-white p-4 rounded shadow">
      {error && <p className="text-red-600 md:col-span-2">{error}</p>}
      {Object.keys(initialState).map((key) => (
        <input
          key={key}
          className="border p-2 rounded"
          placeholder={key}
          value={form[key]}
          onChange={(e) => setForm((prev) => ({ ...prev, [key]: e.target.value }))}
        />
      ))}
      <button className="bg-slate-900 text-white p-2 rounded md:col-span-2">Create Product</button>
    </form>
  );
}
