import { useState, useEffect } from 'react';
import { getReports, generateReport, downloadReport } from '../services/api';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const data = await getReports();
      setReports(data);
    } catch (error) {
      console.error('Failed to load reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async (category) => {
    setGenerating(true);
    try {
      await generateReport({
        category,
        title: `${category} Report - ${new Date().toLocaleDateString()}`,
      });
      loadReports();
    } catch (error) {
      console.error('Failed to generate report:', error);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (reportId) => {
    try {
      const blob = await downloadReport(reportId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `report-${reportId}.pdf`;
      a.click();
    } catch (error) {
      console.error('Failed to download report:', error);
    }
  };

  const reportTypes = [
    { name: 'Revenue Analysis', category: 'revenue', icon: '💰', color: 'from-green-500 to-green-600' },
    { name: 'Leakage Summary', category: 'leakage', icon: '⚠️', color: 'from-red-500 to-red-600' },
    { name: 'Risk Assessment', category: 'risk', icon: '📊', color: 'from-orange-500 to-orange-600' },
    { name: 'Performance Report', category: 'performance', icon: '📈', color: 'from-blue-500 to-blue-600' },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        <p className="text-gray-600 mt-1">Generate and download revenue analysis reports</p>
      </div>

      {/* Generate Reports */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {reportTypes.map((type) => (
          <button
            key={type.category}
            onClick={() => handleGenerate(type.category)}
            disabled={generating}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all text-left disabled:opacity-50"
          >
            <div className={`w-12 h-12 bg-gradient-to-br ${type.color} rounded-lg flex items-center justify-center mb-4`}>
              <span className="text-2xl">{type.icon}</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">{type.name}</h3>
            <p className="text-sm text-gray-600">Generate {type.category} report</p>
          </button>
        ))}
      </div>

      {/* Recent Reports */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100">
        <div className="p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-900">Recent Reports</h2>
        </div>
        
        <div className="divide-y divide-gray-100">
          {reports.length === 0 ? (
            <div className="p-12 text-center">
              <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">📄</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">No reports yet</h3>
              <p className="text-gray-600">Generate your first report using the options above</p>
            </div>
          ) : (
            reports.map((report) => (
              <div key={report.id} className="p-6 hover:bg-gray-50 transition-all">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-lg flex items-center justify-center">
                      <span className="text-2xl">📄</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900">{report.title}</h3>
                      <p className="text-sm text-gray-600">
                        {report.category} • {new Date(report.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDownload(report.id)}
                    className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
                  >
                    Download PDF
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports;
