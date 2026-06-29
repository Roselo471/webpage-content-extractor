import pandas as pd
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

BLOCKED_PATHS = ['/feed/', '/wp-includes/', '/wp-content/']
BLOCKED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.js', '.css', '.svg', '.ico', '.pdf', '.webp'}
MAX_URLS = 300

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    # 检查路径是否含屏蔽关键词
    for blocked in BLOCKED_PATHS:
        if blocked in parsed.path:
            return False
    # 检查扩展名
    path = parsed.path.lower()
    for ext in BLOCKED_EXTENSIONS:
        if path.endswith(ext):
            return False
    return True

def load_and_filter(input_csv: str) -> list[str]:
    df = pd.read_csv(input_csv)
    
    # 自动识别URL列（列名含'url'，不区分大小写）
    url_col = next((col for col in df.columns if 'url' in col.lower()), None)
    if url_col is None:
        raise ValueError("CSV里找不到URL列，请确保列名包含'url'")
    
    all_urls = df[url_col].dropna().tolist()
    logger.info(f"读取到 {len(all_urls)} 条URL")
    
    valid_urls = [url for url in all_urls if is_valid_url(url)]
    filtered_count = len(all_urls) - len(valid_urls)
    if filtered_count > 0:
        logger.info(f"过滤掉 {filtered_count} 条无效URL")
    
    # 硬上限检查
    if len(valid_urls) > MAX_URLS:
        logger.warning(f"URL数量({len(valid_urls)})超过上限{MAX_URLS}，截断处理")
        valid_urls = valid_urls[:MAX_URLS]
    
    logger.info(f"最终有效URL：{len(valid_urls)} 条")
    return valid_urls