import os
import json
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def build_prompt(news_texts):
    prompt = (
        "[INST] You are a news recommendation assistant. "
        "To help the ranking system recommend more relevant news to users, "
        "your task is to identify user interests based on user's news engagement history.\n"
        "You are asked to summarize user interest based on his/her browsed news history list. "
        "Each browsed news is in a line and contains news title, abstract and category name.\n"
        "### Input\n"
        "History of user browsed news\n"
    )
    for i, news in enumerate(news_texts, 1):
        prompt += f"{i}. {news}\n"
    prompt += (
        "### Task Requirement\n"
        "Now, please provide a concise and accurate summary of the user's news interests in three sentences. "
        "You do not need to give particular examples. [/INST]\n"
        "Summary of user interest:"
    )
    return prompt

def main(
    formatted_news_path,
    user_sessions_path,
    output_path,
    model_name="meta-llama/Meta-Llama-3-8B-Instruct",
    max_history=60
):
    formatted_news = load_json(formatted_news_path)
    user_sessions = load_json(user_sessions_path)
    user_summaries = {}

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)

    for user_id, sessions in tqdm(user_sessions.items(), desc="Generating summaries"):
        news_ids = [nid for session in sessions for nid in session][-max_history:]
        news_texts = [formatted_news[nid] for nid in news_ids if nid in formatted_news]
        prompt = build_prompt(news_texts)
        output = generator(prompt, do_sample=False)[0]["generated_text"]
        summary = output.split("Summary of user interest:")[-1].strip()
        user_summaries[user_id] = summary

    save_json(user_summaries, output_path)
    print(f"[Saved] LLM summaries → {output_path}")

if __name__ == "__main__":
    formatted_news_path = "output/MINDsmall_train/formatted_news.json"
    user_sessions_path = "output/MINDsmall_train/user_sessions.json"
    output_path = "output/MINDsmall_train/user_summaries_llama.json"
    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    main(formatted_news_path, user_sessions_path, output_path, model_name)


