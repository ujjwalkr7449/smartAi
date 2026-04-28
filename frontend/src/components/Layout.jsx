import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function Layout({ children }) {
  const logout = useAuthStore((s) => s.logout);
  return (
    <div className="min-h-screen">
      <header className="bg-slate-900 text-white px-4 py-3 flex justify-between">
        <nav className="flex gap-4">
          <Link to="/">Dashboard</Link>
          <Link to="/products">Products</Link>
          <Link to="/ai">AI Assistant</Link>
        </nav>
        <button onClick={logout} className="bg-red-500 px-3 py-1 rounded">Logout</button>
      </header>
      <main className="p-4 md:p-8 max-w-[1440px] mx-auto">{children}</main>
    </div>
  );
}
