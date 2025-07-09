import os
import json

def split_sessions(behaviors_path, output_path, max_history=60, session_size=10):
    """
    MIND behaviors.tsv를 읽어서 사용자별 세션을 분리하고 저장합니다.
    각 사용자의 클릭 히스토리를 최신순으로 최대 max_history까지 유지하며,
    session_size 단위로 세션을 나눕니다.
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

            if user_id not in user_sessions:
                user_sessions[user_id] = []
            user_sessions[user_id].extend(clicked_news)
            user_sessions[user_id] = user_sessions[user_id][-max_history:]

    # 세션 단위로 분할
    user_sessions_partitioned = {}
    for user_id, clicks in user_sessions.items():
        sessions = []
        for i in range(0, len(clicks), session_size):
            sessions.append(clicks[i:i+session_size])
        user_sessions_partitioned[user_id] = sessions

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(user_sessions_partitioned, out_f, ensure_ascii=False, indent=2)

    print(f"[Saved] User sessions with partition → {output_path}")

