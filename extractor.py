#!/usr/bin/env python3
"""
Generic XPath Extractor
Extracts data from HTML files using XPath expressions and saves results
"""

import argparse
import json
import os
from lxml import html, etree
from typing import List, Dict, Any, Union
from datetime import datetime


class XPathExtractor:
    """Generic HTML extractor using XPath"""

    def __init__(self, html_file: str, output_dir: str = 'result'):
        """
        Initialize the extractor

        Args:
            html_file: Path to HTML file
            output_dir: Directory to save results (default: 'result')
        """
        self.html_file = html_file
        self.output_dir = output_dir
        self.tree = None
        self.results = {}

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Load and parse HTML
        self._load_html()

    def _load_html(self):
        """Load and parse the HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.tree = html.fromstring(content)
            print(f"✓ Loaded HTML file: {self.html_file}")
        except FileNotFoundError:
            print(f"❌ Error: File not found: {self.html_file}")
            raise
        except Exception as e:
            print(f"❌ Error loading HTML: {e}")
            raise

    def extract(self, xpath: str, label: str = None) -> List[str]:
        """
        Extract data using XPath expression

        Args:
            xpath: XPath expression
            label: Optional label for the extracted data

        Returns:
            List of extracted text values
        """
        if not self.tree:
            print("❌ HTML not loaded")
            return []

        try:
            # Extract elements using XPath
            elements = self.tree.xpath(xpath)

            # Convert elements to text
            results = []
            for elem in elements:
                if isinstance(elem, str):
                    # Already a string (from text() or @attribute)
                    results.append(elem.strip())
                elif hasattr(elem, 'text_content'):
                    # Element node - get text content
                    text = elem.text_content().strip()
                    if text:
                        results.append(text)
                else:
                    # Try to convert to string
                    results.append(str(elem).strip())

            # Store results with label
            key = label if label else xpath
            self.results[key] = results

            print(f"✓ Extracted {len(results)} item(s) from: {xpath[:60]}...")
            return results

        except etree.XPathEvalError as e:
            print(f"❌ Invalid XPath expression: {e}")
            return []
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return []

    def extract_multiple(self, xpath_dict: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Extract data using multiple XPath expressions

        Args:
            xpath_dict: Dictionary mapping labels to XPath expressions
                       Example: {'title': '//h1', 'price': '//span[@class="price"]'}

        Returns:
            Dictionary mapping labels to extracted values
        """
        results = {}
        for label, xpath in xpath_dict.items():
            results[label] = self.extract(xpath, label)
        return results

    def print_results(self):
        """Print extraction results in a formatted way"""
        if not self.results:
            print("\n⚠️  No results to display")
            return

        print("\n" + "="*80)
        print("EXTRACTION RESULTS")
        print("="*80 + "\n")

        for label, values in self.results.items():
            print(f"📋 {label}")
            print("-" * 40)
            if values:
                for i, value in enumerate(values, 1):
                    # Truncate long values
                    display_value = value if len(value) <= 100 else value[:100] + "..."
                    print(f"  {i}. {display_value}")
            else:
                print("  (No data found)")
            print()

        print("="*80 + "\n")

    def save_to_json(self, filename: str = None):
        """
        Save results to JSON file in output directory

        Args:
            filename: Output filename (default: auto-generated)
        """
        if not self.results:
            print("⚠️  No results to save")
            return

        if not filename:
            # Auto-generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = os.path.splitext(os.path.basename(self.html_file))[0]
            filename = f"{base_name}_extracted_{timestamp}.json"

        output_path = os.path.join(self.output_dir, filename)

        # Prepare data for JSON
        json_data = {
            'source_file': self.html_file,
            'extraction_time': datetime.now().isoformat(),
            'total_fields': len(self.results),
            'data': self.results
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Results saved to: {output_path}")
        return output_path

    def save_to_txt(self, filename: str = None):
        """
        Save results to text file in output directory

        Args:
            filename: Output filename (default: auto-generated)
        """
        if not self.results:
            print("⚠️  No results to save")
            return

        if not filename:
            # Auto-generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = os.path.splitext(os.path.basename(self.html_file))[0]
            filename = f"{base_name}_extracted_{timestamp}.txt"

        output_path = os.path.join(self.output_dir, filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("EXTRACTION RESULTS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Source File: {self.html_file}\n")
            f.write(f"Extraction Time: {datetime.now().isoformat()}\n")
            f.write(f"Total Fields: {len(self.results)}\n\n")

            for label, values in self.results.items():
                f.write(f"\n{'='*80}\n")
                f.write(f"{label}\n")
                f.write(f"{'-'*80}\n")
                if values:
                    for i, value in enumerate(values, 1):
                        f.write(f"{i}. {value}\n")
                else:
                    f.write("(No data found)\n")

        print(f"💾 Results saved to: {output_path}")
        return output_path


def main():
    """CLI interface for the extractor"""
    parser = argparse.ArgumentParser(
        description='Generic XPath Extractor - Extract data from HTML files using XPath',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract single XPath
  python3 extractor.py info/main1.html --xpath '//*[@id="financial"]/div[3]//h2'

  # Extract with custom label
  python3 extractor.py info/main1.html --xpath '//h2' --label 'Headings'

  # Save to custom output directory
  python3 extractor.py info/main1.html --xpath '//h2' --output data/

  # Save as text file
  python3 extractor.py info/main1.html --xpath '//h2' --format txt

  # Interactive mode (enter multiple XPaths)
  python3 extractor.py info/main1.html --interactive
        """
    )

    parser.add_argument('html_file', help='Path to HTML file')
    parser.add_argument('--xpath', '-x', help='XPath expression to extract')
    parser.add_argument('--label', '-l', help='Label for extracted data')
    parser.add_argument('--output', '-o', default='result', help='Output directory (default: result)')
    parser.add_argument('--format', '-f', choices=['json', 'txt', 'both'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive mode - enter multiple XPaths')
    parser.add_argument('--filename', help='Custom output filename')

    args = parser.parse_args()

    try:
        # Initialize extractor
        extractor = XPathExtractor(args.html_file, args.output)

        if args.interactive:
            # Interactive mode
            print("\n" + "="*80)
            print("INTERACTIVE XPATH EXTRACTION MODE")
            print("="*80)
            print("\nEnter XPath expressions (or 'done' to finish):")
            print("Format: label=xpath  OR  just xpath\n")

            while True:
                user_input = input("XPath: ").strip()

                if user_input.lower() in ['done', 'quit', 'exit', '']:
                    break

                # Parse input
                if '=' in user_input:
                    label, xpath = user_input.split('=', 1)
                    label = label.strip()
                    xpath = xpath.strip()
                else:
                    xpath = user_input
                    label = None

                # Extract
                extractor.extract(xpath, label)

        elif args.xpath:
            # Single XPath extraction
            extractor.extract(args.xpath, args.label)
        else:
            print("❌ Error: Please provide --xpath or use --interactive mode")
            parser.print_help()
            return

        # Display results
        extractor.print_results()

        # Save results
        if args.format in ['json', 'both']:
            extractor.save_to_json(args.filename)

        if args.format in ['txt', 'both']:
            txt_filename = args.filename.replace('.json', '.txt') if args.filename else None
            extractor.save_to_txt(txt_filename)

    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
