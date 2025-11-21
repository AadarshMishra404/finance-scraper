# IPO Data Extractor

A smart, robust data extractor for extracting IPO information from ipoplatform.com HTML pages. Handles variations in HTML structure and extracts all key IPO fields needed for investment analysis and reports.

## Features

### Extracted Data Categories

#### 1. Basic Information
- Company Name
- IPO Category (Mainboard/SME/Upcoming)
- Exchange (BSE/NSE)
- Issue Type (Book Building, Fixed Price)

#### 2. Important Dates
- DRHP Filed Date
- IPO Open Date
- IPO Close Date
- Allotment Date
- Refund Initiation Date
- Listing Date

#### 3. Pricing Details
- IPO Size (in Crores)
- Issue Price (in Rupees)
- Price Band (Upper/Lower)
- Face Value
- Lot Size (shares per lot)

#### 4. Financial Information
- Market Capitalisation
- P/E Ratio
- Revenue (Annualised)
- PAT - Profit After Tax (Annualised)
- Pre-Issue Promoter Holding (%)
- Post-Issue Promoter Holding (%)

#### 5. Company Information
- Sector
- City/Location
- Sub-Sector
- Company Description

#### 6. Stakeholders
- Lead Managers/BRLM (Book Running Lead Manager)
- Registrar (RTA)

#### 7. Issue Composition
- Fresh Issue Amount
- Offer for Sale (OFS) Amount

#### 8. Subscription Data
- Overall Subscription (times)
- Category-wise Subscription (QIB, NII, Retail)
- Day-wise Subscription

#### 9. Documents
- RHP (Red Herring Prospectus) URL
- DRHP (Draft RHP) URL

## Installation

### Requirements
- Python 3.7+
- BeautifulSoup4
- lxml (optional, for faster parsing)

```bash
pip install beautifulsoup4 lxml
```

## Usage

### Basic Usage

```python
from ipo_data_extractor import IPODataExtractor

# Initialize with HTML file path
extractor = IPODataExtractor('index.html')

# Extract all data
data = extractor.extract_all()

# Print summary to console
extractor.print_summary()

# Save to JSON file
extractor.save_to_json('ipo_data.json')
```

### Command Line Usage

```bash
python3 extract_ipo_data.py
```

This will:
1. Load `index.html` from the current directory
2. Extract all IPO data
3. Print a formatted summary
4. Save results to `sudeep_pharma_ipo_data.json`

### Advanced Usage

```python
from ipo_data_extractor import IPODataExtractor

# Initialize extractor
extractor = IPODataExtractor('path/to/ipo_page.html')

# Extract specific sections
basic_info = extractor._extract_basic_info()
dates = extractor._extract_dates()
pricing = extractor._extract_pricing()
financial = extractor._extract_financial_info()
company = extractor._extract_company_info()
stakeholders = extractor._extract_stakeholders()

# Get JSON string
json_str = extractor.to_json(indent=2)
print(json_str)
```

## Output Format

The extractor outputs data in JSON format with the following structure:

```json
{
  "basic_info": {
    "company_name": "Sudeep Pharma",
    "ipo_category": "MainBoard Upcoming",
    "exchange": "BSE,NSE",
    "issue_type": "Book Building"
  },
  "dates": {
    "drhp_date": "24th June 2025",
    "ipo_open_date": "21st November 2025",
    "ipo_close_date": "25th November 2025",
    "allotment_date": "26th November 2025",
    "refund_date": "27th November 2025",
    "listing_date": "28th November 2025"
  },
  "pricing": {
    "ipo_size_cr": 895.0,
    "issue_price_rs": 593.0,
    "lot_size": 25
  },
  "financial_info": {
    "market_cap_cr": 6698.0,
    "pe_ratio": 53.55,
    "revenue_annualised_cr": 499.64,
    "pat_annualised_cr": 125.08,
    "pre_issue_promoter_holding_percent": 89.66
  },
  "company_info": {
    "sector": "Pharmaceutical",
    "city": "Vadodara",
    "sub_sector": "Technology-led manufacturer...",
    "description": "Company description..."
  },
  "stakeholders": {
    "lead_managers": [
      "ICICI Securities Limited",
      "IIFL Securities Limited"
    ],
    "registrar": "Universal Capital Securities Private Limited"
  },
  "issue_composition": {
    "fresh_issue_cr": 95.0,
    "offer_for_sale_cr": 800.0
  },
  "documents": {
    "rhp_url": "https://...",
    "drhp_url": "https://..."
  }
}
```

## Key Features

### 1. Smart Pattern Matching
- Uses multiple regex patterns with fallbacks
- Handles variations in HTML structure
- Validates extracted data (e.g., date format validation)

### 2. Robust Error Handling
- Continues extraction even if some fields are missing
- Handles placeholder values like `[●]`
- Cleans HTML entities and extra whitespace

### 3. Flexible Input
- Accepts HTML file path
- Accepts raw HTML string
- Works with large HTML files (800KB+)

### 4. Multiple Output Formats
- Python dictionary
- JSON string
- JSON file
- Formatted console output

## Example: Sudeep Pharma IPO

```bash
$ python3 extract_ipo_data.py
```

Output:
```
================================================================================
IPO DATA EXTRACTION SUMMARY
================================================================================

📋 BASIC INFORMATION
----------------------------------------
  Company Name: Sudeep Pharma
  IPO Category: MainBoard Upcoming
  Exchange: BSE,NSE
  Issue Type: Book Building

📅 IMPORTANT DATES
----------------------------------------
  DRHP Date: 24th June 2025
  IPO Open Date: 21st November 2025
  IPO Close Date: 25th November 2025
  Allotment Date: 26th November 2025
  Listing Date: 28th November 2025

💰 PRICING DETAILS
----------------------------------------
  IPO Size: ₹895.00 Cr
  Issue Price: ₹593.00

📊 FINANCIAL INFORMATION
----------------------------------------
  Market Cap: ₹6,698.00 Cr
  PE Ratio: 53.55
  Revenue (annualised): ₹499.64 Cr
  PAT (annualised): ₹125.08 Cr
  Pre-Issue Promoter Holding: 89.66%

🏢 COMPANY INFORMATION
----------------------------------------
  Sector: Pharmaceutical
  City: Vadodara
  Sub Sector: Technology-led manufacturer...

👥 STAKEHOLDERS
----------------------------------------
  Lead Managers:
    - ICICI Securities Limited
    - IIFL Securities Limited
  Registrar: Universal Capital Securities Private Limited

================================================================================
```

## Customization

### Adding New Fields

To add extraction for new fields, add a method in the `IPODataExtractor` class:

```python
def _extract_custom_field(self) -> Dict[str, Any]:
    """Extract custom field"""
    html_str = str(self.soup)

    pattern = r'Your Pattern Here'
    match = re.search(pattern, html_str, re.IGNORECASE)

    if match:
        return {'field_name': self._clean_text(match.group(1))}

    return {}
```

Then add it to the `extract_all()` method:

```python
def extract_all(self) -> Dict[str, Any]:
    self.data = {
        # ... existing fields ...
        'custom_data': self._extract_custom_field()
    }
    return self.data
```

## Use Cases

1. **IPO Analysis**: Gather all key IPO data for investment decisions
2. **Market Research**: Track IPO trends, sectors, and performance
3. **Automated Reporting**: Generate IPO reports automatically
4. **Data Aggregation**: Build IPO databases from multiple HTML pages
5. **Comparison**: Compare multiple IPOs side by side

## Limitations

- Designed specifically for ipoplatform.com HTML structure
- May need pattern updates if website structure changes
- Subscription data requires IPO to be open/closed (not available for upcoming IPOs)
- Some fields may be marked as `[●]` for upcoming IPOs

## Future Enhancements

- [ ] Support for GMP (Grey Market Premium) extraction
- [ ] Anchor investor data extraction
- [ ] Historical performance metrics
- [ ] Peer comparison data
- [ ] CSV export functionality
- [ ] Batch processing for multiple HTML files
- [ ] API integration for live data

## License

MIT License - Feel free to use and modify as needed.

## Author

Created for extracting IPO data from ipoplatform.com

---

**Note**: This extractor is for educational and research purposes. Always verify critical financial information from official sources (SEBI, Stock Exchange, Company RHP/DRHP).
