# IPO Search System - Complete Guide

A powerful search system that lets you find and extract IPO company details from ipoplatform.com by simply searching for the company name.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Build Company Index (First Time Setup)

```bash
python3 ipo_cli.py --build
```

This will scrape ipoplatform.com and create a searchable index of all IPO companies. Takes ~1-2 minutes.

### 3. Search for a Company

```bash
# Interactive mode (recommended for beginners)
python3 ipo_cli.py --interactive

# Direct search
python3 ipo_cli.py --search "Sudeep"

# Get full details
python3 ipo_cli.py --details "Sudeep Pharma"
```

---

## 📋 Components

### 1. **ipo_index_builder.py** - Index Builder
Scrapes ipoplatform.com listing pages to build a searchable index of companies.

```python
from ipo_index_builder import IPOIndexBuilder

builder = IPOIndexBuilder()
companies = builder.build_index()
builder.save_index('companies_index.json')
```

### 2. **ipo_search_engine.py** - Search Engine
Provides fuzzy search capabilities with similarity matching.

```python
from ipo_search_engine import IPOSearchEngine

engine = IPOSearchEngine('companies_index.json')
results = engine.search('Sudeep', limit=10)
```

### 3. **search_ipo.py** - Search & Extract Tool
Combines search with data extraction.

```python
from search_ipo import IPOSearchAndExtract

tool = IPOSearchAndExtract()
tool.search_and_extract('Sudeep Pharma', save_json=True)
```

### 4. **ipo_cli.py** - Command Line Interface
Easy-to-use CLI for all operations.

---

## 🎯 Usage Examples

### Example 1: Interactive Search (Easiest)

```bash
python3 ipo_cli.py --interactive
```

```
🔍 Enter company name to search: Sudeep

Found 2 matching companies:
1. Sudeep Pharma (MainBoard)
   Match: ██████████ 95.2% | ID: 4179

📌 Select a company (number): 1
✓ Selected: Sudeep Pharma
💾 Save to JSON file? (y/n): y

[Extracts and displays full IPO data]
```

### Example 2: Direct Command Line Search

```bash
# Search only (quick lookup)
python3 ipo_cli.py --search "Pharma"

# Get full details (extracts all data)
python3 ipo_cli.py --details "Sudeep Pharma"
```

### Example 3: Using Python Scripts Directly

```python
# Method 1: Non-interactive
python3 search_ipo.py "Sudeep Pharma"

# Method 2: Interactive
python3 search_ipo.py
```

### Example 4: Programmatic Usage

```python
from search_ipo import IPOSearchAndExtract

# Initialize
tool = IPOSearchAndExtract()

# Search for companies
results = tool.search_companies('Sudeep', limit=5)
for company in results:
    print(f"{company['name']} - {company['url']}")

# Get full details for best match
data = tool.search_and_extract('Sudeep Pharma', save_json=True)

# Access extracted data
print(data['basic_info']['company_name'])
print(data['pricing']['ipo_size_cr'])
print(data['financial_info']['market_cap_cr'])
```

---

## 🔧 CLI Commands Reference

### Build Index
```bash
python3 ipo_cli.py --build
```
Scrapes all IPO listing pages and creates `companies_index.json`

### Search Companies
```bash
python3 ipo_cli.py --search "QUERY"
```
Shows matching companies with similarity scores

### Get Company Details
```bash
python3 ipo_cli.py --details "COMPANY NAME"
```
Fetches and extracts full IPO data, saves to JSON

### Interactive Mode
```bash
python3 ipo_cli.py --interactive
```
Step-by-step guided search and extraction

### Show Statistics
```bash
python3 ipo_cli.py --stats
```
Display index statistics

### List Categories
```bash
python3 ipo_cli.py --categories
```
Show all IPO categories (Mainboard, SME, etc.)

---

## 🎨 Features

### 1. Fuzzy Search
Finds companies even with partial or misspelled names:
- "Sudeep" → finds "Sudeep Pharma"
- "pharma" → finds all pharmaceutical companies
- "ICICI" → finds all ICICI-related IPOs

### 2. Similarity Scoring
Results ranked by relevance:
```
1. Sudeep Pharma
   Match: ██████████ 95.2%

2. Deep Industries
   Match: ████████   78.3%
```

### 3. Smart Index
- Covers Mainboard, SME, and Upcoming IPOs
- Deduplicates companies
- Fast local search (no internet needed after index is built)

### 4. Live Data Extraction
- Fetches latest data from ipoplatform.com
- Extracts 50+ fields of IPO information
- Saves to JSON for further processing

---

## 📊 Output Format

When you extract company details, you get a JSON file with:

```json
{
  "basic_info": {
    "company_name": "Sudeep Pharma",
    "ipo_category": "MainBoard Upcoming",
    "exchange": "BSE,NSE"
  },
  "dates": {
    "ipo_open_date": "21st November 2025",
    "ipo_close_date": "25th November 2025"
  },
  "pricing": {
    "ipo_size_cr": 895.0,
    "issue_price_rs": 593.0
  },
  "financial_info": {
    "market_cap_cr": 6698.0,
    "pe_ratio": 53.55
  },
  "company_info": {
    "sector": "Pharmaceutical",
    "city": "Vadodara"
  }
}
```

---

## 🔄 Updating the Index

The company index should be updated periodically to include new IPOs:

```bash
# Rebuild index (recommended: once per week)
python3 ipo_cli.py --build
```

---

## 💡 Tips & Best Practices

### For Searching
- Use short, distinctive keywords: "Sudeep", "Pharma", "ICICI"
- Try different variations if first search doesn't work
- Use interactive mode for exploration

### For Data Extraction
- Save JSON files for record-keeping
- Check the extracted data for [●] placeholders (means data not available)
- For upcoming IPOs, some fields may be empty

### For Automation
```python
# Example: Batch processing
from search_ipo import IPOSearchAndExtract

companies = ['Sudeep Pharma', 'XYZ IPO', 'ABC Corp']
tool = IPOSearchAndExtract()

for company in companies:
    print(f"\nProcessing: {company}")
    tool.search_and_extract(company, save_json=True)
```

---

## 🐛 Troubleshooting

### "No index found"
```bash
# Build the index first
python3 ipo_cli.py --build
```

### "No companies found"
- Try a shorter/different search term
- Rebuild index if company is very new
- Check if company name is correct on ipoplatform.com

### "Error fetching data"
- Check internet connection
- The website might be down temporarily
- URL structure might have changed (report as issue)

### Import errors
```bash
# Install dependencies
pip install -r requirements.txt
```

---

## 📁 File Structure

```
.
├── ipo_cli.py                  # Main CLI interface
├── search_ipo.py               # Search & extract tool
├── ipo_search_engine.py        # Search engine
├── ipo_index_builder.py        # Index builder
├── ipo_data_extractor.py       # Data extractor (existing)
├── companies_index.json        # Company index (generated)
└── *_data.json                 # Extracted company data files
```

---

## 🚀 Advanced Usage

### Custom Index Location
```python
from ipo_search_engine import IPOSearchEngine

engine = IPOSearchEngine('custom_index.json')
results = engine.search('Company Name')
```

### Search by Category
```python
from ipo_search_engine import IPOSearchEngine

engine = IPOSearchEngine()
mainboard_companies = engine.search_by_category('mainboard')
sme_companies = engine.search_by_category('sme')
```

### Search by ID
```python
from ipo_search_engine import IPOSearchEngine

engine = IPOSearchEngine()
company = engine.search_by_id('4179')  # Sudeep Pharma
```

---

## 📝 Notes

- The system scrapes publicly available data from ipoplatform.com
- Always verify critical financial data from official sources (SEBI, RHP)
- For educational and research purposes
- Respect website's terms of service and rate limits

---

## 🎉 You're All Set!

Try it now:
```bash
python3 ipo_cli.py --interactive
```

Happy IPO hunting! 🚀
