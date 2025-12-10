import { useState, useEffect } from 'react';
import { getReports, generateReport, downloadReport } from '../services/api';
import { MdAttachMoney, MdWarning, MdAssessment, MdTrendingUp, MdDescription } from 'react-icons/md';

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
    { name: 'Revenue Analysis', category: 'revenue', IconComponent: MdAttachMoney, color: 'bg-green-500' },
    { name: 'Leakage Summary', category: 'leakage', IconComponent: MdWarning, color: 'bg-red-500' },
    { name: 'Risk Assessment', category: 'risk', IconComponent: MdAssessment, color: 'bg-brand-accent' },
    { name: 'Performance Report', category: 'performance', IconComponent: MdTrendingUp, color: 'bg-blue-500' },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-12 h-12 border-4 border-brand-accent border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-black">Reports</h1>
        <p className="text-slate-600 mt-2">Generate and download revenue analysis reports</p>
      </div>

      {/* Generate Reports */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {reportTypes.map((type) => (
          <button
            key={type.category}
            onClick={() => handleGenerate(type.category)}
            disabled={generating}
            className="bg-white rounded-xl shadow-md border border-slate-200 p-6 hover:shadow-lg card-hover text-left disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <div className={`w-12 h-12 ${type.color} rounded-lg flex items-center justify-center mb-4 text-white`}>
              <type.IconComponent className="w-7 h-7" />
            </div>
            <h3 className="text-base sm:text-lg font-bold text-black mb-2">{type.name}</h3>
            <p className="text-xs sm:text-sm text-slate-600">Generate {type.category} report</p>
          </button>
        ))}
      </div>

      {/* Recent Reports */}
      <div className="bg-white rounded-xl shadow-md border border-slate-200">
        <div className="p-6 border-b border-slate-100">
          <h2 className="text-lg sm:text-xl font-bold text-black">Recent Reports</h2>
        </div>
        
        <div className="divide-y divide-slate-100">
          {reports.length === 0 ? (
            <div className="p-8 sm:p-12 text-center">
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MdDescription className="w-10 h-10 sm:w-12 sm:h-12 text-slate-400" />
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-black mb-2">No reports yet</h3>
              <p className="text-slate-600 text-sm sm:text-base">Generate your first report using the options above</p>
            </div>
          ) : (
            reports.map((report) => (
              <div key={report.id} className="p-4 sm:p-6 hover:bg-slate-50 transition-all">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="flex items-start sm:items-center gap-3 sm:gap-4 min-w-0 flex-1">
                  <div className="w-10 h-10 sm:w-12 sm:h-12 bg-black rounded-lg flex items-center justify-center flex-shrink-0 text-brand-accent">
                    <MdDescription className="w-6 h-6 sm:w-7 sm:h-7" />
                  </div>
                    <div className="min-w-0">
                      <h3 className="font-bold text-slate-900 truncate">{report.title}</h3>
                      <p className="text-xs sm:text-sm text-slate-600 mt-1">
                        {report.category} • {new Date(report.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDownload(report.id)}
                    className="w-full sm:w-auto px-4 py-2 bg-black text-brand-accent rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all text-sm"
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
