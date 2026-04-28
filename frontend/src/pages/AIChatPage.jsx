import { useState } from 'react';
import Layout from '../components/Layout';
import { sendChat } from '../services/aiService';

export default function AIChatPage() {
  const [message, setMessage] = useState('Show low stock products');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await sendChat({ message });
      setResponse(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'AI request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <form onSubmit={handleSubmit} className="space-y-3">
        <textarea className="w-full border rounded p-3" rows="4" value={message} onChange={(e) => setMessage(e.target.value)} />
        <button className="bg-slate-900 text-white px-4 py-2 rounded">{loading ? 'Thinking...' : 'Ask AI'}</button>
      </form>
      {error && <p className="text-red-600 mt-3">{error}</p>}
      {response && (
        <section className="mt-4 bg-white p-4 rounded shadow">
          <h2 className="font-semibold">Answer</h2>
          <p>{response.answer}</p>
          <h3 className="font-semibold mt-3">Tool Results</h3>
          <pre className="bg-gray-100 p-2 rounded overflow-x-auto text-sm">{JSON.stringify(response.tool_results, null, 2)}</pre>
        </section>
      )}
    </Layout>
  );
}
