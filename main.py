import argparse
import csv
import logging
from url_filter import load_and_filter
from fetcher import fetch
from parser import parse

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

FIELDNAMES = ['url', 'title', 'meta_description', 'h1', 'h2s', 'markdown_content', 'internal_links']

def main():
    parser = argparse.ArgumentParser(description='网站文本爬取工具')
    parser.add_argument('--input', required=True, help='输入CSV路径')
    parser.add_argument('--output', required=True, help='输出CSV路径')
    args = parser.parse_args()

    urls = load_and_filter(args.input)
    total = len(urls)
    success, failed = 0, 0

    with open(args.output, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{total}] 爬取中：{url}")
            html = fetch(url)
            if html is None:
                failed += 1
                writer.writerow({'url': url, **{k: '' for k in FIELDNAMES[1:]}})
                continue
            result = parse(html, url)
            writer.writerow({'url': url, **result})
            success += 1

    logger.info(f"\n完成！成功：{success} 条，失败：{failed} 条")
    logger.info(f"结果已保存到：{args.output}")

if __name__ == '__main__':
    main()