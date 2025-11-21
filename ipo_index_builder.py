#!/usr/bin/env python3
"""
IPO Index Builder
Scrapes ipoplatform.com listing pages to build a searchable index of all IPO companies
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict
import time


class IPOIndexBuilder:
    """Builds and maintains a searchable index of IPO companies"""

    BASE_URL = "https://www.ipoplatform.com"

    # Different IPO categories to scrape
    CATEGORIES = {
        'mainboard': '/list-of-mainboard-ipos',
        'sme': '/list-of-sme-ipos',
        'upcoming': '/upcoming-mainboard-ipo',
    }

    def __init__(self):
        self.companies = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a webpage"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None

    def extract_company_from_link(self, link_tag) -> Dict:
        """Extract company information from an IPO link"""
        try:
            href = link_tag.get('href', '')

            # Pattern: /ipo/company-name-ipo/1234 or full URL
            match = re.search(r'/ipo/([^/]+)/(\d+)', href)
            if not match:
                return None

            slug = match.group(1)
            company_id = match.group(2)

            # Extract company name from link text or title
            company_name = link_tag.get_text(strip=True)

            # Clean up company name (remove "IPO" suffix if present)
            company_name = re.sub(r'\s+IPO\s*$', '', company_name, flags=re.IGNORECASE)

            if not company_name:
                # Try to get from title attribute
                company_name = link_tag.get('title', '').replace(' IPO', '')

            if company_name and slug and company_id:
                return {
                    'name': company_name.strip(),
                    'slug': slug,
                    'id': company_id,
                    'url': f"{self.BASE_URL}/ipo/{slug}/{company_id}"
                }
        except Exception as e:
            print(f"Warning: Error extracting company info: {e}")

        return None

    def scrape_category(self, category_name: str, category_path: str) -> List[Dict]:
        """Scrape all companies from a category"""
        print(f"\n🔍 Scraping {category_name} IPOs...")

        url = f"{self.BASE_URL}{category_path}"
        soup = self.fetch_page(url)

        if not soup:
            return []

        companies = []

        # Find all IPO links - they typically have href="/ipo/company-name/id"
        # Try both absolute and relative URLs
        ipo_links = soup.find_all('a', href=re.compile(r'(/ipo/|https://www\.ipoplatform\.com/ipo/)[^/]+/\d+'))

        print(f"  Found {len(ipo_links)} IPO links on page")

        seen = set()  # To avoid duplicates

        for link in ipo_links:
            company = self.extract_company_from_link(link)
            if company:
                # Use ID as unique identifier
                if company['id'] not in seen:
                    company['category'] = category_name
                    companies.append(company)
                    seen.add(company['id'])
                    print(f"  ✓ {company['name']} (ID: {company['id']})")

        print(f"  Found {len(companies)} companies in {category_name}")
        return companies

    def build_index(self) -> List[Dict]:
        """Build complete index by scraping all categories"""
        print("="*80)
        print("BUILDING IPO COMPANY INDEX")
        print("="*80)

        all_companies = []

        for category_name, category_path in self.CATEGORIES.items():
            companies = self.scrape_category(category_name, category_path)
            all_companies.extend(companies)

            # Be nice to the server
            time.sleep(1)

        # Remove duplicates based on ID
        unique_companies = {}
        for company in all_companies:
            unique_companies[company['id']] = company

        self.companies = list(unique_companies.values())

        print(f"\n{'='*80}")
        print(f"✅ Index built successfully!")
        print(f"   Total unique companies: {len(self.companies)}")
        print(f"{'='*80}\n")

        return self.companies

    def save_index(self, filepath: str = 'companies_index.json'):
        """Save the index to a JSON file"""
        if not self.companies:
            print("⚠️  No companies to save. Build index first.")
            return

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'total_companies': len(self.companies),
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'companies': self.companies
            }, f, indent=2, ensure_ascii=False)

        print(f"💾 Index saved to {filepath}")

    def load_index(self, filepath: str = 'companies_index.json') -> List[Dict]:
        """Load index from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.companies = data.get('companies', [])
                print(f"✓ Loaded {len(self.companies)} companies from {filepath}")
                print(f"  Last updated: {data.get('last_updated', 'Unknown')}")
                return self.companies
        except FileNotFoundError:
            print(f"❌ Index file not found: {filepath}")
            return []
        except Exception as e:
            print(f"❌ Error loading index: {e}")
            return []

    def get_company_by_id(self, company_id: str) -> Dict:
        """Get company information by ID"""
        for company in self.companies:
            if company['id'] == company_id:
                return company
        return None

    def get_company_by_slug(self, slug: str) -> Dict:
        """Get company information by slug"""
        for company in self.companies:
            if company['slug'] == slug:
                return company
        return None


def main():
    """Main function to build and save the index"""
    builder = IPOIndexBuilder()

    # Build the index
    companies = builder.build_index()

    # Save to file
    builder.save_index('companies_index.json')

    # Show some sample companies
    if companies:
        print("\n📋 Sample companies:")
        for company in companies[:5]:
            print(f"  • {company['name']} ({company['category']}) - {company['url']}")


if __name__ == "__main__":
    main()
