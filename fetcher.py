import requests
import time
import random
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
TIMEOUT = 10

def fetch(url: str) -> str | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"爬取失败 {url}: {e}")
        return None
    finally:
        # 无论成功失败都延时，避免请求过快
        time.sleep(random.uniform(0.5, 2.0))