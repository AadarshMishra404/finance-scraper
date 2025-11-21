#!/usr/bin/env python3
"""
IPO Search & Extract Tool
Search for IPO companies and extract their detailed information
"""

import sys
import requests
from ipo_search_engine import IPOSearchEngine
from ipo_data_extractor import IPODataExtractor
import json


class IPOSearchAndExtract:
    """Main class that combines search and data extraction"""

    def __init__(self):
        self.search_engine = IPOSearchEngine()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_company_html(self, url: str) -> str:
        """Fetch HTML content from company URL"""
        try:
            print(f"📥 Fetching data from: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            print("✓ Data fetched successfully")
            return response.text
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None

    def search_companies(self, query: str, limit: int = 10) -> list:
        """Search for companies matching query"""
        return self.search_engine.search(query, limit=limit)

    def get_company_details(self, company: dict, save_json: bool = False) -> dict:
        """
        Get detailed IPO information for a company

        Args:
            company: Company dict with 'url' key
            save_json: Whether to save extracted data to JSON file

        Returns:
            Extracted IPO data dictionary
        """
        html_content = self.fetch_company_html(company['url'])

        if not html_content:
            return None

        print("\n🔍 Extracting IPO data...\n")

        # Extract data using IPODataExtractor
        extractor = IPODataExtractor(html_content)
        data = extractor.extract_all()

        # Print summary
        extractor.print_summary()

        # Save to JSON if requested
        if save_json:
            filename = f"{company['slug']}_data.json"
            extractor.save_to_json(filename)

        return data

    def interactive_search(self):
        """Interactive search mode"""
        if not self.search_engine.companies:
            print("\n❌ No company index found!")
            print("   Please run: python3 ipo_index_builder.py")
            return

        print("="*80)
        print("IPO COMPANY SEARCH & EXTRACT")
        print("="*80)
        print("\nType 'quit' or 'exit' to quit\n")

        while True:
            try:
                query = input("🔍 Enter company name to search: ").strip()

                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                if not query:
                    continue

                # Search for companies
                results = self.search_companies(query, limit=10)

                if not results:
                    print("\n❌ No companies found. Try a different search term.\n")
                    continue

                # Display results
                print(f"\n{'='*80}")
                print(f"Found {len(results)} matching companies:")
                print(f"{'='*80}\n")

                for i, company in enumerate(results, 1):
                    score = company.get('match_score', 0)
                    print(f"{i}. {company['name']} ({company.get('category', 'N/A')})")
                    print(f"   Match: {'█' * int(score * 10)} {score:.1%} | ID: {company['id']}")

                print(f"\n{'='*80}")

                # Let user select
                selection = input("\n📌 Select a company (number) or press Enter to search again: ").strip()

                if not selection:
                    continue

                try:
                    index = int(selection) - 1
                    if 0 <= index < len(results):
                        selected = results[index]
                        print(f"\n✓ Selected: {selected['name']}")

                        # Ask if user wants to save to JSON
                        save = input("💾 Save to JSON file? (y/n): ").strip().lower()
                        save_json = save == 'y'

                        # Get detailed information
                        self.get_company_details(selected, save_json=save_json)

                        # Ask if user wants to continue
                        cont = input("\n🔍 Search for another company? (y/n): ").strip().lower()
                        if cont != 'y':
                            print("\n👋 Goodbye!")
                            break
                    else:
                        print("❌ Invalid selection")
                except ValueError:
                    print("❌ Please enter a valid number")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()

    def search_and_extract(self, company_name: str, save_json: bool = True):
        """
        Non-interactive: Search for a company and extract its data

        Args:
            company_name: Company name to search for
            save_json: Whether to save to JSON file

        Returns:
            Extracted data or None
        """
        # Search
        results = self.search_companies(company_name, limit=5)

        if not results:
            print(f"❌ No companies found matching '{company_name}'")
            return None

        # Use best match
        best_match = results[0]
        print(f"\n✓ Best match: {best_match['name']} (Score: {best_match['match_score']:.1%})")

        # Extract details
        return self.get_company_details(best_match, save_json=save_json)


def main():
    """Main entry point"""
    tool = IPOSearchAndExtract()

    # Check if company name provided as argument
    if len(sys.argv) > 1:
        company_name = ' '.join(sys.argv[1:])
        print(f"Searching for: {company_name}\n")
        tool.search_and_extract(company_name, save_json=True)
    else:
        # Interactive mode
        tool.interactive_search()


if __name__ == "__main__":
    main()
