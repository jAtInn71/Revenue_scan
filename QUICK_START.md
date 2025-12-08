# 🚀 Quick Start - Excel Analysis

## 3-Minute Setup

### 1. Install Dependencies
```bash
cd Revenue_scan/backend
pip install -r requirements.txt
```

### 2. Start Backend
```bash
python main.py
```
Server runs at: `http://localhost:8000`

### 3. Start Frontend (New Terminal)
```bash
cd Revenue_scan/frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

### 4. Create Test Data (Optional)
```bash
cd Revenue_scan
python create_sample_data.py
```

This generates 3 sample files you can upload immediately.

## 📤 Upload Your First File

1. Open browser: `http://localhost:5173`
2. Login (or sign up)
3. Click **Upload** in navigation
4. Drag & drop any Excel/CSV file
5. Click **Upload** button
6. **View Results!** 🎉

## 📊 What Files Work?

**ANY Excel or CSV with financial data!**

Examples:
- Sales reports
- Invoice exports
- Transaction logs
- Revenue statements
- Customer purchase history
- Product sales data
- E-commerce orders
- POS exports

**Column names don't matter!** System auto-detects:
- Revenue/Sales/Income/Amount columns
- Cost/Expense columns
- Customer/Client columns
- Product/Item columns
- Discounts, refunds, and more

## 🎯 What You'll Get

### Instant Analysis:
✅ **Leakage Detection** - 9 different checks  
✅ **Financial Summary** - Revenue, costs, profit, margin  
✅ **AI Insights** - Strategic recommendations  
✅ **KPIs** - All key metrics calculated  
✅ **Issue Details** - What's wrong and how to fix  
✅ **Action Plan** - 30-day implementation guide  

### Example Output:
```
📊 Leakage Analysis
- Total Issues: 8
- Critical: 2
- Impact: $45,250

💰 Financial Summary
- Revenue: $1,250,000
- Profit: $375,000
- Margin: 30%

🎯 Top Recommendations
1. Fix negative revenue - Save $12,500
2. Reduce discounts - Save $5,625
3. Standardize pricing - Save $8,500
```

## 📝 Sample Data

Use our test data generator:
```bash
python create_sample_data.py
```

Creates 3 files:
1. **Sample_Revenue_Data.xlsx** - Full dataset (3 sheets)
2. **Sample_Revenue_Data.csv** - CSV version
3. **Problem_Dataset.xlsx** - Intentional issues for testing

Upload any of these to see the system in action!

## 🔧 Troubleshooting

**Backend won't start?**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

**Frontend won't start?**
```bash
cd frontend
npm install --force
npm run dev
```

**"File cannot be parsed"?**
- Open file in Excel
- Save As → CSV UTF-8
- Try uploading again

**No columns detected?**
- Ensure first row has headers
- Use descriptive names (e.g., "Revenue" not "Col1")

## 💡 Pro Tips

1. **Best Results**: Include revenue, cost, customer, and product columns
2. **Column Names**: Use keywords like "sales", "revenue", "customer"
3. **Clean Data**: Remove empty rows at top
4. **Multiple Sheets**: Upload each sheet separately for detailed analysis
5. **Regular Analysis**: Upload monthly to track improvements

## 📚 More Info

- **Complete Guide**: See `EXCEL_ANALYSIS_GUIDE.md`
- **What's Fixed**: See `EXCEL_ANALYSIS_COMPLETE.md`
- **Code Documentation**: Check `services/enhanced_leakage_analyzer.py`

## ✨ That's It!

You're ready to analyze ANY Excel/CSV file and stop revenue leakage! 🎉

**Upload a file and watch the magic happen!** 🚀
