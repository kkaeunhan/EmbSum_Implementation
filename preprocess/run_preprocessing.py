import os
from preprocess.news_formatter import format_news
from preprocess.session_splitter import split_sessions

def preprocess_mind_dataset(base_dir, output_dir, max_history=60, session_size=10):
    news_path = os.path.join(base_dir, "news.tsv")
    behaviors_path = os.path.join(base_dir, "behaviors.tsv")
    formatted_news_path = os.path.join(output_dir, "formatted_news.json")
    user_sessions_path = os.path.join(output_dir, "user_sessions.json")

    print(f"=== Preprocessing: {base_dir} ===")
    format_news(news_path, formatted_news_path)
    split_sessions(behaviors_path, user_sessions_path, max_history=max_history, session_size=session_size)
    print(f"=== Done: Preprocessing outputs saved in {output_dir} ===\n")

if __name__ == "__main__":
    BASE_INPUT_DIR = "data"
    BASE_OUTPUT_DIR = "output"

    # Train 데이터 처리
    preprocess_mind_dataset(
        base_dir=os.path.join(BASE_INPUT_DIR, "MINDsmall_train"),
        output_dir=os.path.join(BASE_OUTPUT_DIR, "MINDsmall_train"),
        max_history=60,
        session_size=10
    )

    # Dev 데이터 처리
    preprocess_mind_dataset(
        base_dir=os.path.join(BASE_INPUT_DIR, "MINDsmall_dev"),
        output_dir=os.path.join(BASE_OUTPUT_DIR, "MINDsmall_dev"),
        max_history=60,
        session_size=10
    )
