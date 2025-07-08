import os
import json

def format_news(news_path, output_path):
    """
    MIND news.tsv를 읽어서 뉴스 컨텐츠를 포맷팅하고 저장합니다.
    포맷 예시:
    News Title: <title>; News Abstract: <abstract>; News Category: <category>.
    """
    formatted_news = {}

    with open(news_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 5:
                continue
            news_id = parts[0]
            category = parts[1]
            title = parts[3]
            abstract = parts[4]

            # 포맷팅된 텍스트 생성
            text = f"News Title: {title}; News Abstract: {abstract}; News Category: {category}."
            formatted_news[news_id] = text

    # JSON으로 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(formatted_news, out_f, ensure_ascii=False, indent=2)

    print(f"[Saved] Formatted news → {output_path}")