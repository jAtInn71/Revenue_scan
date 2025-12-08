import { useState, useCallback } from 'react';
import { uploadFile, getUploads } from '../services/api';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState('');
  const [availableSheets, setAvailableSheets] = useState(null);
  const [selectedSheet, setSelectedSheet] = useState(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  }, []);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const validTypes = ['.csv', '.xlsx', '.xls'];
    const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(fileExtension)) {
      setError('Please upload a CSV or Excel file');
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setFile(selectedFile);
    setError('');
    setUploadResult(null);
    setAvailableSheets(null);
    setSelectedSheet(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError('');

    try {
      console.log('Starting upload for file:', file.name);
      const result = await uploadFile(file, selectedSheet);
      console.log('Upload result:', result);
      
      // Save to analysis history
      const historyEntry = {
        id: result.upload_id || `upload-${Date.now()}`,
        timestamp: new Date().toISOString(),
        filename: file.name,
        uploadId: result.upload_id || 'unknown',
        rowsCount: result.rows_count || 0,
        leakageDetected: result.leakage_summary?.total_amount || 0,
        riskLevel: result.leakage_summary?.risk_level || 'Low',
        selectedSheet: result.selected_sheet,
        summary: result.ai_analysis?.message || 'Analysis completed'
      };

      const existingHistory = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
      existingHistory.push(historyEntry);
      localStorage.setItem('analysisHistory', JSON.stringify(existingHistory));
      
      // If Excel file with multiple sheets, store them for potential re-upload
      if (result.sheet_names && result.sheet_names.length > 1) {
        setAvailableSheets(result.sheet_names);
        setSelectedSheet(result.selected_sheet);
        // Keep file for re-analysis of other sheets
      } else {
        // Single sheet or CSV - clear file after upload
        setFile(null);
        setAvailableSheets(null);
        setSelectedSheet(null);
      }
      
      // Always update result (don't reset it)
      setUploadResult(result);
    } catch (err) {
      console.error('Upload error:', err);
      const errorMessage = err.response?.data?.detail || 
                          err.message || 
                          'Upload failed. Please try again.';
      setError(errorMessage);
      console.error('Full error object:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-black">Upload Data</h1>
        <p className="text-slate-600 mt-2">Upload your revenue data for AI-powered analysis</p>
      </div>

      {/* Upload Area */}
      <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 md:p-8">
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-8 md:p-12 text-center transition-all ${
            isDragging
              ? 'border-brand-accent bg-brand-accent/5'
              : 'border-slate-300 hover:border-brand-accent hover:bg-slate-50'
          }`}
        >
          <div className="flex flex-col items-center gap-4">
            <div className="w-16 h-16 md:w-20 md:h-20 bg-black rounded-full flex items-center justify-center text-brand-accent">
              <span className="text-3xl md:text-4xl">📤</span>
            </div>
            
            <div>
              <h3 className="text-lg md:text-xl font-bold text-black">
                {file ? file.name : 'Drop your file here'}
              </h3>
              <p className="text-slate-600 mt-2 text-sm md:text-base">
                {file ? (
                  <span className="text-green-600 font-medium">
                    ✓ File selected ({(file.size / 1024).toFixed(2)} KB)
                  </span>
                ) : (
                  'or click to browse'
                )}
              </p>
            </div>

            {!file && (
              <label className="cursor-pointer">
                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <span className="px-6 py-3 bg-black text-white rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all inline-block">
                  Choose File
                </span>
              </label>
            )}

            {file && (
              <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                <button
                  onClick={handleUpload}
                  disabled={uploading}
                  className="flex-1 sm:flex-none px-6 py-3 bg-black text-white rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {uploading ? (
                    <span className="flex items-center justify-center gap-2 text-white">
                      <div className="w-5 h-5 border-2 border-brand-accent border-t-transparent rounded-full animate-spin"></div>
                      Uploading...
                    </span>
                  ) : (
                    availableSheets ? 'Re-analyze Sheet' : '✓ Upload File'
                  )}
                </button>
                <button
                  onClick={() => {
                    setFile(null);
                    setAvailableSheets(null);
                    setSelectedSheet(null);
                    setUploadResult(null);
                    setError('');
                  }}
                  className="flex-1 sm:flex-none px-6 py-3 border-2 border-slate-300 text-slate-700 rounded-lg font-semibold hover:bg-slate-50 transition-all"
                >
                  {availableSheets ? 'Clear & Start Over' : 'Cancel'}
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm text-slate-600">
          <div className="flex items-center gap-2">
            <span className="text-green-500 font-bold">✓</span>
            <span>CSV files supported</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-green-500 font-bold">✓</span>
            <span>Excel (.xlsx, .xls)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-green-500 font-bold">✓</span>
            <span>Max size: 10MB</span>
          </div>
        </div>
      </div>

      {/* Sheet Selection for Excel files */}
      {availableSheets && availableSheets.length > 1 && (
        <div className="bg-brand-accent/5 border border-brand-accent rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 bg-brand-accent rounded-lg flex items-center justify-center flex-shrink-0 font-bold text-black">
              <span>📊</span>
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-blue-900 mb-2">Excel Workbook - Multiple Sheets Available</h3>
              <p className="text-blue-700 text-sm mb-4">
                This file contains <span className="font-semibold">{availableSheets.length} sheets</span>. 
                {uploadResult && (
                  <span> Currently viewing: <span className="font-semibold">{uploadResult.selected_sheet}</span></span>
                )}
              </p>
              <div className="flex items-center gap-3 flex-wrap">
                <label className="text-sm font-medium text-blue-900">Switch to Sheet:</label>
                <select
                  value={selectedSheet || ''}
                  onChange={(e) => setSelectedSheet(e.target.value)}
                  className="px-4 py-2 border border-blue-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {availableSheets.map((sheet) => (
                    <option key={sheet} value={sheet}>
                      {sheet}
                    </option>
                  ))}
                </select>
                <button
                  onClick={handleUpload}
                  disabled={uploading || selectedSheet === uploadResult?.selected_sheet}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {uploading ? (
                    <span className="flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Analyzing...
                    </span>
                  ) : (
                    selectedSheet === uploadResult?.selected_sheet ? 'Current Sheet' : 'Analyze This Sheet'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 md:p-6">
          <div className="flex items-start gap-3">
            <div className="text-2xl flex-shrink-0">⚠️</div>
            <div className="flex-1">
              <h3 className="font-bold text-red-900 mb-1">Upload Failed</h3>
              <p className="text-red-700 text-sm">{error}</p>
              <p className="text-red-600 text-xs mt-2">
                💡 Tips: Check that the file format is correct (CSV, XLSX, or XLS), file size is under 10MB, and try again.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Upload Result */}
      {uploadResult && (
        <div className="space-y-4 animate-slide-up">
          <div className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center flex-shrink-0">
                <span className="text-white text-2xl">✓</span>
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-black">Upload Successful!</h3>
                <p className="text-gray-700 mt-2">
                  File ID: <span className="font-mono font-semibold">{uploadResult.upload_id}</span>
                </p>
                <p className="text-green-700 mt-1">
                  Rows Processed: <span className="font-semibold">{uploadResult.rows_count}</span>
                </p>
                {uploadResult.selected_sheet && (
                  <p className="text-green-700 mt-1">
                    Sheet Analyzed: <span className="font-semibold">{uploadResult.selected_sheet}</span>
                    {uploadResult.sheet_names && uploadResult.sheet_names.length > 1 && (
                      <span className="text-sm ml-2">({uploadResult.sheet_names.length} sheets total)</span>
                    )}
                  </p>
                )}
                
                {uploadResult.leakage_summary && (
                  <div className="mt-4 bg-white rounded-lg p-4 border border-green-200">
                    <h4 className="font-bold text-gray-900 mb-3">📊 Leakage Analysis</h4>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Total Leakages</p>
                        <p className="text-2xl font-bold text-red-600">
                          {uploadResult.leakage_summary.total_leakages}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600">Critical</p>
                        <p className="text-2xl font-bold text-red-600">
                          {uploadResult.leakage_summary.critical || 0}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600">Warnings</p>
                        <p className="text-2xl font-bold text-orange-600">
                          {uploadResult.leakage_summary.warnings || 0}
                        </p>
                      </div>
                    </div>

                    {uploadResult.leakage_summary.total_amount > 0 && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-sm text-gray-600">Potential Revenue Impact</p>
                        <p className="text-2xl font-bold text-red-600">
                          ${uploadResult.leakage_summary.total_amount.toLocaleString()}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* AI Analysis */}
          {uploadResult.ai_analysis && (
            <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl p-6">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-2xl">🤖</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">AI Comprehensive Analysis</h3>
                  <p className="text-gray-700 mb-4">{uploadResult.ai_analysis.message}</p>
                  
                  {/* Financial Summary */}
                  {uploadResult.financial_summary && (
                    <div className="bg-white rounded-lg p-4 mb-4 border border-indigo-100">
                      <h4 className="font-bold text-gray-900 mb-3">💰 Financial Summary</h4>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                          <p className="text-xs text-gray-600">Total Revenue</p>
                          <p className="text-lg font-bold text-green-600">
                            ${uploadResult.financial_summary.total_revenue?.toLocaleString() || 0}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Total Costs</p>
                          <p className="text-lg font-bold text-red-600">
                            ${uploadResult.financial_summary.total_costs?.toLocaleString() || 0}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Net Profit</p>
                          <p className="text-lg font-bold text-blue-600">
                            ${uploadResult.financial_summary.net_profit?.toLocaleString() || 0}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Profit Margin</p>
                          <p className="text-lg font-bold text-purple-600">
                            {uploadResult.financial_summary.profit_margin?.toFixed(2) || 0}%
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* AI Insights */}
                  {uploadResult.ai_analysis.ai_insights && (
                    <div className="bg-white rounded-lg p-4 mb-4 border border-indigo-100">
                      <h4 className="font-bold text-gray-900 mb-3">📊 AI Insights</h4>
                      <div className="prose max-w-none text-sm text-gray-700 whitespace-pre-line">
                        {uploadResult.ai_analysis.ai_insights}
                      </div>
                    </div>
                  )}

                  {/* KPIs */}
                  {uploadResult.kpis && (
                    <div className="bg-white rounded-lg p-4 mb-4 border border-indigo-100">
                      <h4 className="font-bold text-gray-900 mb-3">📈 Key Performance Indicators</h4>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        <div>
                          <p className="text-xs text-gray-600">Revenue per Transaction</p>
                          <p className="text-lg font-bold text-indigo-600">
                            ${uploadResult.kpis.revenue_per_transaction?.toFixed(2) || 0}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Total Transactions</p>
                          <p className="text-lg font-bold text-indigo-600">
                            {uploadResult.kpis.total_transactions?.toLocaleString() || 0}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Revenue at Risk</p>
                          <p className="text-lg font-bold text-red-600">
                            ${uploadResult.kpis.revenue_at_risk?.toLocaleString() || 0}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Recommendations */}
                  {uploadResult.ai_analysis.recommendations && uploadResult.ai_analysis.recommendations.length > 0 && (
                    <div className="space-y-3">
                      <h4 className="font-bold text-gray-900">💡 Top Recommendations:</h4>
                      {uploadResult.ai_analysis.recommendations.map((rec, index) => (
                        <div key={index} className="bg-white rounded-lg p-4 border border-indigo-100">
                          <div className="flex items-start gap-2">
                            <span className="flex-shrink-0 w-6 h-6 bg-indigo-600 text-white rounded-full flex items-center justify-center text-xs font-bold">
                              {index + 1}
                            </span>
                            <p className="text-sm text-gray-700 flex-1">{rec}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Top Issues */}
          {uploadResult.leakage_summary?.top_issues && uploadResult.leakage_summary.top_issues.length > 0 && (
            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🔍 Top Issues Detected</h3>
              <div className="space-y-3">
                {uploadResult.leakage_summary.top_issues.map((issue) => (
                  <div key={issue.id} className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                    <span className={`text-2xl ${issue.severity === 'high' ? 'text-red-500' : 'text-orange-500'}`}>
                      {issue.severity === 'high' ? '🚨' : '⚠️'}
                    </span>
                    <div className="flex-1">
                      <h4 className="font-bold text-gray-900">{issue.type}</h4>
                      <p className="text-sm text-gray-600 mt-1">{issue.description}</p>
                      {issue.column && (
                        <p className="text-xs text-indigo-600 mt-1">Column: {issue.column}</p>
                      )}
                      {issue.amount > 0 && (
                        <p className="text-sm text-red-600 font-semibold mt-1">
                          Impact: ${issue.amount.toLocaleString()}
                        </p>
                      )}
                      {issue.affected_rows && (
                        <p className="text-xs text-gray-500 mt-1">
                          Affected Rows: {issue.affected_rows.toLocaleString()}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Column Analysis Summary */}
          {uploadResult.summary?.column_details && (
            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">📋 Complete Column Analysis</h3>
              <p className="text-sm text-gray-600 mb-4">
                Analyzed {uploadResult.total_rows?.toLocaleString()} rows across {uploadResult.total_columns} columns
              </p>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {Object.entries(uploadResult.summary.column_details).map(([colName, details]) => (
                  <div key={colName} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-bold text-gray-900">{colName}</h4>
                      <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded">
                        {details.data_type}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                      {details.sum !== undefined && (
                        <div>
                          <p className="text-gray-600 text-xs">Total Sum</p>
                          <p className="font-semibold text-green-600">
                            ${details.sum?.toLocaleString() || 0}
                          </p>
                        </div>
                      )}
                      {details.mean !== undefined && (
                        <div>
                          <p className="text-gray-600 text-xs">Average</p>
                          <p className="font-semibold text-blue-600">
                            ${details.mean?.toFixed(2) || 0}
                          </p>
                        </div>
                      )}
                      {details.min !== undefined && (
                        <div>
                          <p className="text-gray-600 text-xs">Min → Max</p>
                          <p className="font-semibold text-gray-700">
                            ${details.min?.toFixed(2)} → ${details.max?.toFixed(2)}
                          </p>
                        </div>
                      )}
                      <div>
                        <p className="text-gray-600 text-xs">Missing Values</p>
                        <p className={`font-semibold ${details.null_count > 0 ? 'text-red-600' : 'text-green-600'}`}>
                          {details.null_count} ({details.null_percentage?.toFixed(1)}%)
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 text-xs">Unique Values</p>
                        <p className="font-semibold text-gray-700">{details.unique_values}</p>
                      </div>
                      {details.negative_count !== undefined && details.negative_count > 0 && (
                        <div>
                          <p className="text-gray-600 text-xs">Negative Values</p>
                          <p className="font-semibold text-red-600">{details.negative_count}</p>
                        </div>
                      )}
                      {details.zero_count !== undefined && details.zero_count > 0 && (
                        <div>
                          <p className="text-gray-600 text-xs">Zero Values</p>
                          <p className="font-semibold text-orange-600">{details.zero_count}</p>
                        </div>
                      )}
                    </div>

                    {details.top_values && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-xs text-gray-600 mb-2">Top Values:</p>
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(details.top_values).slice(0, 5).map(([val, count]) => (
                            <span key={val} className="text-xs bg-gray-100 px-2 py-1 rounded">
                              {val}: {count}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-100">
        <h3 className="text-lg font-bold text-gray-900 mb-4">📋 Upload Instructions</h3>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start gap-2">
            <span className="text-indigo-600 font-bold">1.</span>
            <span>Prepare your revenue data in CSV or Excel format</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-indigo-600 font-bold">2.</span>
            <span>Include columns like: revenue, date, customer, product, amount</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-indigo-600 font-bold">3.</span>
            <span>Drag and drop your file or click to browse</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-indigo-600 font-bold">4.</span>
            <span>Our AI will automatically analyze and detect potential leakages</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Upload;
