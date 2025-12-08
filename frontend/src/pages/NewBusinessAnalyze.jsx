import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { analyzeNewBusiness } from '../services/api'

const NewBusinessAnalyze = () => {
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors } } = useForm()
  const [loading, setLoading] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      const response = await analyzeNewBusiness(data)
      
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
        <h1 className="text-3xl font-bold text-gray-900 mb-2">New Business Analysis</h1>
        <p className="text-gray-600">
          Prevent revenue leakage before launch - Get risk assessment & strategic recommendations
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 bg-white rounded-lg shadow p-6">
        {/* Business Information */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-blue-600 border-b pb-2">Business Information</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Business Name *</label>
              <input
                {...register('business_name', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="My Startup"
              />
              {errors.business_name && <p className="text-red-500 text-sm mt-1">{errors.business_name.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Industry *</label>
              <input
                {...register('industry', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="E-commerce, SaaS, Retail"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Business Model *</label>
              <select
                {...register('business_model', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Pricing Strategy *</label>
              <select
                {...register('pricing_strategy', { required: 'Required' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select...</option>
                <option value="cost_plus">Cost Plus</option>
                <option value="value_based">Value Based</option>
                <option value="competitive">Competitive</option>
                <option value="dynamic">Dynamic</option>
                <option value="freemium">Freemium</option>
                <option value="tiered">Tiered</option>
              </select>
            </div>
          </div>
        </div>

        {/* Financial Projections */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-blue-600 border-b pb-2">Financial Projections</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expected Monthly Revenue ($) *</label>
              <input
                type="number"
                step="0.01"
                {...register('expected_monthly_revenue', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="50000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Product Price ($) *</label>
              <input
                type="number"
                step="0.01"
                {...register('product_price', { required: 'Required', min: 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="99.99"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cost per Unit ($) *</label>
              <input
                type="number"
                step="0.01"
                {...register('product_cost_per_unit', { required: 'Required', min: 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="40.00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expected Units Sold/Month *</label>
              <input
                type="number"
                {...register('expected_units_sold', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fixed Monthly Costs ($) *</label>
              <input
                type="number"
                step="0.01"
                {...register('fixed_monthly_costs', { required: 'Required', min: 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="10000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Planned Discount (%) *</label>
              <input
                type="number"
                step="0.1"
                {...register('planned_discount_percentage', { required: 'Required', min: 0, max: 100 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="10"
                defaultValue="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expected Refund Rate (%) *</label>
              <input
                type="number"
                step="0.1"
                {...register('expected_refund_rate', { required: 'Required', min: 0, max: 100 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="5"
                defaultValue="0"
              />
            </div>
          </div>
        </div>

        {/* Operational Setup */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-blue-600 border-b pb-2">Operational Setup</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Payment Methods *</label>
              <select
                {...register('payment_methods', { required: 'Required' })}
                multiple
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent h-32"
              >
                <option value="cash">Cash</option>
                <option value="card">Card</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="digital_wallet">Digital Wallet</option>
                <option value="credit">Credit</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">Hold Ctrl/Cmd to select multiple</p>
            </div>

            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  {...register('inventory_tracking')}
                  className="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">Inventory Tracking System</label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  {...register('has_billing_system')}
                  className="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">Automated Billing System</label>
              </div>
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors"
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
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-blue-900 mb-2">Executive Summary</h3>
              <p className="text-blue-800">{analysisResult.executive_summary}</p>
            </div>

            {/* Financial Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-green-600 mb-1">Expected Revenue</p>
                <p className="text-2xl font-bold text-green-900">
                  ${analysisResult.financial_summary.expected_monthly_revenue.toLocaleString()}
                </p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-sm text-red-600 mb-1">Potential Loss</p>
                <p className="text-2xl font-bold text-red-900">
                  ${analysisResult.total_potential_loss.toLocaleString()}
                </p>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <p className="text-sm text-yellow-600 mb-1">Risk Level</p>
                <p className="text-2xl font-bold text-yellow-900 capitalize">
                  {analysisResult.risk_level}
                </p>
              </div>
            </div>

            {/* Leakage Points */}
            {analysisResult.leakage_points && analysisResult.leakage_points.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4">Identified Risks ({analysisResult.leakage_count})</h3>
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
                      <p className="text-sm text-blue-600"><strong>Recommendation:</strong> {point.recommendation}</p>
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

export default NewBusinessAnalyze
