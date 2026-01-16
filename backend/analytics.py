import json
import os
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYTICS_FILE = os.path.join(BASE_DIR, "analytics.json")


def load_analytics():
    if not os.path.exists(ANALYTICS_FILE):
        return Counter()
    with open(ANALYTICS_FILE, "r") as f:
        return Counter(json.load(f))


def save_analytics(counter):
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(counter, f, indent=2)


def log_question(question):
    counter = load_analytics()
    normalized = question.lower().strip()
    counter[normalized] += 1
    save_analytics(counter)


def get_top_questions(limit=10):
    counter = load_analytics()
    return counter.most_common(limit)
