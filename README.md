# webpage-content-extractor

A Python command-line tool that reads a list of URLs, crawls each page, and extracts structured content into a CSV file.

Built for freelance delivery: give it a URL list, get back a clean CSV with titles, meta tags, headings, Markdown body content, and internal link maps.

---

## Features

- Extracts per URL: `title`, `meta description`, `H1`, `H2s`, body text as Markdown, and internal links with anchor texts
- Filters out WordPress noise (`/feed/`, `/wp-includes/`, `/wp-content/`, static assets)
- Polite crawling: random delay of 0.5–2 seconds between requests
- Graceful failure: if a URL is unreachable, logs the error and continues — no crashes
- Hard cap of 300 URLs with a warning if exceeded

---

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py --input urls.csv --output results.csv
```

| Argument | Description |
|---|---|
| `--input` | Path to your input CSV file containing URLs |
| `--output` | Path where the results CSV will be saved |

---

## Input Format

Your input CSV **must have a header row**. The column containing URLs must have `url` somewhere in its name (case-insensitive), e.g. `url`, `URL`, `page_url`.

**Correct format:**

```
url
https://example.com/page-one
https://example.com/page-two
https://example.com/page-three
```

> ⚠️ **Common mistake:** If your CSV has no header row, the tool will treat the first URL as the column name and skip it. Always add a `url` header as the first row.

---

## Output Format

The output CSV contains one row per URL:

| Column | Description |
|---|---|
| `url` | The page URL |
| `title` | Page `<title>` tag content |
| `meta_description` | `<meta name="description">` content |
| `h1` | First `<h1>` tag |
| `h2s` | All `<h2>` tags, separated by ` \| ` |
| `markdown_content` | Body text converted to Markdown (nav/header/footer removed) |
| `internal_links` | Internal links in `anchor text::target URL` format, separated by ` \| ` |

If a URL fails to load, its row will still appear in the output with all fields empty except `url`.

---

## URL Filtering

The following URLs are automatically skipped and will not appear in the output:

- Paths containing `/feed/`, `/wp-includes/`, `/wp-content/`
- Static file extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.js`, `.css`, `.svg`, `.ico`, `.pdf`, `.webp`

---

## Project Structure

```
webpage-content-extractor/
├── main.py           # Entry point, orchestrates the pipeline
├── url_filter.py     # Reads and filters the input URL list
├── fetcher.py        # HTTP requests with retry and delay
├── parser.py         # HTML parsing and content extraction
├── requirements.txt
└── README.md
```

---

## Dependencies

| Library | Purpose |
|---|---|
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing |
| `markdownify` | HTML to Markdown conversion |
| `pandas` | CSV reading and writing |

---

## Limitations

- Does not handle JavaScript-rendered pages (static HTML only)
- Does not handle login walls or CAPTCHAs
- Does not auto-discover URLs — requires a pre-prepared URL list as input
