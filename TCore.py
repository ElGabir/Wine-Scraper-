"""
Core scraping library for TeaScraper.
Gathers metadata, title, headings, links, images, files, and main visible text from a page.
Saves to an output folder (created for each run).
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def download_file(url, folder):
    """
    Downloads a file (image, pdf, etc.) from `url` to `folder`.
    Returns the path or an error message.
    """
    try:
        resp = requests.get(url, stream=True, timeout=15)
        resp.raise_for_status()
        fname = os.path.basename(urlparse(url).path)
        if not fname:
            fname = "file"
        local_path = os.path.join(folder, fname)
        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(4096):
                f.write(chunk)
        return local_path
    except Exception as e:
        return f"Failed to download {url}: {e}"

def limitless_scrape(url, out_dir):
    """
    Main function that scrapes the provided `url` and stores all
    artifacts and summary info in `out_dir`.
    """
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        with open(os.path.join(out_dir, "info.txt"), "w", encoding="utf-8") as f:
            f.write(f"Failed to fetch URL: {url}\nError: {e}")
        return

    soup = BeautifulSoup(resp.content, "html.parser")
    report = []
    report.append(f"URL: {url}\nStatus code: {resp.status_code}\n")

    # All Meta tags
    metas = soup.find_all('meta')
    if metas:
        report.append("Meta tags:")
        for tag in metas:
            name = tag.get('name') or tag.get('property') or ''
            content = tag.get('content', '')
            report.append(f"  - {name}: {content}")
        report.append("")

    # Page title
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    report.append(f"Title: {title}\n")

    # All headings h1–h6
    for h in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        heads = [tag.get_text(strip=True) for tag in soup.find_all(h)]
        if heads:
            report.append(f"{h.upper()} tags:")
            report.extend([f"  - {t}" for t in heads])
            report.append("")

    # All links
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    if links:
        report.append(f"Links ({len(links)}):")
        report.extend([f"  - {l}" for l in links])
        report.append("")

    # All images
    images = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]
    if images:
        report.append(f"Images ({len(images)}):")
        img_dir = os.path.join(out_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        for img_url in images:
            local_img = download_file(img_url, img_dir)
            report.append(f"  - {img_url}  -->  {local_img}")
        report.append("")

    # Download all PDFs and document files linked on the page
    files = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if any(a['href'].lower().endswith(ext)
                for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx'])]
    if files:
        file_dir = os.path.join(out_dir, "downloads")
        os.makedirs(file_dir, exist_ok=True)
        report.append(f"File downloads ({len(files)}):")
        for f_url in files:
            local_file = download_file(f_url, file_dir)
            report.append(f"  - {f_url}  -->  {local_file}")
        report.append("")

    # All visible text (remove scripts, styles, nav, etc.)
    for t in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        t.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [l for l in text.splitlines() if l]
    report.append("\n" + "=" * 30)
    report.append(f"VISIBLE TEXT ({len(lines)} lines):\n")
    report.extend(lines)
    report.append("\n--- END ---\n")

    # Save report
    with open(os.path.join(out_dir, "info.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report))
