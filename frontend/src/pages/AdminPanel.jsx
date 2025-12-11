import { useState, useEffect } from 'react';
import { Users, Eye, Shield, UserX, Search, ChevronDown, ChevronRight, FileText, Upload, TrendingUp, DollarSign, AlertTriangle, BarChart3, Activity } from 'lucide-react';
import api from '../services/api';

export default function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userDetails, setUserDetails] = useState(null);
  const [userAnalyses, setUserAnalyses] = useState([]);
  const [userUploads, setUserUploads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedUser, setExpandedUser] = useState(null);
  const [activeTab, setActiveTab] = useState('overview'); // overview, analyses, uploads
  const [systemMetrics, setSystemMetrics] = useState(null);
  const [metricsLoading, setMetricsLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
    fetchSystemMetrics();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/admin/users');
      console.log('Users fetched:', response.data);
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to load users';
      setError(errorMsg);
      alert(`Error: ${errorMsg}. Make sure you are logged in as admin and the backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  const fetchSystemMetrics = async () => {
    setMetricsLoading(true);
    try {
      const response = await api.get('/dashboard/admin');
      console.log('System metrics fetched:', response.data);
      setSystemMetrics(response.data.system_metrics);
    } catch (error) {
      console.error('Failed to fetch system metrics:', error);
      // Don't alert for metrics - just log the error
    } finally {
      setMetricsLoading(false);
    }
  };

  const fetchUserDetails = async (userId) => {
    setLoading(true);
    try {
      const [detailsResponse, analysesResponse, uploadsResponse] = await Promise.all([
        api.get(`/admin/users/${userId}`),
        api.get(`/admin/users/${userId}/analyses`),
        api.get(`/admin/users/${userId}/uploads`)
      ]);
      
      console.log('User details:', detailsResponse.data);
      console.log('User analyses:', analysesResponse.data);
      console.log('User uploads:', uploadsResponse.data);
      
      setUserDetails(detailsResponse.data);
      setUserAnalyses(analysesResponse.data.analyses || []);
      setUserUploads(uploadsResponse.data.uploads || []);
      setSelectedUser(userId);
      setExpandedUser(userId);
      setActiveTab('analyses');
    } catch (error) {
      console.error('Failed to fetch user details:', error);
      alert(error.response?.data?.detail || 'Failed to load user details');
    } finally {
      setLoading(false);
    }
  };

  const toggleUserRole = async (userId, currentRole) => {
    const newRole = currentRole === 'admin' ? 'user' : 'admin';
    try {
      await api.put(`/admin/users/${userId}/role`, { role: newRole });
      fetchUsers();
      if (selectedUser === userId) {
        fetchUserDetails(userId);
      }
    } catch (error) {
      console.error('Failed to update role:', error);
      alert(error.response?.data?.detail || 'Failed to update role');
    }
  };

  const toggleUserActive = async (userId) => {
    try {
      await api.put(`/admin/users/${userId}/toggle-active`);
      fetchUsers();
      if (selectedUser === userId) {
        fetchUserDetails(userId);
      }
    } catch (error) {
      console.error('Failed to toggle user active status:', error);
      alert(error.response?.data?.detail || 'Failed to update user status');
    }
  };

  const deleteUser = async (userId) => {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      return;
    }
    
    try {
      await api.delete(`/admin/users/${userId}`);
      fetchUsers();
      if (selectedUser === userId) {
        setSelectedUser(null);
        setUserDetails(null);
        setUserAnalyses([]);
        setUserUploads([]);
        setExpandedUser(null);
      }
    } catch (error) {
      console.error('Failed to delete user:', error);
      alert(error.response?.data?.detail || 'Failed to delete user');
    }
  };

  const filteredUsers = users.filter(user => 
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (user.company_name && user.company_name.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount || 0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-3 bg-gradient-to-br from-gray-800 to-gray-600 rounded-xl">
              <Shield className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Admin Panel</h1>
              <p className="text-gray-600">Manage users and view their data</p>
            </div>
          </div>
        </div>

        {/* System Metrics */}
        {systemMetrics && (
          <div className="mb-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Total Users */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Total Users</p>
                  <p className="text-3xl font-bold text-gray-900">{systemMetrics.totalUsers}</p>
                </div>
                <div className="p-3 bg-gradient-to-br from-gray-700 to-gray-500 rounded-lg">
                  <Users className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>

            {/* Active Users */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Active Users</p>
                  <p className="text-3xl font-bold text-green-600">{systemMetrics.activeUsers}</p>
                </div>
                <div className="p-3 bg-gradient-to-br from-green-600 to-green-500 rounded-lg">
                  <Activity className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>

            {/* Total Revenue */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Total Revenue</p>
                  <p className="text-2xl font-bold text-gray-900">₹{systemMetrics.totalRevenue?.toLocaleString() || 0}</p>
                </div>
                <div className="p-3 bg-gradient-to-br from-blue-600 to-blue-500 rounded-lg">
                  <DollarSign className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>

            {/* Total Leakage */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Total Leakage</p>
                  <p className="text-2xl font-bold text-red-600">₹{systemMetrics.totalLeakage?.toLocaleString() || 0}</p>
                </div>
                <div className="p-3 bg-gradient-to-br from-red-600 to-red-500 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>

            {/* Average Risk Score */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Avg Risk Score</p>
                  <p className="text-3xl font-bold text-orange-600">{systemMetrics.avgRiskScore?.toFixed(1) || '0.0'}</p>
                </div>
                <div className="p-3 bg-gradient-to-br from-orange-600 to-orange-500 rounded-lg">
                  <BarChart3 className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        )}

        {metricsLoading && !systemMetrics && (
          <div className="mb-8">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
              <p className="text-center text-gray-500">Loading system metrics...</p>
            </div>
          </div>
        )}

        {/* Error Banner */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
            <p className="text-red-800 font-semibold">Error: {error}</p>
            <p className="text-red-600 text-sm mt-1">Make sure the backend is running and you're logged in as admin.</p>
          </div>
        )}

        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Search users by name, email, or company..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-gray-500 focus:border-transparent bg-white text-gray-900"
            />
          </div>
        </div>

        {/* Users List */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200">
          {/* Mobile Card View (hidden on md+) */}
          <div className="md:hidden divide-y divide-gray-200">
            {loading && filteredUsers.length === 0 ? (
              <div className="px-6 py-12 text-center text-gray-500">Loading users...</div>
            ) : filteredUsers.length === 0 ? (
              <div className="px-6 py-12 text-center text-gray-500">No users found</div>
            ) : (
              filteredUsers.map((user) => (
                <div key={user.id} className="p-4">
                  {/* User Card */}
                  <div className="flex items-start gap-3 mb-3">
                    <div className="flex-shrink-0 h-12 w-12 bg-gradient-to-br from-gray-700 to-gray-500 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold">{user.full_name.charAt(0).toUpperCase()}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-semibold text-gray-900 truncate">{user.full_name}</h3>
                      <p className="text-xs text-gray-600 truncate">{user.email}</p>
                      {user.company_name && (
                        <p className="text-xs text-gray-500 truncate mt-1">{user.company_name}</p>
                      )}
                    </div>
                  </div>
                  
                  {/* Badges */}
                  <div className="flex flex-wrap gap-2 mb-3">
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                      user.role === 'admin' 
                        ? 'bg-gradient-to-r from-gray-800 to-gray-600 text-white' 
                        : 'bg-gray-200 text-gray-800'
                    }`}>
                      {user.role}
                    </span>
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                      user.is_active 
                        ? 'bg-gray-900 text-white' 
                        : 'bg-gray-300 text-gray-700'
                    }`}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                    <span className="px-3 py-1 text-xs text-gray-600 bg-gray-100 rounded-full">
                      Joined {new Date(user.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  
                  {/* Actions */}
                  <div className="flex gap-2">
                    <button
                      onClick={() => expandedUser === user.id ? setExpandedUser(null) : fetchUserDetails(user.id)}
                      className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                    >
                      {expandedUser === user.id ? 'Hide' : 'View'} Details
                    </button>
                    <button
                      onClick={() => toggleUserRole(user.id, user.role)}
                      className="px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                      title={`Change to ${user.role === 'admin' ? 'User' : 'Admin'}`}
                    >
                      <Shield className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => toggleUserActive(user.id)}
                      className="px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                      title={user.is_active ? 'Deactivate' : 'Activate'}
                    >
                      <Users className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => deleteUser(user.id)}
                      className="px-3 py-2 text-red-600 hover:text-red-900 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete User"
                    >
                      <UserX className="h-5 w-5" />
                    </button>
                  </div>
                  
                  {/* Expanded Details (Mobile) */}
                  {expandedUser === user.id && userDetails && (
                    <div className="mt-4 pt-4 border-t border-gray-200 space-y-4">
                      {/* Stats */}
                      <div className="grid grid-cols-2 gap-3">
                        <div className="bg-gray-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600">Analyses</p>
                          <p className="text-xl font-bold text-gray-900">{userDetails.total_analyses}</p>
                        </div>
                        <div className="bg-gray-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600">Uploads</p>
                          <p className="text-xl font-bold text-gray-900">{userDetails.total_uploads}</p>
                        </div>
                      </div>
                      
                      {/* Last Login */}
                      <div className="text-xs text-gray-600">
                        Last login: <span className="font-medium text-gray-900">
                          {userDetails.last_login ? formatDate(userDetails.last_login) : 'Never'}
                        </span>
                      </div>
                      
                      {/* Tabs */}
                      <div className="flex gap-2 border-b border-gray-200">
                        <button
                          onClick={() => setActiveTab('analyses')}
                          className={`pb-2 px-3 text-sm font-medium border-b-2 transition-colors ${
                            activeTab === 'analyses'
                              ? 'border-gray-900 text-gray-900'
                              : 'border-transparent text-gray-500'
                          }`}
                        >
                          Analyses ({userAnalyses.length})
                        </button>
                        <button
                          onClick={() => setActiveTab('uploads')}
                          className={`pb-2 px-3 text-sm font-medium border-b-2 transition-colors ${
                            activeTab === 'uploads'
                              ? 'border-gray-900 text-gray-900'
                              : 'border-transparent text-gray-500'
                          }`}
                        >
                          Uploads ({userUploads.length})
                        </button>
                      </div>
                      
                      {/* Tab Content */}
                      {activeTab === 'analyses' && (
                        <div className="space-y-2">
                          {userAnalyses.length === 0 ? (
                            <p className="text-center text-gray-500 py-4 text-sm">No analyses found</p>
                          ) : (
                            userAnalyses.map((analysis) => (
                              <div key={analysis.id} className="bg-gray-50 p-3 rounded-lg text-xs space-y-1">
                                <p className="font-semibold text-gray-900">{analysis.business_name}</p>
                                <p className="text-gray-600">Industry: {analysis.industry}</p>
                                <div className="flex justify-between">
                                  <span className="text-gray-600">Revenue: <span className="font-semibold text-gray-900">{formatCurrency(analysis.total_revenue)}</span></span>
                                  <span className="text-gray-600">Leakage: <span className="font-semibold text-red-600">{formatCurrency(analysis.leakage_amount)}</span></span>
                                </div>
                              </div>
                            ))
                          )}
                        </div>
                      )}
                      
                      {activeTab === 'uploads' && (
                        <div className="space-y-2">
                          {userUploads.length === 0 ? (
                            <p className="text-center text-gray-500 py-4 text-sm">No uploads found</p>
                          ) : (
                            userUploads.map((upload) => (
                              <div key={upload.id} className="bg-gray-50 p-3 rounded-lg text-xs space-y-1">
                                <div className="flex items-center gap-2">
                                  <FileText className="h-4 w-4 text-gray-600 flex-shrink-0" />
                                  <p className="font-semibold text-gray-900 truncate">{upload.filename}</p>
                                </div>
                                <p className="text-gray-600">{upload.rows_count?.toLocaleString()} rows × {upload.columns_count} cols</p>
                                <p className="text-gray-500">{formatDate(upload.created_at)}</p>
                              </div>
                            ))
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
          
          {/* Desktop Table View (hidden on mobile) */}
          <div className="hidden md:block overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gradient-to-r from-gray-800 to-gray-700">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Company
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Role
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Joined
                  </th>
                  <th className="px-6 py-4 text-right text-xs font-semibold text-white uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {loading && filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                      Loading users...
                    </td>
                  </tr>
                ) : filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                      No users found
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((user) => (
                    <>
                      <tr key={user.id} className={`hover:bg-gray-50 transition-colors ${expandedUser === user.id ? 'bg-gray-50' : ''}`}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-10 w-10 bg-gradient-to-br from-gray-700 to-gray-500 rounded-full flex items-center justify-center">
                              <span className="text-white font-semibold text-sm">
                                {user.full_name.charAt(0).toUpperCase()}
                              </span>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900">{user.full_name}</div>
                              <div className="text-sm text-gray-500">{user.email}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">{user.company_name || '-'}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            user.role === 'admin' 
                              ? 'bg-gradient-to-r from-gray-800 to-gray-600 text-white' 
                              : 'bg-gray-200 text-gray-800'
                          }`}>
                            {user.role}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            user.is_active 
                              ? 'bg-gray-900 text-white' 
                              : 'bg-gray-300 text-gray-700'
                          }`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatDate(user.created_at)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <div className="flex items-center justify-end space-x-2">
                            <button
                              onClick={() => expandedUser === user.id ? setExpandedUser(null) : fetchUserDetails(user.id)}
                              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                              title="View Details"
                            >
                              {expandedUser === user.id ? <ChevronDown className="h-5 w-5" /> : <ChevronRight className="h-5 w-5" />}
                            </button>
                            <button
                              onClick={() => toggleUserRole(user.id, user.role)}
                              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                              title={`Change to ${user.role === 'admin' ? 'User' : 'Admin'}`}
                            >
                              <Shield className="h-5 w-5" />
                            </button>
                            <button
                              onClick={() => toggleUserActive(user.id)}
                              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                              title={user.is_active ? 'Deactivate' : 'Activate'}
                            >
                              <Users className="h-5 w-5" />
                            </button>
                            <button
                              onClick={() => deleteUser(user.id)}
                              className="p-2 text-red-600 hover:text-red-900 hover:bg-red-50 rounded-lg transition-colors"
                              title="Delete User"
                            >
                              <UserX className="h-5 w-5" />
                            </button>
                          </div>
                        </td>
                      </tr>
                      
                      {/* Expanded Details */}
                      {expandedUser === user.id && userDetails && (
                        <tr>
                          <td colSpan="6" className="px-6 py-6 bg-gradient-to-br from-gray-50 to-white">
                            <div className="space-y-6">
                              {/* Stats Cards */}
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                                  <div className="flex items-center justify-between">
                                    <div>
                                      <p className="text-sm text-gray-600">Total Analyses</p>
                                      <p className="text-2xl font-bold text-gray-900">{userDetails.total_analyses}</p>
                                    </div>
                                    <div className="p-3 bg-gradient-to-br from-gray-700 to-gray-500 rounded-lg">
                                      <TrendingUp className="h-6 w-6 text-white" />
                                    </div>
                                  </div>
                                </div>
                                
                                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                                  <div className="flex items-center justify-between">
                                    <div>
                                      <p className="text-sm text-gray-600">Total Uploads</p>
                                      <p className="text-2xl font-bold text-gray-900">{userDetails.total_uploads}</p>
                                    </div>
                                    <div className="p-3 bg-gradient-to-br from-gray-600 to-gray-400 rounded-lg">
                                      <Upload className="h-6 w-6 text-white" />
                                    </div>
                                  </div>
                                </div>
                                
                                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                                  <div className="flex items-center justify-between">
                                    <div>
                                      <p className="text-sm text-gray-600">Last Login</p>
                                      <p className="text-sm font-semibold text-gray-900">
                                        {userDetails.last_login ? formatDate(userDetails.last_login) : 'Never'}
                                      </p>
                                    </div>
                                    <div className="p-3 bg-gradient-to-br from-gray-500 to-gray-300 rounded-lg">
                                      <Eye className="h-6 w-6 text-white" />
                                    </div>
                                  </div>
                                </div>
                              </div>

                              {/* Tabs */}
                              <div className="border-b border-gray-200">
                                <div className="flex space-x-4">
                                  <button
                                    onClick={() => setActiveTab('analyses')}
                                    className={`pb-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                                      activeTab === 'analyses'
                                        ? 'border-gray-900 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                                  >
                                    Analyses ({userAnalyses.length})
                                  </button>
                                  <button
                                    onClick={() => setActiveTab('uploads')}
                                    className={`pb-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                                      activeTab === 'uploads'
                                        ? 'border-gray-900 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                                  >
                                    Uploads ({userUploads.length})
                                  </button>
                                </div>
                              </div>

                              {/* Tab Content */}
                              {activeTab === 'analyses' && (
                                <div className="space-y-3">
                                  {userAnalyses.length === 0 ? (
                                    <p className="text-center text-gray-500 py-8">No analyses found</p>
                                  ) : (
                                    userAnalyses.map((analysis) => (
                                      <div key={analysis.id} className="bg-white p-4 rounded-lg border border-gray-200 hover:border-gray-400 transition-colors">
                                        <div className="flex items-center justify-between">
                                          <div className="flex-1">
                                            <h4 className="font-semibold text-gray-900">{analysis.business_name}</h4>
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-2 text-sm">
                                              <div>
                                                <span className="text-gray-600">Industry:</span>
                                                <span className="ml-2 text-gray-900">{analysis.industry}</span>
                                              </div>
                                              <div>
                                                <span className="text-gray-600">Revenue:</span>
                                                <span className="ml-2 text-gray-900 font-semibold">{formatCurrency(analysis.total_revenue)}</span>
                                              </div>
                                              <div>
                                                <span className="text-gray-600">Leakage:</span>
                                                <span className="ml-2 text-red-600 font-semibold">{formatCurrency(analysis.leakage_amount)}</span>
                                              </div>
                                              <div>
                                                <span className="text-gray-600">Date:</span>
                                                <span className="ml-2 text-gray-900">{formatDate(analysis.created_at)}</span>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                      </div>
                                    ))
                                  )}
                                </div>
                              )}

                              {activeTab === 'uploads' && (
                                <div className="space-y-3">
                                  {userUploads.length === 0 ? (
                                    <p className="text-center text-gray-500 py-8">No uploads found</p>
                                  ) : (
                                    userUploads.map((upload) => (
                                      <div key={upload.id} className="bg-white p-4 rounded-lg border border-gray-200 hover:border-gray-400 transition-colors">
                                        <div className="flex items-center justify-between">
                                          <div className="flex items-center space-x-3">
                                            <FileText className="h-8 w-8 text-gray-600" />
                                            <div>
                                              <h4 className="font-semibold text-gray-900">{upload.filename}</h4>
                                              <p className="text-sm text-gray-600">
                                                {upload.rows_count?.toLocaleString()} rows × {upload.columns_count} columns
                                              </p>
                                              <p className="text-xs text-gray-500 mt-1">{formatDate(upload.created_at)}</p>
                                            </div>
                                          </div>
                                          <span className="text-xs px-2 py-1 bg-gray-200 text-gray-800 rounded">
                                            {upload.file_type.toUpperCase()}
                                          </span>
                                        </div>
                                      </div>
                                    ))
                                  )}
                                </div>
                              )}
                            </div>
                          </td>
                        </tr>
                      )}
                    </>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
