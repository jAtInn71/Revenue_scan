import { useState, useEffect } from 'react';
import { getDashboardData } from '../services/api';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { MdAttachMoney, MdWarning, MdAnalytics, MdTrendingUp } from 'react-icons/md';

// Sample data for initial display
const SAMPLE_REVENUE_TREND = [
  { month: 'Jan', revenue: 0, target: 50000 },
  { month: 'Feb', revenue: 0, target: 50000 },
  { month: 'Mar', revenue: 0, target: 50000 },
  { month: 'Apr', revenue: 0, target: 50000 },
  { month: 'May', revenue: 0, target: 50000 },
  { month: 'Jun', revenue: 0, target: 50000 },
];

const SAMPLE_CATEGORY_DATA = [
  { name: 'Product A', value: 0, percentage: 0 },
  { name: 'Product B', value: 0, percentage: 0 },
  { name: 'Product C', value: 0, percentage: 0 },
  { name: 'Product D', value: 0, percentage: 0 },
];

const SAMPLE_LEAKAGE_DATA = [
  { category: 'Discounts', amount: 0 },
  { category: 'Returns', amount: 0 },
  { category: 'Errors', amount: 0 },
  { category: 'Fraud', amount: 0 },
];

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasData, setHasData] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const dashboardData = await getDashboardData();
      if (dashboardData && Object.keys(dashboardData).length > 0) {
        setData(dashboardData);
        setHasData(true);
        setError('');
      } else {
        setData(null);
        setHasData(false);
      }
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setData(null);
      setHasData(false);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    // Save current analysis to history before clearing
    if (data && hasData) {
      const historyEntry = {
        id: `analysis-${Date.now()}`,
        timestamp: new Date().toISOString(),
        filename: 'Dashboard Analysis',
        uploadId: data.upload_id || 'unknown',
        rowsCount: data.metrics?.totalTransactions || 0,
        leakageDetected: data.metrics?.leakageDetected || 0,
        riskLevel: data.metrics?.riskLevel || 'Unknown',
        summary: {
          totalRevenue: data.metrics?.totalRevenue,
          netProfit: data.metrics?.netProfit,
          profitMargin: data.metrics?.profitMargin,
          analysesRun: data.metrics?.analysesRun,
        }
      };

      // Save to localStorage history
      const existingHistory = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
      existingHistory.push(historyEntry);
      localStorage.setItem('analysisHistory', JSON.stringify(existingHistory));
    }

    // Clear data and reload fresh
    setData(null);
    setHasData(false);
    setLoading(true);
    setError('');
    await loadDashboard();
  };

  const COLORS = ['#000000', '#404040', '#808080', '#c0c0c0'];

  // Get chart data - use real data if available, otherwise use sample data
  const revenueTrendData = data?.metrics?.revenueTrend || SAMPLE_REVENUE_TREND;
  const categoryData = data?.metrics?.categoryBreakdown || SAMPLE_CATEGORY_DATA;
  const leakageData = data?.metrics?.leakageByCategory || SAMPLE_LEAKAGE_DATA;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-black">Dashboard</h1>
            <p className="text-gray-600 mt-2">Overview of your revenue analytics {!hasData && '(Sample Data - Upload to see real data)'}</p>
          </div>
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="px-6 py-3 bg-black text-white rounded-lg font-semibold hover:bg-gray-900 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <svg className={`w-5 h-5 transition-transform duration-300 ${loading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {hasData ? 'Refresh & Save' : 'Refresh'}
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {/* Total Revenue */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">Total Revenue</p>
              <p className="text-2xl md:text-3xl font-bold text-black">
                ${data?.metrics?.totalRevenue?.toLocaleString() || '0'}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-black rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdAttachMoney className="text-white text-xl md:text-2xl" />
            </div>
          </div>
          <p className="text-xs md:text-sm text-gray-600">
            Net Profit: ${data?.metrics?.netProfit?.toLocaleString() || '0'} ({data?.metrics?.profitMargin?.toFixed(1) || '0'}%)
          </p>
        </div>

        {/* Revenue Leakage */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">Revenue Leakage</p>
              <p className="text-2xl md:text-3xl font-bold text-red-600">
                ${data?.metrics?.leakageDetected?.toLocaleString() || '0'}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-red-600 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdWarning className="text-white text-xl md:text-2xl" />
            </div>
          </div>
          <p className="text-xs md:text-sm font-medium text-red-600">
            {data?.metrics?.leakagePercentage?.toFixed(1) || '0'}% of revenue
          </p>
        </div>

        {/* Risk Level */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">Risk Level</p>
              <p className="text-2xl md:text-3xl font-bold text-black">
                {data?.metrics?.riskScore || 0}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdAnalytics className="text-white text-xl md:text-2xl" />
            </div>
          </div>
          <p className={`text-xs md:text-sm font-medium ${
            data?.metrics?.riskLevel === 'Critical' ? 'text-red-600' :
            data?.metrics?.riskLevel === 'High' ? 'text-orange-600' :
            data?.metrics?.riskLevel === 'Medium' ? 'text-yellow-600' :
            'text-green-600'
          }`}>
            {data?.metrics?.riskLevel || 'Low'}
          </p>
        </div>

        {/* Total Analyses */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">Total Analyses</p>
              <p className="text-2xl md:text-3xl font-bold text-black">
                {data?.metrics?.analysesRun || 0}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-black rounded-lg flex items-center justify-center text-white flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdTrendingUp className="text-xl md:text-2xl" />
            </div>
          </div>
          <p className="text-xs md:text-sm text-gray-600">
            {data?.metrics?.totalTransactions?.toLocaleString() || '0'} rows analyzed
          </p>
        </div>
      </div>

      {/* AI Insight */}
      {data?.aiInsight && (
        <div className={`rounded-xl shadow-md p-6 border transition-all duration-300 animate-slide-up ${
          data.aiInsight.title.includes('Critical') ? 'bg-red-50 border-red-200' :
          data.aiInsight.title.includes('Significant') ? 'bg-orange-50 border-orange-200' :
          data.aiInsight.title.includes('Optimization') ? 'bg-gray-50 border-gray-200' :
          'bg-green-50 border-green-200'
        }`}>
          <div className="flex items-start gap-4">
            <div className="text-3xl flex-shrink-0">
              {data.aiInsight.title.includes('Critical') ? '🚨' :
               data.aiInsight.title.includes('Significant') ? '⚠️' :
               data.aiInsight.title.includes('Optimization') ? '💡' :
               '✅'}
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-bold text-black mb-2">{data.aiInsight.title}</h3>
              <p className="text-gray-700">{data.aiInsight.message}</p>
            </div>
          </div>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Trend Chart */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
          <h3 className="text-lg font-bold text-black mb-4">Revenue Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
              <XAxis dataKey="month" stroke="#808080" />
              <YAxis stroke="#808080" />
              <Tooltip 
                formatter={(value) => `$${value.toLocaleString()}`}
                contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e5e5', borderRadius: '8px' }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="revenue" 
                stroke="#000000" 
                strokeWidth={3} 
                dot={{ fill: '#000000', r: 5 }} 
                name="Actual Revenue"
              />
              <Line 
                type="monotone" 
                dataKey="target" 
                stroke="#808080" 
                strokeWidth={2} 
                strokeDasharray="5 5"
                dot={{ fill: '#808080', r: 4 }} 
                name="Target"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Leakage by Category Chart */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
          <h3 className="text-lg font-bold text-black mb-4">Leakage by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={leakageData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
              <XAxis dataKey="category" stroke="#808080" />
              <YAxis stroke="#808080" />
              <Tooltip 
                formatter={(value) => `$${value.toLocaleString()}`}
                contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e5e5', borderRadius: '8px' }}
              />
              <Bar dataKey="amount" fill="#000000" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Category Distribution Pie Chart */}
      <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
        <h3 className="text-lg font-bold text-black mb-4">Revenue Distribution by Category</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={categoryData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${entry.percentage}%`}
              outerRadius={100}
              fill="#000000"
              dataKey="value"
            >
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value) => `$${value.toLocaleString()}`}
              contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e5e5', borderRadius: '8px' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Alerts - Only show if there's data */}
      {hasData && data?.recentAlerts && data.recentAlerts.length > 0 && (
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
          <h3 className="text-lg font-bold text-black mb-4">Recent Alerts</h3>
          <div className="space-y-3">
            {data.recentAlerts.map((alert) => (
              <div key={alert.id} className={`flex items-start gap-3 p-4 rounded-lg border transition-all duration-300 transform hover:scale-102 hover:shadow-md ${
                alert.severity === 'high' ? 'bg-red-50 border-red-200 hover:border-red-300' :
                alert.severity === 'medium' ? 'bg-orange-50 border-orange-200 hover:border-orange-300' :
                'bg-gray-50 border-gray-200 hover:border-gray-300'
              }`}>
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 font-bold text-white ${
                  alert.severity === 'high' ? 'bg-red-500' :
                  alert.severity === 'medium' ? 'bg-orange-500' :
                  'bg-black'
                }`}>
                  {alert.severity === 'high' ? '!' :
                   alert.severity === 'medium' ? '⚠' :
                   'i'}
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="font-semibold text-black">{alert.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    {new Date(alert.timestamp).toLocaleString()}
                  </p>
                </div>
                {!alert.isRead && (
                  <div className="w-2 h-2 bg-red-500 rounded-full flex-shrink-0 mt-2 animate-pulse-slow"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
