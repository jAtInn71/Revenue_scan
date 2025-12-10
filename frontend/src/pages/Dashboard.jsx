import { useState, useEffect } from 'react';
import { getDashboardData } from '../services/api';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { MdAttachMoney, MdWarning, MdAnalytics, MdTrendingUp } from 'react-icons/md';
import { IoAlertCircle, IoCheckmarkCircle } from 'react-icons/io5';
import { HiLightBulb } from 'react-icons/hi';
import { BiSolidBarChartAlt2 } from 'react-icons/bi';

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

  // Create summary metrics for quick view and graphs
  const metrics = {
    totalRevenue: data?.metrics?.totalRevenue || 0,
    leakageDetected: data?.metrics?.leakageDetected || 0,
    riskScore: data?.metrics?.riskScore || 0,
    analysesRun: data?.metrics?.analysesRun || 0,
    netProfit: data?.metrics?.netProfit || 0,
  };

  // Get chart data from backend (only if available)
  const hasChartData = data?.charts && (
    (data.charts.revenueVsLeakage && data.charts.revenueVsLeakage.length > 0) ||
    (data.charts.leakageByCategory && data.charts.leakageByCategory.length > 0) ||
    (data.charts.leakageBySegment && data.charts.leakageBySegment.length > 0)
  );

  // Revenue vs Leakage Trend (from uploaded data)
  const revenueTrendData = data?.charts?.revenueVsLeakage || [];

  // Leakage by Category (from uploaded data)
  const leakageCategoryData = data?.charts?.leakageByCategory || [];

  // Leakage by Severity/Segment (from uploaded data)
  const leakageSeverityData = data?.charts?.leakageBySegment || [];

  // Create metrics comparison data for bar chart (always show)
  const metricsComparisonData = [
    { name: 'Total Revenue', value: metrics.totalRevenue, color: '#000000' },
    { name: 'Net Profit', value: metrics.netProfit, color: '#404040' },
    { name: 'Leakage', value: metrics.leakageDetected, color: '#DC2626' },
  ];

  // Create risk and analyses data for dual axis chart (always show)
  const performanceData = [
    { metric: 'Risk Score', value: metrics.riskScore, max: 100 },
    { metric: 'Analyses', value: metrics.analysesRun, max: metrics.analysesRun > 0 ? metrics.analysesRun : 10 },
  ];

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
            <div className="flex-1 min-w-0 pr-2">
              <p className="text-sm font-medium text-gray-600 mb-2">Total Revenue</p>
              <p className="text-lg md:text-xl lg:text-2xl font-bold text-black truncate" title={`₹${data?.metrics?.totalRevenue?.toLocaleString() || '0'}`}>
                ₹{data?.metrics?.totalRevenue?.toLocaleString() || '0'}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-black rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdAttachMoney className="text-white text-xl md:text-2xl" />
            </div>
          </div>
          <p className="text-xs md:text-sm text-gray-600 truncate" title={`Net Profit: ₹${data?.metrics?.netProfit?.toLocaleString() || '0'} (${data?.metrics?.profitMargin?.toFixed(1) || '0'}%)`}>
            Net Profit: ₹{data?.metrics?.netProfit?.toLocaleString() || '0'} ({data?.metrics?.profitMargin?.toFixed(1) || '0'}%)
          </p>
        </div>

        {/* Revenue Leakage */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1 min-w-0 pr-2">
              <p className="text-sm font-medium text-gray-600 mb-2">Revenue Leakage</p>
              <p className="text-lg md:text-xl lg:text-2xl font-bold text-red-600 truncate" title={`₹${data?.metrics?.leakageDetected?.toLocaleString() || '0'}`}>
                ₹{data?.metrics?.leakageDetected?.toLocaleString() || '0'}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-red-600 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdWarning className="text-white text-xl md:text-2xl" />
            </div>
          </div>
          <p className="text-xs md:text-sm font-medium text-red-600 truncate" title={`${data?.metrics?.leakagePercentage?.toFixed(1) || '0'}% of revenue`}>
            {data?.metrics?.leakagePercentage?.toFixed(1) || '0'}% of revenue
          </p>
        </div>

        {/* Risk Level */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1 min-w-0 pr-2">
              <p className="text-sm font-medium text-gray-600 mb-2">Risk Level</p>
              <p className="text-lg md:text-xl lg:text-2xl font-bold text-black truncate" title={String(data?.metrics?.riskScore || 0)}>
                {data?.metrics?.riskScore || 0}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdAnalytics className="text-white text-xl md:text-2xl" />
            </div>
          </div>
          <p className={`text-xs md:text-sm font-medium truncate ${
            data?.metrics?.riskLevel === 'Critical' ? 'text-red-600' :
            data?.metrics?.riskLevel === 'High' ? 'text-orange-600' :
            data?.metrics?.riskLevel === 'Medium' ? 'text-yellow-600' :
            'text-green-600'
          }`} title={data?.metrics?.riskLevel || 'Low'}>
            {data?.metrics?.riskLevel || 'Low'}
          </p>
        </div>

        {/* Total Analyses */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 md:p-6 hover:shadow-lg hover:border-gray-300 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1 min-w-0 pr-2">
              <p className="text-sm font-medium text-gray-600 mb-2">Total Analyses</p>
              <p className="text-lg md:text-xl lg:text-2xl font-bold text-black truncate" title={String(data?.metrics?.analysesRun || 0)}>
                {data?.metrics?.analysesRun || 0}
              </p>
            </div>
            <div className="w-10 h-10 md:w-12 md:h-12 bg-black rounded-lg flex items-center justify-center text-white flex-shrink-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <MdTrendingUp className="text-xl md:text-2xl" />
            </div>
          </div>
          <p className="text-xs md:text-sm text-gray-600 truncate" title={`${data?.metrics?.totalTransactions?.toLocaleString() || '0'} rows analyzed`}>
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
            <div className="flex-shrink-0">
              {data.aiInsight.title.includes('Critical') ? (
                <MdWarning className="w-10 h-10 text-red-600" />
              ) : data.aiInsight.title.includes('Significant') ? (
                <IoAlertCircle className="w-10 h-10 text-orange-600" />
              ) : data.aiInsight.title.includes('Optimization') ? (
                <HiLightBulb className="w-10 h-10 text-gray-600" />
              ) : (
                <IoCheckmarkCircle className="w-10 h-10 text-green-600" />
              )}
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
        {/* Metrics Overview Bar Chart - Always show */}
        <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
          <h3 className="text-lg font-bold text-black mb-4">Financial Metrics Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={metricsComparisonData} barSize={40}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis dataKey="name" stroke="#000000" style={{ fontSize: '12px', fontWeight: '500' }} />
              <YAxis stroke="#000000" tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}K`} style={{ fontSize: '12px', fontWeight: '500' }} />
              <Tooltip 
                formatter={(value) => `₹${value.toLocaleString()}`}
                contentStyle={{ backgroundColor: '#000000', color: '#ffffff', border: 'none', borderRadius: '8px', fontWeight: '500' }}
                labelStyle={{ color: '#ffffff', fontWeight: 'bold' }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {metricsComparisonData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk & Performance Chart - Always show */}
        <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
          <h3 className="text-lg font-bold text-black mb-4">Risk & Performance Metrics</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={performanceData} layout="vertical" barSize={30}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis type="number" stroke="#000000" style={{ fontSize: '12px', fontWeight: '500' }} />
              <YAxis type="category" dataKey="metric" stroke="#000000" style={{ fontSize: '12px', fontWeight: '500' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#000000', color: '#ffffff', border: 'none', borderRadius: '8px', fontWeight: '500' }}
                labelStyle={{ color: '#ffffff', fontWeight: 'bold' }}
              />
              <Bar dataKey="value" fill="#000000" radius={[0, 8, 8, 0]}>
                {performanceData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? '#DC2626' : '#000000'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Revenue vs Leakage Trend - Only show if data available */}
        {revenueTrendData.length > 0 && (
          <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
            <h3 className="text-lg font-bold text-black mb-4">Revenue vs Leakage Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
                <XAxis dataKey="month" stroke="#000000" style={{ fontSize: '12px', fontWeight: '500' }} />
                <YAxis stroke="#000000" tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}K`} style={{ fontSize: '12px', fontWeight: '500' }} />
                <Tooltip 
                  formatter={(value) => `₹${value.toLocaleString()}`}
                  contentStyle={{ backgroundColor: '#000000', color: '#ffffff', border: 'none', borderRadius: '8px', fontWeight: '500' }}
                  labelStyle={{ color: '#ffffff', fontWeight: 'bold' }}
                />
                <Legend wrapperStyle={{ color: '#000000', fontWeight: '500' }} />
                <Line 
                  type="monotone" 
                  dataKey="revenue" 
                  stroke="#000000" 
                  strokeWidth={3} 
                  dot={{ fill: '#000000', r: 6, strokeWidth: 2, stroke: '#ffffff' }} 
                  name="Revenue"
                />
                <Line 
                  type="monotone" 
                  dataKey="leakage" 
                  stroke="#DC2626" 
                  strokeWidth={3} 
                  dot={{ fill: '#DC2626', r: 6, strokeWidth: 2, stroke: '#ffffff' }} 
                  name="Leakage"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Leakage by Category - Only show if data available */}
        {leakageCategoryData.length > 0 && (
          <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
            <h3 className="text-lg font-bold text-black mb-4">Leakage by Category</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={leakageCategoryData} barSize={40}>
                <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
                <XAxis dataKey="name" stroke="#000000" style={{ fontSize: '12px', fontWeight: '500' }} />
                <YAxis stroke="#000000" tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}K`} style={{ fontSize: '12px', fontWeight: '500' }} />
                <Tooltip 
                  formatter={(value) => `₹${value.toLocaleString()}`}
                  contentStyle={{ backgroundColor: '#000000', color: '#ffffff', border: 'none', borderRadius: '8px', fontWeight: '500' }}
                  labelStyle={{ color: '#ffffff', fontWeight: 'bold' }}
                />
                <Bar dataKey="value" fill="#DC2626" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Leakage by Severity - Only show if data available */}
        {leakageSeverityData.length > 0 && (
          <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 animate-slide-up">
            <h3 className="text-lg font-bold text-black mb-4">Leakage Distribution by Severity</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={leakageSeverityData}
                  cx="50%"
                  cy="50%"
                  labelLine={true}
                  label={(entry) => `${entry.name}: ${entry.value}`}
                  outerRadius={90}
                  innerRadius={0}
                  fill="#000000"
                  dataKey="value"
                  strokeWidth={2}
                  stroke="#ffffff"
                >
                  {leakageSeverityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => `${value} issues`}
                  contentStyle={{ backgroundColor: '#eeeeeeff', color: '#ffffff', border: 'none', borderRadius: '8px', fontWeight: '500' }}
                  labelStyle={{ color: '#ffffffff', fontWeight: 'bold' }}
                />
                <Legend wrapperStyle={{ color: '#000000', fontWeight: '500' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* No Data Message */}
      {!hasChartData && hasData && (
        <div className="bg-gray-50 rounded-xl border-2 border-dashed border-gray-300 p-8 text-center animate-slide-up">
          <BiSolidBarChartAlt2 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-black mb-2">No Chart Data Available</h3>
          <p className="text-gray-600">
            Upload more data files to generate detailed trend and category charts.
          </p>
        </div>
      )}

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
