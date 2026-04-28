import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginRequest } from '../services/authService';
import { useAuthStore } from '../store/authStore';
import { validateEmail } from '../utils/validators';

export default function LoginPage() {
  const navigate = useNavigate();
  const setSession = useAuthStore((s) => s.setSession);
  const [email, setEmail] = useState('admin@smartstore.ai');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateEmail(email)) {
      setError('Invalid email');
      return;
    }
    if (password.length < 8) {
      setError('Password should be at least 8 characters');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const tokens = await loginRequest({ email, password });
      setSession({ accessToken: tokens.access_token, user: { email } });
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow w-full max-w-md space-y-3">
        <h1 className="text-2xl font-semibold">SmartStore AI Login</h1>
        {error && <p className="text-red-600">{error}</p>}
        <input className="w-full border p-2 rounded" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input className="w-full border p-2 rounded" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button className="w-full bg-slate-900 text-white py-2 rounded" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
      </form>
    </div>
  );
}
