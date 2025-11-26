# TeaScraper (Limitless AI Web Scraper)

**TeaScraper** is a limitless AI web scraper.  
Paste any URL and this tool will extract:
- All metadata (`<meta>` tags)
- Title
- All headings (h1–h6)
- All links (`href`s)
- All images (and downloads them)
- Downloadable doc files (PDF, DOC, etc.)
- All visible page text

Results are saved into a timestamped folder with the page content and all resources.

---

## Quickstart

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2. **Run TeaScraper:**
    ```bash
    python -m TeaScraper.tea_scraper
    ```
3. **Paste a target URL when prompted.**

4. **Check the created `run_YYYYmmdd-HHMMSS/` folder for results.**

---

## Sample Output

- `info.txt` — The main summary/report.
- `/images/` — Downloaded images.
- `/downloads/` — Downloaded files such as PDFs.

---

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

---

> **Use TeaScraper only on pages you are legally allowed to scrape. Educational only!**
