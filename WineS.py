import os
import time
from .tea_scraper_core import limitless_scrape

def print_banner():
    banner = r"""
████████╗███████╗ █████╗     ███████╗████████╗ █████╗ ██████╗ ██████╗ ███████╗██████╗ 
╚══██╔══╝██╔════╝██╔══██╗    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
   ██║   █████╗  ███████║    █████╗     ██║   ███████║██████╔╝██████╔╝█████╗  ██████╔╝
   ██║   ██╔══╝  ██╔══██║    ██╔══╝     ██║   ██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
   ██║   ███████╗██║  ██║    ██║        ██║   ██║  ██║██║  ██║██║  ██║███████╗██║  ██║
   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

                    Limitless AI Web Scraper — github.com/ElGabir/TeaScraper

        ░░ Paste your target URL and let the tea pour in... Happy scraping! ░░
    """
    print(banner)

def main():
    """Entry point for TeaScraper. Asks for URL and scrapes the website."""

    print_banner()  # Show the banner when the script runs

    url = input("Paste the target URL: ").strip()
    if not url:
        print("You must enter a URL.")
        return

    # Create output directory with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = f"run_{timestamp}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"Scraping {url} ...")
    limitless_scrape(url, out_dir)
    print(f"\nAll results, including info, links, metadata, images (and files) are saved in: {out_dir}")

if __name__ == "__main__":
    main()
