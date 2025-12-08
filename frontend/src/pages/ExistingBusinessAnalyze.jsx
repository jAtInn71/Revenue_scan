import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { analyzeExistingBusiness } from '../services/api'

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
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Existing Business Analysis</h1>
        <p className="text-gray-600">
          Identify and recover revenue leaks in your current operations
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 bg-white rounded-lg shadow p-6">
        {/* Business Information */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-green-600 border-b pb-2">Business Information</h2>
          
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
          <h2 className="text-xl font-semibold text-green-600 border-b pb-2">Financial Data</h2>
          
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
          <h2 className="text-xl font-semibold text-green-600 border-b pb-2">Revenue Loss Indicators</h2>
          
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
          <h2 className="text-xl font-semibold text-green-600 border-b pb-2">Operational Issues</h2>
          
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
          <h2 className="text-xl font-semibold text-green-600 border-b pb-2">Systems & Tools</h2>
          
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
            className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors"
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
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Results</h2>
            
            {/* Executive Summary */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-green-900 mb-2">Executive Summary</h3>
              <p className="text-green-800">{analysisResult.executive_summary}</p>
            </div>

            {/* Financial Summary */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-blue-600 mb-1">Monthly Revenue</p>
                <p className="text-2xl font-bold text-blue-900">
                  ${analysisResult.financial_summary.monthly_revenue.toLocaleString()}
                </p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-sm text-red-600 mb-1">Total Loss</p>
                <p className="text-2xl font-bold text-red-900">
                  ${analysisResult.total_identified_loss.toLocaleString()}
                </p>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <p className="text-sm text-yellow-600 mb-1">Loss %</p>
                <p className="text-2xl font-bold text-yellow-900">
                  {analysisResult.financial_summary.loss_percentage.toFixed(1)}%
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-purple-600 mb-1">Risk Level</p>
                <p className="text-2xl font-bold text-purple-900 capitalize">
                  {analysisResult.risk_level}
                </p>
              </div>
            </div>

            {/* Leakage Breakdown */}
            {analysisResult.leakage_breakdown && (
              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Loss Breakdown</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600">Refunds</p>
                    <p className="text-lg font-bold text-red-600">${analysisResult.leakage_breakdown.refunds.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600">Returns</p>
                    <p className="text-lg font-bold text-orange-600">${analysisResult.leakage_breakdown.returns.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600">Discounts</p>
                    <p className="text-lg font-bold text-yellow-600">${analysisResult.leakage_breakdown.discounts.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600">Uncollected</p>
                    <p className="text-lg font-bold text-purple-600">${analysisResult.leakage_breakdown.uncollected.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600">Inventory Shrinkage</p>
                    <p className="text-lg font-bold text-pink-600">${analysisResult.leakage_breakdown.inventory_shrinkage.toLocaleString()}</p>
                  </div>
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600">Unrecorded Sales</p>
                    <p className="text-lg font-bold text-indigo-600">${analysisResult.leakage_breakdown.unrecorded_sales.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Leakage Points */}
            {analysisResult.leakage_points && analysisResult.leakage_points.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4">Identified Issues ({analysisResult.leakage_count})</h3>
                <div className="space-y-3">
                  {analysisResult.leakage_points.map((point, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-gray-900">{point.category}</h4>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          point.severity === 'high' ? 'bg-red-100 text-red-800' :
                          point.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {point.severity.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-2">{point.description}</p>
                      <p className="text-sm text-gray-600 mb-2"><strong>Impact:</strong> {point.impact}</p>
                      <p className="text-sm text-green-600"><strong>Recommendation:</strong> {point.recommendation}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recovery Strategies */}
            {analysisResult.recovery_strategies && analysisResult.recovery_strategies.length > 0 && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Recovery Strategies</h3>
                <div className="space-y-3">
                  {analysisResult.recovery_strategies.map((strategy, index) => (
                    <div key={index} className="border border-green-200 bg-green-50 rounded-lg p-4">
                      <h4 className="font-semibold text-green-900 mb-2">{strategy.name}</h4>
                      <p className="text-gray-700 mb-2">{strategy.description}</p>
                      <div className="flex gap-4 text-sm">
                        <span className="text-gray-600"><strong>Impact:</strong> {strategy.impact}</span>
                        <span className="text-gray-600"><strong>Timeline:</strong> {strategy.timeline}</span>
                        <span className="text-green-600"><strong>Recovery:</strong> {strategy.estimated_recovery}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => setAnalysisResult(null)}
              className="mt-6 w-full py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
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
