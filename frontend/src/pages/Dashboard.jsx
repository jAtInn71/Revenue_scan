import { useState, useEffect } from 'react';
import { getDashboardData } from '../services/api';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const dashboardData = await getDashboardData();
      setData(dashboardData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-6">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Overview of your revenue analytics</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                ${data?.metrics?.totalRevenue?.toLocaleString() || '0'}
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Net Profit: ${data?.metrics?.netProfit?.toLocaleString() || '0'} 
                ({data?.metrics?.profitMargin?.toFixed(1) || '0'}%)
              </p>
            </div>
            <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
              <span className="text-2xl">💰</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Revenue Leakage</p>
              <p className="text-3xl font-bold text-red-600 mt-2">
                ${data?.metrics?.leakageDetected?.toLocaleString() || '0'}
              </p>
              <p className="text-sm text-red-600 mt-2 font-medium">
                {data?.metrics?.leakagePercentage?.toFixed(1) || '0'}% of revenue
              </p>
            </div>
            <div className="w-12 h-12 bg-gradient-to-br from-red-400 to-red-600 rounded-lg flex items-center justify-center">
              <span className="text-2xl">⚠️</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Risk Level</p>
              <p className="text-3xl font-bold text-orange-600 mt-2">
                {data?.metrics?.riskScore || 0}
              </p>
              <p className={`text-sm mt-2 font-medium ${
                data?.metrics?.riskLevel === 'Critical' ? 'text-red-600' :
                data?.metrics?.riskLevel === 'High' ? 'text-orange-600' :
                data?.metrics?.riskLevel === 'Medium' ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {data?.metrics?.riskLevel || 'Low'}
              </p>
            </div>
            <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-orange-600 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📊</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Analyses</p>
              <p className="text-3xl font-bold text-indigo-600 mt-2">
                {data?.metrics?.analysesRun || 0}
              </p>
              <p className="text-sm text-gray-600 mt-2 font-medium">
                {data?.metrics?.totalTransactions?.toLocaleString() || '0'} rows analyzed
              </p>
            </div>
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-400 to-indigo-600 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📈</span>
            </div>
          </div>
        </div>
      </div>

      {/* AI Insight */}
      {data?.aiInsight && (
        <div className={`rounded-xl shadow-lg p-6 border ${
          data.aiInsight.title.includes('Critical') ? 'bg-red-50 border-red-200' :
          data.aiInsight.title.includes('Significant') ? 'bg-orange-50 border-orange-200' :
          data.aiInsight.title.includes('Optimization') ? 'bg-yellow-50 border-yellow-200' :
          'bg-green-50 border-green-200'
        }`}>
          <div className="flex items-start gap-4">
            <div className="text-3xl">
              {data.aiInsight.title.includes('Critical') ? '🚨' :
               data.aiInsight.title.includes('Significant') ? '⚠️' :
               data.aiInsight.title.includes('Optimization') ? '📊' :
               '✅'}
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-bold text-gray-900 mb-2">{data.aiInsight.title}</h3>
              <p className="text-gray-700">{data.aiInsight.message}</p>
            </div>
          </div>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue vs Leakage Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Revenue vs Leakage Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data?.charts?.revenueVsLeakage || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" stroke="#666" />
              <YAxis stroke="#666" />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="revenue" 
                stroke="#10b981" 
                strokeWidth={3} 
                dot={{ fill: '#10b981', r: 5 }} 
                name="Revenue"
              />
              <Line 
                type="monotone" 
                dataKey="leakage" 
                stroke="#ef4444" 
                strokeWidth={3} 
                dot={{ fill: '#ef4444', r: 5 }} 
                name="Leakage"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Category Distribution */}
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Leakage by Category</h3>
          {data?.charts?.leakageByCategory?.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.charts.leakageByCategory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                <Bar dataKey="value" fill="#6366f1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-400">
              <div className="text-center">
                <p className="text-lg">📊</p>
                <p className="mt-2">No data yet - upload a file to see leakage breakdown</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Leakage by Severity */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Leakage by Severity</h3>
        {data?.charts?.leakageBySegment?.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.charts.leakageBySegment} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" stroke="#666" />
              <YAxis type="category" dataKey="name" stroke="#666" />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8b5cf6" radius={[0, 8, 8, 0]}>
                {data.charts.leakageBySegment.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color || '#8b5cf6'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[300px] flex items-center justify-center text-gray-400">
            <div className="text-center">
              <p className="text-lg">📈</p>
              <p className="mt-2">No severity data - upload a file to see issue priorities</p>
            </div>
          </div>
        )}
      </div>

      {/* Recent Alerts */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Recent Alerts</h3>
        <div className="space-y-3">
          {data?.recentAlerts?.length > 0 ? (
            data.recentAlerts.map((alert) => (
              <div key={alert.id} className={`flex items-start gap-3 p-4 rounded-lg border ${
                alert.severity === 'high' ? 'bg-red-50 border-red-200' :
                alert.severity === 'medium' ? 'bg-orange-50 border-orange-200' :
                'bg-blue-50 border-blue-200'
              }`}>
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  alert.severity === 'high' ? 'bg-red-500' :
                  alert.severity === 'medium' ? 'bg-orange-500' :
                  'bg-blue-500'
                }`}>
                  <span className="text-white text-lg">
                    {alert.severity === 'high' ? '🚨' :
                     alert.severity === 'medium' ? '⚠️' :
                     'ℹ️'}
                  </span>
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">{alert.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    {new Date(alert.timestamp).toLocaleString()}
                  </p>
                </div>
                {!alert.isRead && (
                  <div className="w-2 h-2 bg-red-500 rounded-full flex-shrink-0 mt-2"></div>
                )}
              </div>
            ))
          ) : (
            <p className="text-center text-gray-500 py-8">
              No recent alerts - upload data to start analysis
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
