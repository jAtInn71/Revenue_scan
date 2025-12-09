import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import AIChat from './pages/AIChat';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import AnalysisHistory from './pages/AnalysisHistory';
import NewBusinessAnalyze from './pages/NewBusinessAnalyze';
import ExistingBusinessAnalyze from './pages/ExistingBusinessAnalyze';
import AdminPanel from './pages/AdminPanel';
import Layout from './components/Layout';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div style={{minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'white'}}>
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem'}}>
          <div style={{width: '64px', height: '64px', border: '4px solid black', borderTop: '4px solid transparent', borderRadius: '50%', animation: 'spin 1s linear infinite'}}></div>
          <p style={{color: '#4b5563', fontWeight: '500'}}>Loading...</p>
        </div>
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={
          isAuthenticated ? <Navigate to="/dashboard" /> : <Login setIsAuthenticated={setIsAuthenticated} />
        } />
        <Route path="/signup" element={
          isAuthenticated ? <Navigate to="/dashboard" /> : <Signup setIsAuthenticated={setIsAuthenticated} />
        } />
        
        <Route path="/" element={
          isAuthenticated ? <Layout setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" replace />
        }>
          <Route index element={<Navigate to="/dashboard" />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="upload" element={<Upload />} />
          <Route path="ai-chat" element={<AIChat />} />
          <Route path="reports" element={<Reports />} />
          <Route path="history" element={<AnalysisHistory />} />
          <Route path="settings" element={<Settings />} />
          <Route path="admin" element={<AdminPanel />} />
          <Route path="analyze/new-business" element={<NewBusinessAnalyze />} />
          <Route path="analyze/existing-business" element={<ExistingBusinessAnalyze />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
