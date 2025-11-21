"""
Smart IPO Data Extractor
Extracts all required fields from IPO Platform website HTML
Handles variations and missing data gracefully
"""

import re
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional, List
import json


class IPODataExtractor:
    """
    Smart extractor class for IPO data from ipoplatform.com HTML pages
    """

    def __init__(self, html_content: str):
        """
        Initialize the extractor with HTML content

        Args:
            html_content: Raw HTML string or file path
        """
        if html_content.endswith('.html'):
            with open(html_content, 'r', encoding='utf-8') as f:
                html_content = f.read()

        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.data = {}

    def extract_all(self) -> Dict[str, Any]:
        """
        Extract all IPO data and return as structured dictionary

        Returns:
            Dictionary containing all extracted IPO data
        """
        self.data = {
            'basic_info': self._extract_basic_info(),
            'dates': self._extract_dates(),
            'pricing': self._extract_pricing(),
            'financial_info': self._extract_financial_info(),
            'stakeholders': self._extract_stakeholders(),
            'company_info': self._extract_company_info(),
            'subscription': self._extract_subscription(),
            'issue_composition': self._extract_issue_composition(),
            'documents': self._extract_documents()
        }

        return self.data

    def _clean_text(self, text: Optional[str]) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace, newlines, and special characters
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove [●] placeholder
        text = re.sub(r'\[●\]', '', text)
        return text.strip()

    def _extract_currency_value(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract currency values like '₹ 895.00 Cr.'

        Returns:
            {'value': 895.00, 'unit': 'Cr', 'currency': '₹'}
        """
        if not text:
            return None

        # Pattern: ₹ 895.00 Cr. or Rs. 895.00 Crore
        pattern = r'[₹Rs.]*\s*([\d,]+\.?\d*)\s*(Cr\.?|Crore|Lakh|Lakhs)?'
        match = re.search(pattern, text)

        if match:
            value = match.group(1).replace(',', '')
            unit = match.group(2) if match.group(2) else ''

            return {
                'value': float(value) if value else None,
                'unit': unit.replace('.', ''),
                'currency': '₹',
                'raw': self._clean_text(text)
            }

        return {'raw': self._clean_text(text)}

    def _extract_basic_info(self) -> Dict[str, Any]:
        """Extract basic IPO information"""
        basic_info = {}

        # Company Name from title
        title = self.soup.find('title')
        if title:
            match = re.search(r'^(.+?)\s+IPO', title.text)
            basic_info['company_name'] = match.group(1).strip() if match else ""

        # IPO Category
        category_elem = self.soup.find('span', class_='mainboard-ipo')
        if category_elem:
            basic_info['ipo_category'] = self._clean_text(category_elem.text)

        # Exchange
        exchange_pattern = re.compile(r'Exchange\s*:\s*<span[^>]*>([^<]+)</span>')
        exchange_match = exchange_pattern.search(str(self.soup))
        if exchange_match:
            basic_info['exchange'] = self._clean_text(exchange_match.group(1))

        # Issue Type
        issue_type_pattern = re.compile(r'Issue Type\s*:\s*<span[^>]*>([^<]+)</span>')
        issue_type_match = issue_type_pattern.search(str(self.soup))
        if issue_type_match:
            basic_info['issue_type'] = self._clean_text(issue_type_match.group(1))

        return basic_info

    def _extract_dates(self) -> Dict[str, str]:
        """Extract all important dates"""
        dates = {}

        # Date pattern: matches dates like "21st November 2025" or "24th June 2025"
        date_regex = r'\d{1,2}(?:st|nd|rd|th)\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'

        # Find specific date fields with better patterns
        date_fields = {
            'drhp_date': r'(?:Date of DRHP|filed its Draft Red Herring Prospectus.*?on).*?<b[^>]*>([^<]+)</b>',
            'ipo_open_date': r'IPO open date is.*?<b[^>]*>([^<]+)</b>',
            'ipo_close_date': r'(?:close|IPO Close).*?date is.*?<b[^>]*>([^<]+)</b>',
            'allotment_date': r'(?:IPO )?Allotment Date is.*?<b[^>]*>([^<]+)</b>',
            'refund_date': r'(?:Initiation of Refund|refund dates).*?<b[^>]*>([^<]+)</b>',
            'listing_date': r'Listing date is.*?<b[^>]*>([^<]+)</b>'
        }

        html_str = str(self.soup)
        for field, pattern in date_fields.items():
            match = re.search(pattern, html_str, re.IGNORECASE | re.DOTALL)
            if match:
                date_text = self._clean_text(match.group(1))
                # Validate it's actually a date
                if re.search(date_regex, date_text):
                    dates[field] = date_text

        return dates

    def _extract_pricing(self) -> Dict[str, Any]:
        """Extract pricing information"""
        pricing = {}

        html_str = str(self.soup)

        # IPO Size - multiple patterns
        size_patterns = [
            r'IPO size is.*?<b>₹\s*([\d,]+\.?\d*)\s*(Cr\.?|Crore)',
            r'ipo size of ₹\s*([\d,]+\.?\d*)\s*(Cr\.?)',
            r'IPO\s+Size\s*:.*?<b[^>]*>₹\s*([\d,]+\.?\d*)\s*(Cr\.?)'
        ]
        for pattern in size_patterns:
            size_match = re.search(pattern, html_str, re.IGNORECASE)
            if size_match:
                pricing['ipo_size_cr'] = float(size_match.group(1).replace(',', ''))
                break

        # Issue Price
        price_patterns = [
            r'Issue Price\s*:.*?<b[^>]*>₹\s*([\d,]+\.?\d*)',
            r'IPO price of.*?<b>₹\s*([\d,]+\.?\d*)</b>'
        ]
        for pattern in price_patterns:
            price_match = re.search(pattern, html_str, re.IGNORECASE)
            if price_match:
                pricing['issue_price_rs'] = float(price_match.group(1).replace(',', ''))
                break

        # Price Band (upper)
        band_pattern = r'upper price band.*?is set at ₹\s*([\d,]+\.?\d*)'
        band_match = re.search(band_pattern, html_str, re.IGNORECASE)
        if band_match:
            pricing['price_band_upper_rs'] = float(band_match.group(1).replace(',', ''))

        # Face Value
        face_value_pattern = r'Face Value.*?₹\s*([\d,]+\.?\d*)'
        face_value_match = re.search(face_value_pattern, html_str, re.IGNORECASE)
        if face_value_match:
            pricing['face_value_rs'] = float(face_value_match.group(1).replace(',', ''))

        # Lot Size
        lot_pattern = r'(?:Lot Size|Market Lot|lot size).*?(\d+)\s*(?:shares?)?'
        lot_match = re.search(lot_pattern, html_str, re.IGNORECASE)
        if lot_match:
            pricing['lot_size'] = int(lot_match.group(1))

        return pricing

    def _extract_financial_info(self) -> Dict[str, Any]:
        """Extract financial information"""
        financial = {}

        html_str = str(self.soup)

        # Market Capitalisation
        mcap_pattern = r'Market Capitalisation\s*:.*?<b[^>]*>₹\s*([\d,]+\.?\d*)\s*Cr\.'
        mcap_match = re.search(mcap_pattern, html_str, re.IGNORECASE)
        if mcap_match:
            financial['market_cap_cr'] = float(mcap_match.group(1).replace(',', ''))

        # PE Multiple/Ratio
        pe_patterns = [
            r'PE\s+(?:multiple|Ratio)\s*:.*?<b[^>]*>([\d,]+\.?\d*)',
            r'PE\s+Ratio:<b[^>]*>([\d,]+\.?\d*)x?</b>'
        ]
        for pattern in pe_patterns:
            pe_match = re.search(pattern, html_str, re.IGNORECASE)
            if pe_match:
                financial['pe_ratio'] = float(pe_match.group(1).replace(',', ''))
                break

        # Revenue (annualised)
        revenue_pattern = r'Revenue\s*\(annualised\).*?<b[^>]*>₹\s*([\d,]+\.?\d*)\s*cr\.'
        revenue_match = re.search(revenue_pattern, html_str, re.IGNORECASE)
        if revenue_match:
            financial['revenue_annualised_cr'] = float(revenue_match.group(1).replace(',', ''))

        # PAT (Profit After Tax) - annualised
        pat_pattern = r'PAT:\s*\(annualised\).*?<b[^>]*>₹\s*([\d,]+\.?\d*)\s*cr\.'
        pat_match = re.search(pat_pattern, html_str, re.IGNORECASE)
        if pat_match:
            financial['pat_annualised_cr'] = float(pat_match.group(1).replace(',', ''))

        # Promoter Holdings
        pre_holding_pattern = r'Pre Issue Promoter Holding\s*:.*?<b[^>]*>([\d.]+)\s*%'
        pre_holding_match = re.search(pre_holding_pattern, html_str, re.IGNORECASE)
        if pre_holding_match:
            financial['pre_issue_promoter_holding_percent'] = float(pre_holding_match.group(1))

        post_holding_pattern = r'Post Issue Promoter Holding\s*:.*?<b[^>]*>([\d.]+)\s*%'
        post_holding_match = re.search(post_holding_pattern, html_str, re.IGNORECASE)
        if post_holding_match:
            financial['post_issue_promoter_holding_percent'] = float(post_holding_match.group(1))

        return financial

    def _extract_stakeholders(self) -> Dict[str, Any]:
        """Extract stakeholder information (BRLM, Registrar)"""
        stakeholders = {}

        html_str = str(self.soup)

        # Lead Manager / BRLM - Extract from specific mentions
        brlm_pattern = r'<a href="[^"]*merchant-banker[^"]*"[^>]*>\s*<b[^>]*>\s*([^<]+?(?:Securities|Capital|Advisory)[^<]*?Limited)\s*</b>'
        brlm_matches = re.findall(brlm_pattern, html_str, re.IGNORECASE)
        if brlm_matches:
            # Remove duplicates while preserving order
            seen = set()
            brlms = []
            for brlm in brlm_matches:
                brlm_clean = self._clean_text(brlm)
                if brlm_clean and brlm_clean not in seen:
                    seen.add(brlm_clean)
                    brlms.append(brlm_clean)
            stakeholders['lead_managers'] = brlms[:3]  # Limit to top 3

        # Registrar - More specific pattern
        registrar_pattern = r'<a[^>]*href="[^"]*ipo-registrar[^"]*"[^>]*>\s*([^<]+?(?:Securities|Capital|Computers|Consultants)[^<]*?Limited[^<]*?)\s*(?:<i|</a>)'
        registrar_match = re.search(registrar_pattern, html_str, re.IGNORECASE)
        if registrar_match:
            stakeholders['registrar'] = self._clean_text(registrar_match.group(1))

        return stakeholders

    def _extract_company_info(self) -> Dict[str, str]:
        """Extract company information"""
        company = {}

        html_str = str(self.soup)

        # Sector - Extract from link text more carefully
        sector_pattern = r'<a[^>]*href="[^"]*know-your-sector/([^"]+)"[^>]*>\s*<b[^>]*>([^<]+)</b>'
        sector_match = re.search(sector_pattern, html_str, re.IGNORECASE)
        if sector_match:
            company['sector'] = self._clean_text(sector_match.group(2))
        else:
            # Fallback: look for sector mention
            sector_fallback = r'caters to.*?<a[^>]*>\s*<b[^>]*>([^<]+)</b>\s*</a>\s*sector'
            sector_fallback_match = re.search(sector_fallback, html_str, re.IGNORECASE)
            if sector_fallback_match:
                company['sector'] = self._clean_text(sector_fallback_match.group(1))

        # City/Location - Extract from link text more carefully
        city_pattern = r'<a[^>]*href="[^"]*geography-wise-ipos/([^"]+)"[^>]*>\s*<b[^>]*>([^<]+)</b>'
        city_match = re.search(city_pattern, html_str, re.IGNORECASE)
        if city_match:
            company['city'] = self._clean_text(city_match.group(2))
        else:
            # Fallback: look for city mention
            city_fallback = r'based in.*?<a[^>]*>\s*<b[^>]*>([^<]+)</b>\s*</a>'
            city_fallback_match = re.search(city_fallback, html_str, re.IGNORECASE)
            if city_fallback_match:
                company['city'] = self._clean_text(city_fallback_match.group(1))

        # Sub Sector
        subsector_pattern = r'Sub Sector\s*:\s*<b[^>]*>([^<]+)</b>'
        subsector_match = re.search(subsector_pattern, html_str, re.IGNORECASE)
        if subsector_match:
            company['sub_sector'] = self._clean_text(subsector_match.group(1))

        # Company Description
        desc_div = self.soup.find('div', id='company-info-preview')
        if desc_div:
            desc_text = self._clean_text(desc_div.text)
            # Remove quotes at start/end
            desc_text = desc_text.strip('"')
            company['description'] = desc_text[:500]  # First 500 chars

        return company

    def _extract_subscription(self) -> Dict[str, Any]:
        """Extract subscription data"""
        subscription = {}

        html_str = str(self.soup)

        # Overall Subscription
        sub_pattern = r'Subscription\s*:.*?<b[^>]*>([^<]+)</b>'
        sub_match = re.search(sub_pattern, html_str, re.IGNORECASE)
        if sub_match:
            sub_text = self._clean_text(sub_match.group(1))
            if sub_text and sub_text != '[●]':
                # Extract times subscribed
                times_match = re.search(r'([\d.]+)\s*times', sub_text, re.IGNORECASE)
                if times_match:
                    subscription['total_subscription_times'] = float(times_match.group(1))
                else:
                    subscription['total_subscription_raw'] = sub_text

        # Look for subscription table (category-wise)
        sub_table = self.soup.find('table', class_=re.compile(r'subscription'))
        if sub_table:
            subscription['category_wise'] = self._parse_subscription_table(sub_table)

        return subscription

    def _parse_subscription_table(self, table) -> List[Dict[str, str]]:
        """Parse subscription table data"""
        rows = []
        headers = []

        # Extract headers
        header_row = table.find('thead')
        if header_row:
            headers = [self._clean_text(th.text) for th in header_row.find_all('th')]

        # Extract data rows
        tbody = table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                cells = [self._clean_text(td.text) for td in tr.find_all('td')]
                if cells and headers:
                    row_data = dict(zip(headers, cells))
                    rows.append(row_data)

        return rows

    def _extract_issue_composition(self) -> Dict[str, Any]:
        """Extract issue composition (Fresh Issue, OFS)"""
        composition = {}

        html_str = str(self.soup)

        # Fresh Issue
        fresh_pattern = r'fresh issue size of\s*₹\s*([\d,]+\.?\d*)\s*Cr'
        fresh_match = re.search(fresh_pattern, html_str, re.IGNORECASE)
        if fresh_match:
            composition['fresh_issue_cr'] = float(fresh_match.group(1).replace(',', ''))

        # Offer for Sale (OFS)
        ofs_pattern = r'Offer for sale being\s*₹\s*([\d,]+\.?\d*)\s*Cr'
        ofs_match = re.search(ofs_pattern, html_str, re.IGNORECASE)
        if ofs_match:
            composition['offer_for_sale_cr'] = float(ofs_match.group(1).replace(',', ''))

        return composition

    def _extract_documents(self) -> Dict[str, str]:
        """Extract document links (RHP, DRHP, etc.)"""
        documents = {}

        # RHP Link
        rhp_link = self.soup.find('a', href=re.compile(r'.*RHP\.pdf|.*Red_Herring.*\.pdf', re.IGNORECASE))
        if rhp_link and rhp_link.get('href'):
            documents['rhp_url'] = rhp_link['href']

        # DRHP Link
        drhp_link = self.soup.find('a', href=re.compile(r'.*DRHP\.pdf', re.IGNORECASE))
        if drhp_link and drhp_link.get('href'):
            documents['drhp_url'] = drhp_link['href']

        return documents

    def to_json(self, indent: int = 2) -> str:
        """
        Convert extracted data to JSON string

        Args:
            indent: Indentation level for pretty printing

        Returns:
            JSON string
        """
        if not self.data:
            self.extract_all()
        return json.dumps(self.data, indent=indent, ensure_ascii=False)

    def save_to_json(self, filepath: str, indent: int = 2):
        """
        Save extracted data to JSON file

        Args:
            filepath: Path to save JSON file
            indent: Indentation level for pretty printing
        """
        if not self.data:
            self.extract_all()

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=indent, ensure_ascii=False)

        print(f"✓ Data saved to {filepath}")

    def print_summary(self):
        """Print a formatted summary of extracted data"""
        if not self.data:
            self.extract_all()

        print("\n" + "="*80)
        print("IPO DATA EXTRACTION SUMMARY")
        print("="*80 + "\n")

        # Basic Info
        if self.data.get('basic_info'):
            print("📋 BASIC INFORMATION")
            print("-" * 40)
            for key, value in self.data['basic_info'].items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

        # Dates
        if self.data.get('dates'):
            print("📅 IMPORTANT DATES")
            print("-" * 40)
            for key, value in self.data['dates'].items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

        # Pricing
        if self.data.get('pricing'):
            print("💰 PRICING DETAILS")
            print("-" * 40)
            for key, value in self.data['pricing'].items():
                if isinstance(value, dict) and 'raw' in value:
                    print(f"  {key.replace('_', ' ').title()}: {value['raw']}")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

        # Financial Info
        if self.data.get('financial_info'):
            print("📊 FINANCIAL INFORMATION")
            print("-" * 40)
            for key, value in self.data['financial_info'].items():
                if isinstance(value, dict) and 'raw' in value:
                    print(f"  {key.replace('_', ' ').title()}: {value['raw']}")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

        # Company Info
        if self.data.get('company_info'):
            print("🏢 COMPANY INFORMATION")
            print("-" * 40)
            for key, value in self.data['company_info'].items():
                if key == 'description':
                    print(f"  {key.replace('_', ' ').title()}: {value[:100]}...")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

        # Stakeholders
        if self.data.get('stakeholders'):
            print("👥 STAKEHOLDERS")
            print("-" * 40)
            for key, value in self.data['stakeholders'].items():
                if isinstance(value, list):
                    print(f"  {key.replace('_', ' ').title()}:")
                    for item in value:
                        print(f"    - {item}")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

        print("="*80 + "\n")


if __name__ == "__main__":
    # Example usage
    print("IPO Data Extractor - Ready to use!")
    print("\nUsage:")
    print("  extractor = IPODataExtractor('index.html')")
    print("  data = extractor.extract_all()")
    print("  extractor.print_summary()")
    print("  extractor.save_to_json('ipo_data.json')")
