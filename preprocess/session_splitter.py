import os
import json

def split_sessions(behaviors_path, output_path, max_history=60):
    """
    MIND behaviors.tsv를 읽어서 사용자별 세션을 분리하고 저장합니다.
    각 사용자의 클릭 히스토리를 최신순으로 최대 max_history까지 유지합니다.
    """
    user_sessions = {}

    with open(behaviors_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 5:
                continue
            user_id = parts[1]
            impressions = parts[4].split(' ')
            clicked_news = [imp.split('-')[0] for imp in impressions if imp.endswith('-1')]
            if not clicked_news:
                continue

            # 사용자 세션에 추가 (최신순 유지)
            if user_id not in user_sessions:
                user_sessions[user_id] = []
            user_sessions[user_id].extend(clicked_news)
            user_sessions[user_id] = user_sessions[user_id][-max_history:]

    # JSON으로 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(user_sessions, out_f, ensure_ascii=False, indent=2)

    print(f"[Saved] User sessions → {output_path}")
