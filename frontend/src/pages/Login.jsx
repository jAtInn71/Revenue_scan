import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import { MdSmartToy, MdAnalytics, MdLock } from 'react-icons/md';

const Login = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await login(formData);
      localStorage.setItem('token', response.access_token);
      setIsAuthenticated(true);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const useDemoCredentials = (email, password) => {
    setFormData({ email, password });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white px-4 py-8 animate-fade-in">
      <div className="w-full max-w-md">
        {/* Logo & Branding */}
        <div className="text-center mb-10 animate-slide-down">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-black rounded-xl shadow-lg mb-4 hover:shadow-xl transition-shadow duration-300">
            <svg viewBox="0 0 40 40" className="w-8 h-8">
              <defs>
                <linearGradient id="rGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#ffffff', stopOpacity: 1 }} />
                  <stop offset="100%" style={{ stopColor: '#f0f0f0', stopOpacity: 1 }} />
                </linearGradient>
              </defs>
              <rect x="10" y="8" width="4" height="24" fill="url(#rGradient)" rx="2" />
              <path d="M 14 8 Q 22 8 22 14 Q 22 18 14 18" fill="none" stroke="url(#rGradient)" strokeWidth="4" strokeLinecap="round" />
              <line x1="14" y1="18" x2="26" y2="32" stroke="url(#rGradient)" strokeWidth="4" strokeLinecap="round" />
            </svg>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-black">
            Revenue
          </h1>
          <p className="text-gray-600 mt-2 text-sm md:text-base font-semibold">AI-Powered Revenue Analytics</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6 md:p-8 animate-slide-up">
          <h2 className="text-2xl font-bold text-black mb-6">Welcome Back</h2>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg animate-shake">
              <p className="text-sm text-red-600 font-medium">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-black mb-2">
                Email Address
              </label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-black transition-all duration-300"
                placeholder="you@company.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black mb-2">
                Password
              </label>
              <input
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-black transition-all duration-300"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-black text-white py-3 rounded-lg font-semibold hover:bg-gray-900 shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Signing in...
                </span>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-7 space-y-3">
            <p className="text-sm text-gray-600 font-semibold text-center">Demo Credentials:</p>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => useDemoCredentials('admin@revenue.com', 'admin123')}
                className="px-4 py-2 bg-black text-white text-xs font-semibold rounded-lg hover:bg-gray-900 hover:shadow-md border border-gray-300 transition-all duration-300 transform hover:scale-105 active:scale-95"
              >
                Admin
              </button>
              <button
                type="button"
                onClick={() => useDemoCredentials('user@revenue.com', 'user123')}
                className="px-4 py-2 bg-gray-800 text-white text-xs font-semibold rounded-lg hover:bg-gray-700 hover:shadow-md border border-gray-300 transition-all duration-300 transform hover:scale-105 active:scale-95"
              >
                User
              </button>
            </div>
          </div>

          {/* Sign Up Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-600 text-sm">
              Don't have an account?{' '}
              <Link to="/signup" className="text-black font-semibold hover:text-gray-700 transition-colors duration-300">
                Create one
              </Link>
            </p>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-8 grid grid-cols-3 gap-3">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center hover:border-black hover:shadow-lg transition-all duration-300 transform hover:scale-105 animate-slide-up">
            <MdSmartToy className="text-3xl mx-auto mb-2 text-black" />
            <p className="text-xs text-gray-600 font-medium">AI Insights</p>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center hover:border-black hover:shadow-lg transition-all duration-300 transform hover:scale-105 animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <MdAnalytics className="text-3xl mx-auto mb-2 text-black" />
            <p className="text-xs text-gray-600 font-medium">Analytics</p>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center hover:border-black hover:shadow-lg transition-all duration-300 transform hover:scale-105 animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <MdLock className="text-3xl mx-auto mb-2 text-black" />
            <p className="text-xs text-gray-600 font-medium">Secure</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
