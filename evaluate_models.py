import os
import json
import csv
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
import torch
from collections import defaultdict

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")  # in case needed later

# Drift detection model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Zero-shot classifier
zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Load reference persona definition
with open('maya_system_prompts.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

with open('maya_persona_defination.md', 'r', encoding='utf-8') as f:
    persona_definition = f.read()

reference_persona = system_prompt + "\n" + persona_definition
reference_embedding = embedding_model.encode(reference_persona, convert_to_tensor=True)

# Load test cases
with open('user_test_cases.json', 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

results = []

def score_with_zero_shot(response):
    labels_persona = ["in character", "out of character"]
    labels_tone = ["friendly", "harsh", "neutral", "playful"]

    persona_res = zero_shot(response, labels_persona)
    tone_res = zero_shot(response, labels_tone)

    persona_score = round(persona_res["scores"][persona_res["labels"].index("in character")] * 10, 2)
    tone_score = round(tone_res["scores"][tone_res["labels"].index("playful")] * 10, 2)

    return persona_score, tone_score

def score_engagement(response):
    # Naive heuristic: longer, richer responses with varied vocabulary are more engaging
    length_score = min(len(response.split()) / 25.0, 1.0) * 10  # cap at 250 words
    keyword_score = sum(1 for w in ["you", "let's", "imagine", "exciting", "fun", "?"] if w in response.lower()) * 2
    engagement_score = min(length_score + keyword_score, 10)
    return round(engagement_score, 2)

for case in test_cases:
    prompt_id = case.get("id")
    category = case.get("category")
    prompt_text = case.get("prompt")
    responses = case.get("responses", {})

    for model_name, response in responses.items():
        response_embedding = embedding_model.encode(response, convert_to_tensor=True)
        similarity_score = util.cos_sim(reference_embedding, response_embedding).item()

        try:
            persona_score, tone_score = score_with_zero_shot(response)
            engagement_score = score_engagement(response)

            results.append({
                "prompt_id": prompt_id,
                "category": category,
                "prompt": prompt_text,
                "model": model_name,
                "persona": persona_score,
                "tone": tone_score,
                "engagement": engagement_score,
                "drift_score": round(similarity_score, 3),
                "timestamp": datetime.utcnow().isoformat()
            })

        except Exception as e:
            print(f"Error scoring response from {model_name} on {prompt_id}: {e}")

# Write Markdown report
with open('results.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, indent=2, ensure_ascii=False)

# Write Markdown report
grouped = defaultdict(lambda: defaultdict(list))
for r in results:
    grouped[r["model"]][r["category"]].append(r)

with open('results.md', 'w', encoding='utf-8') as md:
    md.write(f"# Evaluation Results – {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n")

    for model, categories in grouped.items():
        md.write(f"## Model: `{model}`\n\n")

        for category, entries in categories.items():
            md.write(f"### Category: *{category}*\n\n")

            for r in entries:
                md.write(f"#### Prompt `{r['prompt_id']}`\n")
                md.write(f"> {r['prompt']}\n\n")
                md.write(f"- **Persona Score**: {r['persona']}/10\n")
                md.write(f"- **Tone Score**: {r['tone']}/10\n")
                md.write(f"- **Engagement Score**: {r['engagement']}/10\n")
                md.write(f"- **Drift Score**: {r['drift_score']}\n")
                md.write(f"- *Timestamp*: `{r['timestamp']}`\n\n")

            md.write("---\n\n")
        md.write("\n---\n\n")

print("✅ Reports generated: `results.md` & `results.json`")
