import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { analyzeNewBusiness } from '../services/api'
import { TrendingUp, AlertCircle, DollarSign, Target, Lightbulb, CheckCircle, XCircle } from 'lucide-react'

const NewBusinessAnalyze = () => {
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors }, watch } = useForm()
  const [loading, setLoading] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [showOtherBusinessModel, setShowOtherBusinessModel] = useState(false)
  const [showOtherPricingStrategy, setShowOtherPricingStrategy] = useState(false)
  
  // Watch for "other" selection
  const businessModel = watch('business_model')
  const pricingStrategy = watch('pricing_strategy')

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      // Use custom values if "other" is selected
      const submitData = {
        ...data,
        business_model: data.business_model === 'other' ? data.other_business_model : data.business_model,
        pricing_strategy: data.pricing_strategy === 'other' ? data.other_pricing_strategy : data.pricing_strategy,
      }
      
      const response = await analyzeNewBusiness(submitData)
      
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
        <h1 className="text-3xl font-bold text-black mb-2">New Business Analysis</h1>
        <p className="text-gray-600">
          Prevent revenue leakage before launch - Get risk assessment & strategic recommendations
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
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base"
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
                onChange={(e) => setShowOtherBusinessModel(e.target.value === 'other')}
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
                <option value="other">Other (Specify)</option>
              </select>
              {errors.business_model && <p className="text-red-500 text-sm mt-1">{errors.business_model.message}</p>}
              
              {/* Show text input if "Other" is selected */}
              {(showOtherBusinessModel || businessModel === 'other') && (
                <div className="mt-2">
                  <input
                    {...register('other_business_model', { 
                      required: businessModel === 'other' ? 'Please specify your business model' : false 
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your business model"
                  />
                  {errors.other_business_model && <p className="text-red-500 text-sm mt-1">{errors.other_business_model.message}</p>}
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pricing Strategy *</label>
              <select
                {...register('pricing_strategy', { required: 'Required' })}
                onChange={(e) => setShowOtherPricingStrategy(e.target.value === 'other')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select...</option>
                <option value="cost_plus">Cost Plus</option>
                <option value="value_based">Value Based</option>
                <option value="competitive">Competitive</option>
                <option value="dynamic">Dynamic</option>
                <option value="freemium">Freemium</option>
                <option value="tiered">Tiered</option>
                <option value="other">Other (Specify)</option>
              </select>
              {errors.pricing_strategy && <p className="text-red-500 text-sm mt-1">{errors.pricing_strategy.message}</p>}
              
              {/* Show text input if "Other" is selected */}
              {(showOtherPricingStrategy || pricingStrategy === 'other') && (
                <div className="mt-2">
                  <input
                    {...register('other_pricing_strategy', { 
                      required: pricingStrategy === 'other' ? 'Please specify your pricing strategy' : false 
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your pricing strategy"
                  />
                  {errors.other_pricing_strategy && <p className="text-red-500 text-sm mt-1">{errors.other_pricing_strategy.message}</p>}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Financial Projections */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Financial Projections</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expected Monthly Revenue (₹) *</label>
              <input
                type="number"
                step="0.01"
                {...register('expected_monthly_revenue', { required: 'Required', min: 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="500000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Product Price (₹) *</label>
              <input
                type="number"
                step="0.01"
                {...register('product_price', { required: 'Required', min: 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="999.00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cost per Unit (₹) *</label>
              <input
                type="number"
                step="0.01"
                {...register('product_cost_per_unit', { required: 'Required', min: 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="400.00"
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Fixed Monthly Costs (₹) *</label>
              <input
                type="number"
                step="0.01"
                {...register('fixed_monthly_costs', { required: 'Required', min: 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="100000"
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
          <h2 className="text-xl font-semibold text-black border-b-2 border-gray-300 pb-2">Operational Setup</h2>
          
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
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-gradient-to-r from-black to-gray-900 text-white py-4 px-6 rounded-lg hover:from-gray-900 hover:to-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors shadow-md touch-manipulation text-base"
          >
            {loading ? 'Analyzing...' : 'Analyze Business'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-6 py-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors touch-manipulation text-base"
          >
            Cancel
          </button>
        </div>
      </form>

      {/* Results Display */}
      {analysisResult && (
        <div className="mt-8 space-y-6">
          <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
            <h2 className="text-2xl font-bold text-black mb-6">Analysis Results</h2>
            
            {/* Executive Summary */}
            <div className="bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-300 rounded-lg p-5 mb-6">
              <h3 className="font-semibold text-black mb-2 flex items-center gap-2">
                <TrendingUp size={20} className="text-black" />
                Executive Summary
              </h3>
              <p className="text-gray-800">{analysisResult.executive_summary}</p>
            </div>

            {/* Financial Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-5 rounded-lg border border-gray-300 hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-2">
                  <DollarSign size={18} className="text-black" />
                  <p className="text-sm text-gray-700 font-medium">Expected Revenue</p>
                </div>
                <p className="text-2xl font-bold text-black">
                  ₹{analysisResult.financial_summary.expected_monthly_revenue.toLocaleString()}
                </p>
              </div>
              <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-5 rounded-lg border border-gray-400 hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-2">
                  <AlertCircle size={18} className="text-gray-900" />
                  <p className="text-sm text-gray-700 font-medium">Potential Loss</p>
                </div>
                <p className="text-2xl font-bold text-gray-900">
                  ₹{analysisResult.total_potential_loss.toLocaleString()}
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

            {/* Leakage Points */}
            {analysisResult.leakage_points && analysisResult.leakage_points.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <AlertCircle size={22} className="text-black" />
                  Identified Risks ({analysisResult.leakage_count})
                </h3>
                <div className="space-y-3">
                  {analysisResult.leakage_points.map((point, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-black transition-colors bg-gradient-to-r from-white to-gray-50">
                      <div className="flex justify-between items-start mb-3">
                        <h4 className="font-semibold text-gray-900">{point.category}</h4>
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

export default NewBusinessAnalyze
