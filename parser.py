from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urljoin, urlparse

def parse(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    base_domain = urlparse(base_url).netloc

    # Title
    title = soup.title.string.strip() if soup.title else ''

    # Meta description
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_tag['content'].strip() if meta_tag and meta_tag.get('content') else ''

    # H1（取第一个）
    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text(strip=True) if h1_tag else ''

    # H2（全部）
    h2s = ' | '.join(tag.get_text(strip=True) for tag in soup.find_all('h2'))

    # 正文转Markdown（先移除干扰元素）
    for tag in soup.find_all(['nav', 'header', 'footer', 'script', 'style']):
        tag.decompose()
    body = soup.find('body')
    markdown_content = md(str(body), heading_style='ATX') if body else ''

    # 内链
    internal_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        anchor_text = a_tag.get_text(strip=True)
        if urlparse(full_url).netloc == base_domain and anchor_text:
            internal_links.append(f"{anchor_text}::{full_url}")
    internal_links_str = ' | '.join(internal_links)

    return {
        'title': title,
        'meta_description': meta_description,
        'h1': h1,
        'h2s': h2s,
        'markdown_content': markdown_content,
        'internal_links': internal_links_str,
    }