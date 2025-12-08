import { useState, useEffect } from 'react';
import { MdHistory, MdDelete, MdDownload, MdVisibility, MdSearch } from 'react-icons/md';

const AnalysisHistory = () => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    loadAnalysisHistory();
  }, []);

  const loadAnalysisHistory = async () => {
    try {
      setLoading(true);
      // Get from localStorage for now (will be replaced with API call)
      const historyData = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
      setAnalyses(historyData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)));
      setError('');
    } catch (err) {
      setError('Failed to load analysis history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteAnalysis = (id) => {
    if (window.confirm('Are you sure you want to delete this analysis record?')) {
      const updated = analyses.filter(a => a.id !== id);
      setAnalyses(updated);
      localStorage.setItem('analysisHistory', JSON.stringify(updated));
      setSelectedAnalysis(null);
    }
  };

  const downloadAnalysis = (analysis) => {
    const data = JSON.stringify(analysis, null, 2);
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(data));
    element.setAttribute('download', `analysis-${analysis.id}.json`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const clearAllHistory = () => {
    if (window.confirm('Are you sure you want to clear all analysis history? This cannot be undone.')) {
      setAnalyses([]);
      localStorage.setItem('analysisHistory', '[]');
      setSelectedAnalysis(null);
    }
  };

  const filteredAnalyses = analyses.filter(analysis =>
    analysis.filename?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    analysis.uploadId?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-600 font-medium">Loading analysis history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-black flex items-center gap-3">
              <MdHistory className="text-3xl" />
              Analysis History
            </h1>
            <p className="text-gray-600 mt-2">Admin: View and manage all past analysis records</p>
          </div>
          {analyses.length > 0 && (
            <button
              onClick={clearAllHistory}
              className="px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-all duration-300 transform hover:scale-105 active:scale-95"
            >
              <MdDelete className="inline mr-2" />
              Clear All
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 animate-slide-up">
          <p className="text-red-600 font-medium">{error}</p>
        </div>
      )}

      {/* Search Bar */}
      <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
        <div className="relative">
          <MdSearch className="absolute left-4 top-3.5 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by filename or upload ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-black transition-all duration-300"
          />
        </div>
      </div>

      {/* Analysis List */}
      {filteredAnalyses.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-12 text-center">
          <MdHistory className="text-6xl mx-auto text-gray-300 mb-4" />
          <p className="text-gray-600 text-lg font-medium">No analysis history yet</p>
          <p className="text-gray-500 mt-2">Upload files to start building your analysis history</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* List View */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
              <div className="p-4 bg-black text-white font-bold">
                Analysis Records ({filteredAnalyses.length})
              </div>
              <div className="max-h-96 overflow-y-auto">
                {filteredAnalyses.map((analysis) => (
                  <div
                    key={analysis.id}
                    onClick={() => {
                      setSelectedAnalysis(analysis);
                      setShowDetails(true);
                    }}
                    className={`p-4 border-b border-gray-200 cursor-pointer transition-all duration-300 transform hover:bg-gray-50 hover:scale-102 ${
                      selectedAnalysis?.id === analysis.id ? 'bg-gray-100 border-l-4 border-l-black' : ''
                    }`}
                  >
                    <h4 className="font-bold text-black text-sm truncate">{analysis.filename}</h4>
                    <p className="text-xs text-gray-600 mt-1">ID: {analysis.id.slice(0, 8)}...</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(analysis.timestamp).toLocaleDateString()} {new Date(analysis.timestamp).toLocaleTimeString()}
                    </p>
                    {analysis.leakageDetected && (
                      <p className="text-xs text-red-600 font-semibold mt-2">
                        Leakage: ₹{analysis.leakageDetected.toLocaleString()}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Detail View */}
          <div className="lg:col-span-2">
            {selectedAnalysis && showDetails ? (
              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 animate-slide-up">
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-black">{selectedAnalysis.filename}</h2>
                    <p className="text-gray-600 mt-2">
                      Analyzed: {new Date(selectedAnalysis.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <button
                    onClick={() => downloadAnalysis(selectedAnalysis)}
                    className="p-2 bg-black text-white rounded-lg hover:bg-gray-900 transition-all duration-300 transform hover:scale-110"
                    title="Download Analysis"
                  >
                    <MdDownload className="w-5 h-5" />
                  </button>
                </div>

                {/* Analysis Details Grid */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <p className="text-xs text-gray-600 font-semibold">Upload ID</p>
                    <p className="text-sm font-mono text-black mt-1">{selectedAnalysis.uploadId}</p>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <p className="text-xs text-gray-600 font-semibold">Rows Processed</p>
                    <p className="text-sm font-bold text-black mt-1">
                      {selectedAnalysis.rowsCount?.toLocaleString() || 'N/A'}
                    </p>
                  </div>

                  {selectedAnalysis.leakageDetected && (
                    <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                      <p className="text-xs text-red-600 font-semibold">Leakage Detected</p>
                      <p className="text-sm font-bold text-red-600 mt-1">
                        ₹{selectedAnalysis.leakageDetected.toLocaleString()}
                      </p>
                    </div>
                  )}

                  {selectedAnalysis.riskLevel && (
                    <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                      <p className="text-xs text-gray-600 font-semibold">Risk Level</p>
                      <p className={`text-sm font-bold mt-1 ${
                        selectedAnalysis.riskLevel === 'Critical' ? 'text-red-600' :
                        selectedAnalysis.riskLevel === 'High' ? 'text-orange-600' :
                        selectedAnalysis.riskLevel === 'Medium' ? 'text-yellow-600' :
                        'text-green-600'
                      }`}>
                        {selectedAnalysis.riskLevel}
                      </p>
                    </div>
                  )}
                </div>

                {/* Summary */}
                {selectedAnalysis.summary && (
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h3 className="font-bold text-black mb-3">Summary</h3>
                    <div className="text-sm text-gray-700 whitespace-pre-wrap max-h-48 overflow-y-auto">
                      {typeof selectedAnalysis.summary === 'string' ? 
                        selectedAnalysis.summary : 
                        JSON.stringify(selectedAnalysis.summary, null, 2)
                      }
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={() => downloadAnalysis(selectedAnalysis)}
                    className="flex-1 px-4 py-2 bg-black text-white rounded-lg font-semibold hover:bg-gray-900 transition-all duration-300 flex items-center justify-center gap-2"
                  >
                    <MdDownload /> Download
                  </button>
                  <button
                    onClick={() => deleteAnalysis(selectedAnalysis.id)}
                    className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-all duration-300 flex items-center justify-center gap-2"
                  >
                    <MdDelete /> Delete
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-12 text-center">
                <MdVisibility className="text-6xl mx-auto text-gray-300 mb-4" />
                <p className="text-gray-600 text-lg font-medium">Select an analysis to view details</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisHistory;
