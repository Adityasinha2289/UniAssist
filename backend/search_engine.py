import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===============================
# CONFIG
# ===============================
DATA_PATH = "../processed/bennett/chunks.json"
SIMILARITY_THRESHOLD = 0.12   # tuned for legal / policy text
TOP_K = 3

# ===============================
# LOAD DATA
# ===============================
with open(DATA_PATH, "r", encoding="utf-8") as f:
    CHUNKS = json.load(f)

DOCUMENTS = [c["text"] for c in CHUNKS]

# ===============================
# TF-IDF MODEL
# ===============================
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2
)
X = vectorizer.fit_transform(DOCUMENTS)

# ===============================
# DOMAIN INFERENCE
# ===============================
def infer_domain(query: str):
    q = query.lower()

    if any(k in q for k in ["hostel", "room", "alcohol", "smoking", "mess"]):
        return "hostel"

    if any(k in q for k in ["exam", "end term", "ufm", "paper", "hall ticket"]):
        return "examination"

    if any(k in q for k in ["supplementary", "backlog", "reappear"]):
        return "examination"

    if any(k in q for k in ["attendance", "75", "detained", "detention"]):
        return "academics"

    if any(k in q for k in ["grievance", "complaint", "appeal"]):
        return "grievance"

    if any(k in q for k in ["ragging"]):
        return "anti_ragging"

    if any(k in q for k in ["discipline", "punishment", "suspend", "rusticate"]):
        return "discipline"

    return None

# ===============================
# SEARCH FUNCTION
# ===============================
def search(query: str, top_k: int = TOP_K):
    domain_hint = infer_domain(query)

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, X)[0]

    results = []

    for idx, score in enumerate(similarities):
        if score < SIMILARITY_THRESHOLD:
            continue

        chunk = CHUNKS[idx]

        # domain filtering if inferred
        if domain_hint and chunk["domain"] != domain_hint:
            continue

        results.append({
            "score": round(float(score), 3),
            "text": chunk["text"],
            "domain": chunk["domain"],
            "source": chunk["source"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

# ===============================
# CLI TEST MODE
# ===============================
if __name__ == "__main__":
    print("\n🧠 UniAssist Search Engine (type 'exit' to quit)")
    while True:
        query = input("\nAsk UniAssist: ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        answers = search(query)

        if not answers:
            print("\n❌ No official rule found based on university documents.")
            continue

        for idx, ans in enumerate(answers, 1):
            print(f"\n🔹 Result {idx}")
            print(f"📁 Source : {ans['source']}")
            print(f"🏷 Domain : {ans['domain']}")
            print(f"⭐ Score  : {ans['score']}")
            print("📄 Rule:")
            print(ans["text"][:900])
            print("-" * 60)
