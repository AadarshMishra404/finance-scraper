#!/usr/bin/env python3
"""
IPO CLI - Command Line Interface for IPO Search System
Simple and easy-to-use commands
"""

import sys
import argparse
from ipo_index_builder import IPOIndexBuilder
from ipo_search_engine import IPOSearchEngine
from search_ipo import IPOSearchAndExtract


def build_index():
    """Build/rebuild the company index"""
    print("🔨 Building company index from ipoplatform.com...\n")
    builder = IPOIndexBuilder()
    builder.build_index()
    builder.save_index()
    print("\n✅ Index build complete!")


def search_company(query: str, interactive: bool = False):
    """Search for companies"""
    tool = IPOSearchAndExtract()

    if interactive:
        tool.interactive_search()
    else:
        results = tool.search_companies(query, limit=10)
        tool.search_engine.print_search_results(results)


def get_details(company_name: str, save: bool = True):
    """Get detailed IPO information for a company"""
    tool = IPOSearchAndExtract()
    tool.search_and_extract(company_name, save_json=save)


def list_categories():
    """List all available IPO categories"""
    engine = IPOSearchEngine()
    categories = engine.get_all_categories()

    print("\n📁 Available IPO Categories:")
    print("="*40)
    for cat in categories:
        count = len(engine.search_by_category(cat))
        print(f"  • {cat.title()}: {count} companies")
    print()


def show_stats():
    """Show index statistics"""
    engine = IPOSearchEngine()

    if not engine.companies:
        print("❌ No index found. Run: ipo_cli.py --build")
        return

    print("\n📊 IPO Index Statistics")
    print("="*40)
    print(f"  Total Companies: {len(engine.companies)}")

    categories = engine.get_all_categories()
    for cat in categories:
        count = len(engine.search_by_category(cat))
        print(f"  {cat.title()}: {count}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description='IPO Search & Extract CLI Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build/update the company index
  python3 ipo_cli.py --build

  # Search for companies
  python3 ipo_cli.py --search "Sudeep"

  # Get detailed info for a company
  python3 ipo_cli.py --details "Sudeep Pharma"

  # Interactive search mode
  python3 ipo_cli.py --interactive

  # Show statistics
  python3 ipo_cli.py --stats

  # List categories
  python3 ipo_cli.py --categories
        """
    )

    parser.add_argument('--build', action='store_true',
                        help='Build/rebuild the company index')

    parser.add_argument('--search', type=str, metavar='QUERY',
                        help='Search for companies by name')

    parser.add_argument('--details', type=str, metavar='COMPANY',
                        help='Get detailed IPO info for a company')

    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Start interactive search mode')

    parser.add_argument('--stats', action='store_true',
                        help='Show index statistics')

    parser.add_argument('--categories', action='store_true',
                        help='List all IPO categories')

    parser.add_argument('--no-save', action='store_true',
                        help='Don\'t save extracted data to JSON (use with --details)')

    args = parser.parse_args()

    # Show help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # Execute commands
    try:
        if args.build:
            build_index()

        elif args.search:
            search_company(args.search)

        elif args.details:
            get_details(args.details, save=not args.no_save)

        elif args.interactive:
            search_company('', interactive=True)

        elif args.stats:
            show_stats()

        elif args.categories:
            list_categories()

    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
