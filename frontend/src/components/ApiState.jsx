export default function ApiState({ loading, error, children }) {
  if (loading) return <p className="text-blue-600">Loading...</p>;
  if (error) return <p className="text-red-600">{error}</p>;
  return children;
}
