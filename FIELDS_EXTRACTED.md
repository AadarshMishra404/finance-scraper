# Complete List of IPO Fields Extracted

This document lists all fields that the Smart IPO Data Extractor can extract from ipoplatform.com HTML pages.

## 1. Basic Information (basic_info)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `company_name` | Name of the company | "Sudeep Pharma" | String |
| `ipo_category` | IPO listing category | "MainBoard Upcoming" | String |
| `exchange` | Stock exchange listing | "BSE,NSE" | String |
| `issue_type` | Type of issue | "Book Building" | String |

## 2. Important Dates (dates)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `drhp_date` | Draft RHP filing date | "24th June 2025" | String (Date) |
| `ipo_open_date` | IPO opening date | "21st November 2025" | String (Date) |
| `ipo_close_date` | IPO closing date | "25th November 2025" | String (Date) |
| `allotment_date` | Share allotment date | "26th November 2025" | String (Date) |
| `refund_date` | Refund initiation date | "27th November 2025" | String (Date) |
| `listing_date` | Stock listing date | "28th November 2025" | String (Date) |

## 3. Pricing Details (pricing)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `ipo_size_cr` | Total IPO size in crores | 895.0 | Float |
| `issue_price_rs` | Issue price per share in rupees | 593.0 | Float |
| `price_band_upper_rs` | Upper price band in rupees | 593.0 | Float |
| `face_value_rs` | Face value per share | 10.0 | Float |
| `lot_size` | Minimum shares per lot | 25 | Integer |

## 4. Financial Information (financial_info)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `market_cap_cr` | Market capitalisation in crores | 6698.0 | Float |
| `pe_ratio` | Price to Earnings ratio | 53.55 | Float |
| `revenue_annualised_cr` | Annualised revenue in crores | 499.64 | Float |
| `pat_annualised_cr` | Annualised PAT in crores | 125.08 | Float |
| `pre_issue_promoter_holding_percent` | Promoter holding % before IPO | 89.66 | Float |
| `post_issue_promoter_holding_percent` | Promoter holding % after IPO | 75.50 | Float |

## 5. Company Information (company_info)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `sector` | Industry sector | "Pharmaceutical" | String |
| `city` | Company headquarters city | "Vadodara" | String |
| `sub_sector` | Detailed sector description | "Technology-led manufacturer..." | String |
| `description` | Company description (500 chars) | "Sudeep Pharma Limited is..." | String |

## 6. Stakeholders (stakeholders)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `lead_managers` | BRLM (Book Running Lead Managers) | ["ICICI Securities Limited", "IIFL Securities Limited"] | Array[String] |
| `registrar` | Registrar and Transfer Agent | "Universal Capital Securities..." | String |

## 7. Issue Composition (issue_composition)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `fresh_issue_cr` | Fresh issue amount in crores | 95.0 | Float |
| `offer_for_sale_cr` | OFS amount in crores | 800.0 | Float |

## 8. Subscription Data (subscription)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `total_subscription_times` | Overall subscription (times) | 2.5 | Float |
| `total_subscription_raw` | Raw subscription text | "2.5 times" | String |
| `category_wise` | Category-wise subscription table | [{...}] | Array[Object] |

### Subscription Categories (when available):
- QIB (Qualified Institutional Buyers)
- NII (Non-Institutional Investors)
- Retail Individual Investors
- Employee Reservation
- Shareholder Reservation

## 9. Documents (documents)

| Field | Description | Example | Data Type |
|-------|-------------|---------|-----------|
| `rhp_url` | Red Herring Prospectus URL | "https://..." | String (URL) |
| `drhp_url` | Draft RHP URL | "https://..." | String (URL) |

---

## Complete Field Count

| Section | Fields Count |
|---------|--------------|
| Basic Information | 4 |
| Important Dates | 6 |
| Pricing Details | 5 |
| Financial Information | 6 |
| Company Information | 4 |
| Stakeholders | 2 |
| Issue Composition | 2 |
| Subscription | 2+ (varies) |
| Documents | 2 |
| **TOTAL** | **33+ fields** |

---

## Data Quality Notes

### Fields that may be missing for Upcoming IPOs:
- `issue_price_rs` - Shown as `[●]` until price band is announced
- `face_value_rs` - May not be disclosed in early stage
- `lot_size` - Announced closer to IPO opening
- `post_issue_promoter_holding_percent` - Calculated after final subscription
- `subscription` - Only available during/after IPO period
- `listing_date` - May change based on market conditions

### Always Available Fields:
- `company_name`
- `ipo_category`
- `exchange`
- `issue_type`
- `drhp_date`
- `sector`
- `city`
- `lead_managers`
- `registrar`
- `ipo_size_cr`
- `fresh_issue_cr`
- `offer_for_sale_cr`

---

## Usage Example

```python
from ipo_data_extractor import IPODataExtractor

extractor = IPODataExtractor('index.html')
data = extractor.extract_all()

# Access individual fields
company = data['basic_info']['company_name']
ipo_size = data['pricing']['ipo_size_cr']
sector = data['company_info']['sector']
brlm = data['stakeholders']['lead_managers'][0]

print(f"{company} IPO: ₹{ipo_size} Cr in {sector} sector")
print(f"Lead Manager: {brlm}")
```

Output:
```
Sudeep Pharma IPO: ₹895.0 Cr in Pharmaceutical sector
Lead Manager: ICICI Securities Limited
```

---

## For IPO Reports - Recommended Fields

### Essential Fields (Must Have):
1. Company Name
2. IPO Size
3. Issue Price / Price Band
4. IPO Open & Close Dates
5. Listing Date
6. Lot Size
7. Exchange
8. Sector
9. Lead Managers
10. Registrar

### Important Financial Fields:
11. Market Capitalisation
12. PE Ratio
13. Revenue (Annualised)
14. PAT (Annualised)
15. Fresh Issue vs OFS Breakdown
16. Promoter Holdings

### Additional Context:
17. Company Description
18. Sub-Sector
19. City/Location
20. DRHP/RHP Document Links

This ensures comprehensive coverage for investment analysis and decision-making.
