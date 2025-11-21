#!/usr/bin/env python3
"""
IPO Search Engine
Provides fuzzy search functionality for IPO companies
"""

import json
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


class IPOSearchEngine:
    """Search engine for IPO companies with fuzzy matching"""

    def __init__(self, index_file: str = 'companies_index.json'):
        """
        Initialize search engine with company index

        Args:
            index_file: Path to the companies index JSON file
        """
        self.companies = []
        self.load_index(index_file)

    def load_index(self, index_file: str):
        """Load the company index"""
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.companies = data.get('companies', [])
                print(f"✓ Search engine loaded with {len(self.companies)} companies")
        except FileNotFoundError:
            print(f"❌ Index file not found: {index_file}")
            print("   Run 'python3 ipo_index_builder.py' to build the index first.")
        except Exception as e:
            print(f"❌ Error loading index: {e}")

    def calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity score between two strings

        Returns:
            Float between 0 and 1 (1 = perfect match)
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def search(self, query: str, limit: int = 10, min_score: float = 0.3) -> List[Dict]:
        """
        Search for companies matching the query

        Args:
            query: Search query (company name)
            limit: Maximum number of results to return
            min_score: Minimum similarity score (0-1)

        Returns:
            List of matching companies with similarity scores
        """
        if not query or not self.companies:
            return []

        results = []

        for company in self.companies:
            # Calculate similarity score
            score = self.calculate_similarity(query, company['name'])

            # Also check if query is a substring (partial match)
            if query.lower() in company['name'].lower():
                score = max(score, 0.6)  # Boost substring matches

            if score >= min_score:
                result = company.copy()
                result['match_score'] = score
                results.append(result)

        # Sort by score (descending)
        results.sort(key=lambda x: x['match_score'], reverse=True)

        return results[:limit]

    def search_by_id(self, company_id: str) -> Dict:
        """Search for a company by its ID"""
        for company in self.companies:
            if company['id'] == company_id:
                return company
        return None

    def search_by_slug(self, slug: str) -> Dict:
        """Search for a company by its slug"""
        for company in self.companies:
            if company['slug'] == slug:
                return company
        return None

    def search_by_category(self, category: str) -> List[Dict]:
        """Get all companies in a specific category"""
        return [c for c in self.companies if c.get('category', '').lower() == category.lower()]

    def get_all_categories(self) -> List[str]:
        """Get list of all available categories"""
        categories = set()
        for company in self.companies:
            if 'category' in company:
                categories.add(company['category'])
        return sorted(list(categories))

    def print_search_results(self, results: List[Dict]):
        """Print search results in a formatted way"""
        if not results:
            print("\n❌ No companies found matching your search.")
            return

        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS ({len(results)} found)")
        print(f"{'='*80}\n")

        for i, company in enumerate(results, 1):
            score = company.get('match_score', 0)
            score_bar = '█' * int(score * 10)

            print(f"{i}. {company['name']}")
            print(f"   Category: {company.get('category', 'N/A')} | ID: {company['id']}")
            print(f"   Match: {score_bar} {score:.2%}")
            print(f"   URL: {company['url']}")
            print()


def main():
    """Demo function"""
    print("="*80)
    print("IPO SEARCH ENGINE - Demo")
    print("="*80)

    # Initialize search engine
    engine = IPOSearchEngine()

    if not engine.companies:
        print("\n⚠️  No index found. Please run:")
        print("   python3 ipo_index_builder.py")
        return

    # Example searches
    test_queries = ['Sudeep', 'Pharma', 'ICICI']

    for query in test_queries:
        print(f"\n🔍 Searching for: '{query}'")
        results = engine.search(query, limit=3)
        engine.print_search_results(results)


if __name__ == "__main__":
    main()
