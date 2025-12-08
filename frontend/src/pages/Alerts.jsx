import { useState, useEffect } from 'react';
import { getAlerts, createAlert, updateAlert, deleteAlert } from '../services/api';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newAlert, setNewAlert] = useState({
    metric: '',
    condition: 'greater_than',
    threshold: '',
    severity: 'medium',
  });

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const data = await getAlerts();
      setAlerts(data);
    } catch (error) {
      console.error('Failed to load alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await createAlert({
        ...newAlert,
        threshold: parseFloat(newAlert.threshold),
      });
      setShowCreateModal(false);
      setNewAlert({ metric: '', condition: 'greater_than', threshold: '', severity: 'medium' });
      loadAlerts();
    } catch (error) {
      console.error('Failed to create alert:', error);
    }
  };

  const handleToggle = async (alertId, isActive) => {
    try {
      await updateAlert(alertId, { is_active: !isActive });
      loadAlerts();
    } catch (error) {
      console.error('Failed to update alert:', error);
    }
  };

  const handleDelete = async (alertId) => {
    if (!confirm('Are you sure you want to delete this alert?')) return;
    
    try {
      await deleteAlert(alertId);
      loadAlerts();
    } catch (error) {
      console.error('Failed to delete alert:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-slate-500';
    }
  };

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
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-black">Alerts</h1>
          <p className="text-slate-600 mt-2">Manage your revenue leakage alerts</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="w-full sm:w-auto px-6 py-3 bg-black text-brand-accent rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all"
        >
          + Create Alert
        </button>
      </div>

      {/* Alerts List */}
      <div className="grid gap-4">
        {alerts.length === 0 ? (
          <div className="bg-white rounded-xl shadow-md border border-slate-200 p-8 sm:p-12 text-center">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl sm:text-4xl">🔔</span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-black mb-2">No alerts configured</h3>
            <p className="text-slate-600 mb-6 text-sm sm:text-base">Create your first alert to get notified about revenue issues</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="px-6 py-3 bg-black text-brand-accent rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all inline-block"
            >
              Create First Alert
            </button>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-white rounded-xl shadow-md border border-slate-200 p-6 hover:shadow-lg card-hover"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-start gap-3">
                    <div className={`w-10 h-10 sm:w-12 sm:h-12 ${getSeverityColor(alert.severity)} rounded-lg flex items-center justify-center flex-shrink-0 text-white font-bold`}>
                      ⚠
                    </div>
                    <div className="min-w-0">
                      <h3 className="text-base sm:text-lg font-bold text-black truncate">{alert.metric}</h3>
                      <p className="text-xs sm:text-sm text-slate-600 mt-1">
                        Alert when {alert.condition.replace('_', ' ')} {alert.threshold}
                      </p>
                    </div>
                  </div>
                  
                  <div className="mt-3 flex flex-wrap gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-semibold ${
                      alert.severity === 'critical' ? 'bg-red-100 text-red-700' :
                      alert.severity === 'high' ? 'bg-orange-100 text-orange-700' :
                      alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {alert.severity.toUpperCase()}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-semibold ${
                      alert.is_active ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-700'
                    }`}>
                      {alert.is_active ? '● Active' : '○ Inactive'}
                    </span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
                  <button
                    onClick={() => handleToggle(alert.id, alert.is_active)}
                    className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                      alert.is_active
                        ? 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    }`}
                  >
                    {alert.is_active ? 'Disable' : 'Enable'}
                  </button>
                  <button
                    onClick={() => handleDelete(alert.id)}
                    className="px-4 py-2 bg-red-50 text-red-600 rounded-lg font-medium hover:bg-red-100 transition-all text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Create Alert Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
            <h3 className="text-2xl font-bold text-black mb-6">Create New Alert</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-900 mb-2">Metric</label>
                <input
                  type="text"
                  value={newAlert.metric}
                  onChange={(e) => setNewAlert({ ...newAlert, metric: e.target.value })}
                  placeholder="e.g., Revenue Leakage"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-900 mb-2">Condition</label>
                <select
                  value={newAlert.condition}
                  onChange={(e) => setNewAlert({ ...newAlert, condition: e.target.value })}
                  className="input-field"
                >
                  <option value="greater_than">Greater Than</option>
                  <option value="less_than">Less Than</option>
                  <option value="equals">Equals</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-900 mb-2">Threshold</label>
                <input
                  type="number"
                  value={newAlert.threshold}
                  onChange={(e) => setNewAlert({ ...newAlert, threshold: e.target.value })}
                  placeholder="e.g., 10000"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-900 mb-2">Severity</label>
                <select
                  value={newAlert.severity}
                  onChange={(e) => setNewAlert({ ...newAlert, severity: e.target.value })}
                  className="input-field"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 mt-6">
              <button
                onClick={handleCreate}
                className="flex-1 px-6 py-3 bg-black text-brand-accent rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all"
              >
                Create Alert
              </button>
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 px-6 py-3 border-2 border-slate-300 text-slate-700 rounded-lg font-semibold hover:bg-slate-50 transition-all"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Alerts;
