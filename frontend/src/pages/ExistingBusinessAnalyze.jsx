import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { analyzeExistingBusiness } from '../services/api'
import { TrendingUp, AlertCircle, DollarSign, Target, Lightbulb, CheckCircle, AlertTriangle, BarChart3 } from 'lucide-react'

const ExistingBusinessAnalyze = () => {
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors } } = useForm()
  const [loading, setLoading] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      const response = await analyzeExistingBusiness(data)
      
      if (response.success) {
        setAnalysisResult(response.analysis)
        toast.success('Analysis completed successfully!')
      } else {
        toast.error('Analysis failed. Please try again.')
      }
    } catch (error) {
      console.error('Analysis error:', error)
      toast.error(error.response?.data?.detail || 'Failed to analyze business')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-black mb-2">Existing Business Analysis</h1>
        <p className="text-gray-600">
          Identify and recover revenue leaks in your current operations
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 bg-white rounded-lg shadow p-6">
        {/* Business Information */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Business Information</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Business Name *</label>
              <input
                {...register('business_name', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="My Business"
              />
              {errors.business_name && <p className="text-red-500 text-sm mt-1">{errors.business_name.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Industry *</label>
              <input
                {...register('industry', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Retail, Manufacturing, Service"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Business Model *</label>
              <select
                {...register('business_model', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="">Select...</option>
                <option value="retail">Retail</option>
                <option value="saas">SaaS</option>
                <option value="service">Service</option>
                <option value="ecommerce">E-commerce</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="subscription">Subscription</option>
                <option value="marketplace">Marketplace</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Data Period (Months) *</label>
              <input
                type="number"
                {...register('data_period_months', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="3"
                defaultValue="3"
              />
            </div>
          </div>
        </div>

        {/* Financial Data */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Financial Data</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Revenue ($) *</label>
              <input
                type="number"
                step="0.01"
                {...register('monthly_revenue', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="100000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Total Sales *</label>
              <input
                type="number"
                {...register('total_sales', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Total Invoices *</label>
              <input
                type="number"
                {...register('total_invoices', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="480"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Total Products *</label>
              <input
                type="number"
                {...register('total_products', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="150"
              />
            </div>
          </div>
        </div>

        {/* Revenue Loss Indicators */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Revenue Loss Indicators</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Refunds Amount ($)</label>
              <input
                type="number"
                step="0.01"
                {...register('refunds_amount')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="5000"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Returns Amount ($)</label>
              <input
                type="number"
                step="0.01"
                {...register('returns_amount')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="3000"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Discounts Given ($)</label>
              <input
                type="number"
                step="0.01"
                {...register('discounts_given')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="12000"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Uncollected Payments ($)</label>
              <input
                type="number"
                step="0.01"
                {...register('uncollected_payments')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="2000"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Inventory Shrinkage ($)</label>
              <input
                type="number"
                step="0.01"
                {...register('inventory_shrinkage')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="4000"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Unrecorded Sales ($)</label>
              <input
                type="number"
                step="0.01"
                {...register('unrecorded_sales')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="1500"
                defaultValue="0"
              />
            </div>
          </div>
        </div>

        {/* Operational Issues */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Operational Issues</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Billing Errors Count</label>
              <input
                type="number"
                {...register('billing_errors_count')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="15"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pricing Inconsistencies</label>
              <input
                type="number"
                {...register('pricing_inconsistencies')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="8"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Low Performing Products</label>
              <input
                type="number"
                {...register('low_performing_products')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="20"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">High Cost Products</label>
              <input
                type="number"
                {...register('high_cost_products')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="10"
                defaultValue="0"
              />
            </div>
          </div>
        </div>

        {/* Systems & Tools */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Systems & Tools</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  {...register('has_automated_billing')}
                  className="w-4 h-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">Automated Billing System</label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  {...register('tracks_inventory')}
                  className="w-4 h-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">Inventory Tracking</label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  {...register('uses_crm')}
                  className="w-4 h-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">CRM System</label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Payment Methods *</label>
              <select
                {...register('payment_methods', { required: 'Required' })}
                multiple
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent h-32"
              >
                <option value="cash">Cash</option>
                <option value="card">Card</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="digital_wallet">Digital Wallet</option>
                <option value="credit">Credit</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">Hold Ctrl/Cmd to select multiple</p>
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-gradient-to-r from-black to-gray-900 text-white py-3 px-6 rounded-lg hover:from-gray-900 hover:to-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors shadow-md"
          >
            {loading ? 'Analyzing...' : 'Analyze Business'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>

      {/* Results Display */}
      {analysisResult && (
        <div className="mt-8 space-y-6">
          <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
            <h2 className="text-2xl font-bold text-black mb-6">Comprehensive Analysis Report</h2>
            
            {/* Executive Summary */}
            <div className="bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-300 rounded-lg p-5 mb-6">
              <h3 className="font-semibold text-black mb-3 flex items-center gap-2">
                <TrendingUp size={20} className="text-black" />
                Executive Summary
              </h3>
              <p className="text-gray-800 leading-relaxed">{analysisResult.executive_summary}</p>
            </div>

            {/* Financial Summary */}
            <div className="bg-white rounded-lg p-5 mb-6 border border-blue-100">
              <h3 className="font-bold text-black mb-4 flex items-center gap-2">
                <DollarSign size={20} className="text-black" />
                Financial Summary
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-5 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-2 mb-2">
                    <DollarSign size={18} className="text-black" />
                    <p className="text-sm text-gray-700 font-medium">Monthly Revenue</p>
                  </div>
                  <p className="text-2xl font-bold text-black">
                    ₹{analysisResult.financial_summary.monthly_revenue.toLocaleString()}
                  </p>
                </div>
                <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-5 rounded-lg border border-gray-400 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertTriangle size={18} className="text-gray-900" />
                    <p className="text-sm text-gray-700 font-medium">Total Loss</p>
                  </div>
                  <p className="text-2xl font-bold text-gray-900">
                    ₹{analysisResult.total_identified_loss.toLocaleString()}
                  </p>
                </div>
                <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-5 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-2 mb-2">
                    <BarChart3 size={18} className="text-black" />
                    <p className="text-sm text-gray-700 font-medium">Loss Percentage</p>
                  </div>
                  <p className="text-2xl font-bold text-black">
                    {analysisResult.financial_summary.loss_percentage.toFixed(1)}%
                  </p>
                </div>
                <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-5 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-2 mb-2">
                    <Target size={18} className="text-black" />
                    <p className="text-sm text-gray-700 font-medium">Risk Level</p>
                  </div>
                  <p className="text-2xl font-bold text-black capitalize">
                    {analysisResult.risk_level}
                  </p>
                </div>
              </div>
            </div>

            {/* AI Insights */}
            {analysisResult.ai_insights && (
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-5 mb-6 border border-gray-300">
                <h3 className="font-bold text-black mb-3 flex items-center gap-2">
                  <TrendingUp size={20} className="text-black" />
                  AI Insights
                </h3>
                <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-line leading-relaxed">
                  {analysisResult.ai_insights}
                </div>
              </div>
            )}

            {/* KPIs */}
            {analysisResult.kpis && (
              <div className="bg-white rounded-lg p-5 mb-6 border border-blue-100">
                <h3 className="font-bold text-black mb-4 flex items-center gap-2">
                  <BarChart3 size={20} className="text-black" />
                  Key Performance Indicators
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {analysisResult.kpis.total_transactions && (
                    <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-lg border border-gray-300">
                      <p className="text-xs text-gray-600 font-medium mb-1">Total Transactions</p>
                      <p className="text-xl font-bold text-black mt-1">
                        {analysisResult.kpis.total_transactions.toLocaleString()}
                      </p>
                    </div>
                  )}
                  {analysisResult.kpis.revenue_per_transaction && (
                    <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-lg border border-gray-300">
                      <p className="text-xs text-gray-600 font-medium mb-1">Revenue per Transaction</p>
                      <p className="text-xl font-bold text-black mt-1">
                        ₹{analysisResult.kpis.revenue_per_transaction.toFixed(2)}
                      </p>
                    </div>
                  )}
                  {analysisResult.kpis.revenue_at_risk && (
                    <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-4 rounded-lg border border-gray-400">
                      <p className="text-xs text-gray-600 font-medium mb-1">Revenue at Risk</p>
                      <p className="text-xl font-bold text-gray-900 mt-1">
                        ₹{analysisResult.kpis.revenue_at_risk.toLocaleString()}
                      </p>
                    </div>
                  )}
                  {analysisResult.kpis.loss_to_revenue_ratio && (
                    <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-4 rounded-lg border border-gray-400">
                      <p className="text-xs text-gray-600 font-medium mb-1">Loss to Revenue Ratio</p>
                      <p className="text-xl font-bold text-gray-900 mt-1">
                        {(analysisResult.kpis.loss_to_revenue_ratio * 100).toFixed(2)}%
                      </p>
                    </div>
                  )}
                  {analysisResult.kpis.average_loss_per_issue && (
                    <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-lg border border-gray-300">
                      <p className="text-xs text-gray-600 font-medium mb-1">Avg Loss per Issue</p>
                      <p className="text-xl font-bold text-black mt-1">
                        ₹{analysisResult.kpis.average_loss_per_issue.toFixed(2)}
                      </p>
                    </div>
                  )}
                  {analysisResult.kpis.recovery_potential && (
                    <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-lg border border-gray-300">
                      <p className="text-xs text-gray-600 font-medium mb-1">Recovery Potential</p>
                      <p className="text-xl font-bold text-black mt-1">
                        ₹{analysisResult.kpis.recovery_potential.toLocaleString()}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {analysisResult.recommendations && analysisResult.recommendations.length > 0 && (
              <div className="bg-white rounded-lg p-5 mb-6 border border-blue-100">
                <h3 className="font-bold text-black mb-4 flex items-center gap-2">
                  <Lightbulb size={20} className="text-black" />
                  Top Recommendations
                </h3>
                <div className="space-y-3">
                  {analysisResult.recommendations.map((rec, index) => (
                    <div key={index} className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-4 border border-gray-300 hover:border-gray-400 transition-colors">
                      <div className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-7 h-7 bg-black text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {index + 1}
                        </span>
                        <p className="text-sm text-gray-800 flex-1 leading-relaxed">{rec}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Leakage Breakdown */}
            {analysisResult.leakage_breakdown && (
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-5 mb-6 border border-gray-300">
                <h3 className="font-semibold text-black mb-4 flex items-center gap-2">
                  <BarChart3 size={20} className="text-black" />
                  Detailed Loss Breakdown by Category
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div className="bg-white p-4 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle size={16} className="text-gray-900" />
                      <p className="text-xs text-gray-600 font-medium">Refunds</p>
                    </div>
                    <p className="text-lg font-bold text-gray-900">₹{analysisResult.leakage_breakdown.refunds.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertCircle size={16} className="text-gray-900" />
                      <p className="text-xs text-gray-600 font-medium">Returns</p>
                    </div>
                    <p className="text-lg font-bold text-gray-900">₹{analysisResult.leakage_breakdown.returns.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <DollarSign size={16} className="text-gray-900" />
                      <p className="text-xs text-gray-600 font-medium">Discounts</p>
                    </div>
                    <p className="text-lg font-bold text-gray-900">₹{analysisResult.leakage_breakdown.discounts.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertCircle size={16} className="text-gray-900" />
                      <p className="text-xs text-gray-600 font-medium">Uncollected</p>
                    </div>
                    <p className="text-lg font-bold text-gray-900">₹{analysisResult.leakage_breakdown.uncollected.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <BarChart3 size={16} className="text-gray-900" />
                      <p className="text-xs text-gray-600 font-medium">Inventory Shrinkage</p>
                    </div>
                    <p className="text-lg font-bold text-gray-900">₹{analysisResult.leakage_breakdown.inventory_shrinkage.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp size={16} className="text-gray-900" />
                      <p className="text-xs text-gray-600 font-medium">Unrecorded Sales</p>
                    </div>
                    <p className="text-lg font-bold text-gray-900">₹{analysisResult.leakage_breakdown.unrecorded_sales.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Top Issues */}
            {analysisResult.top_issues && analysisResult.top_issues.length > 0 && (
              <div className="bg-white rounded-lg p-5 mb-6 border border-red-100">
                <h3 className="font-bold text-black mb-4 flex items-center gap-2">
                  <AlertCircle size={20} className="text-black" />
                  Critical Issues Detected
                </h3>
                <div className="space-y-3">
                  {analysisResult.top_issues.map((issue, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border border-gray-300 hover:border-gray-400 transition-colors">
                      <div className={`flex-shrink-0 p-2 rounded-lg ${ issue.severity === 'high' ? 'bg-black' : 'bg-gray-600'}`}>
                        <AlertTriangle size={20} className="text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-bold text-black">{issue.type || issue.category}</h4>
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            issue.severity === 'high' ? 'bg-black text-white border border-black' :
                            'bg-gray-600 text-white border border-gray-600'
                          }`}>
                            {issue.severity?.toUpperCase() || 'ALERT'}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">{issue.description}</p>
                        {issue.amount > 0 && (
                          <p className="text-sm text-black font-semibold">
                            Impact: ₹{issue.amount.toLocaleString()}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Leakage Points */}
            {analysisResult.leakage_points && analysisResult.leakage_points.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <AlertCircle size={22} className="text-black" />
                  Identified Issues ({analysisResult.leakage_count})
                </h3>
                <div className="space-y-3">
                  {analysisResult.leakage_points.map((point, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-black transition-colors bg-gradient-to-r from-white to-gray-50">
                      <div className="flex justify-between items-start mb-3">
                        <h4 className="font-semibold text-black">{point.category}</h4>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          point.severity === 'high' ? 'bg-black text-white border border-black' :
                          point.severity === 'medium' ? 'bg-gray-600 text-white border border-gray-600' :
                          'bg-gray-400 text-white border border-gray-400'
                        }`}>
                          {point.severity.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-2">{point.description}</p>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3 pt-3 border-t border-gray-200">
                        <p className="text-sm text-gray-600 flex items-center gap-1">
                          <AlertCircle size={14} className="text-black" />
                          <strong>Impact:</strong> {point.impact}
                        </p>
                        <p className="text-sm text-gray-700 flex items-center gap-1">
                          <Lightbulb size={14} className="text-black" />
                          <strong>Recommendation:</strong> {point.recommendation}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recovery Strategies */}
            {analysisResult.recovery_strategies && analysisResult.recovery_strategies.length > 0 && (
              <div>
                <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Lightbulb size={22} className="text-black" />
                  Recovery Strategies
                </h3>
                <div className="space-y-3">
                  {analysisResult.recovery_strategies.map((strategy, index) => (
                    <div key={index} className="border border-gray-300 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <h4 className="font-semibold text-black mb-2 flex items-center gap-2">
                        <CheckCircle size={18} className="text-black" />
                        {strategy.name}
                      </h4>
                      <p className="text-gray-700 mb-3">{strategy.description}</p>
                      <div className="flex flex-wrap gap-4 text-sm">
                        <span className="text-gray-600 bg-white px-3 py-1 rounded-full border border-gray-200">
                          <strong>Impact:</strong> {strategy.impact}
                        </span>
                        <span className="text-gray-600 bg-white px-3 py-1 rounded-full border border-gray-200">
                          <strong>Timeline:</strong> {strategy.timeline}
                        </span>
                        <span className="text-black bg-white px-3 py-1 rounded-full border border-gray-300 font-medium">
                          <strong>Recovery:</strong> {strategy.estimated_recovery}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => setAnalysisResult(null)}
              className="mt-6 w-full py-3 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Run New Analysis
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default ExistingBusinessAnalyze
