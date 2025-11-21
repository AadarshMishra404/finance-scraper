#!/usr/bin/env python3
"""
Example script to extract IPO data from HTML file
"""

from ipo_data_extractor import IPODataExtractor
import sys


def main():
    """Main function to demonstrate IPO data extraction"""

    # Path to the HTML file
    html_file = 'index.html'

    print("="*80)
    print("IPO DATA EXTRACTOR - Sudeep Pharma IPO")
    print("="*80)
    print(f"\n📂 Loading HTML file: {html_file}")

    try:
        # Initialize the extractor
        extractor = IPODataExtractor(html_file)

        print("✓ HTML file loaded successfully")
        print("\n🔍 Extracting IPO data...\n")

        # Extract all data
        data = extractor.extract_all()

        # Print summary to console
        extractor.print_summary()

        # Save to JSON file
        output_file = 'sudeep_pharma_ipo_data.json'
        extractor.save_to_json(output_file)

        # Print quick stats
        print("\n📈 EXTRACTION STATISTICS")
        print("-" * 40)
        print(f"  Total sections extracted: {len(data)}")
        print(f"  Basic info fields: {len(data.get('basic_info', {}))}")
        print(f"  Date fields: {len(data.get('dates', {}))}")
        print(f"  Pricing fields: {len(data.get('pricing', {}))}")
        print(f"  Financial fields: {len(data.get('financial_info', {}))}")
        print(f"  Company info fields: {len(data.get('company_info', {}))}")
        print(f"  Stakeholder fields: {len(data.get('stakeholders', {}))}")

        print(f"\n✅ Extraction complete! Data saved to: {output_file}")
        print("\n" + "="*80)

    except FileNotFoundError:
        print(f"❌ Error: File '{html_file}' not found!")
        print("Please make sure the HTML file exists in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
