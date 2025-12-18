from celery import Celery
from sentence_transformers import SentenceTransformer, util

app = Celery("diff", broker="redis://localhost:6379/0")

model = SentenceTransformer("keepitreal/vietnamese-sbert")

@app.task(name="diff.semantic")
def semantic_diff_task(syllabus_id: int, old: str, new: str):

    old_emb = model.encode(old, convert_to_tensor=True)
    new_emb = model.encode(new, convert_to_tensor=True)

    similarity = float(util.cos_sim(old_emb, new_emb)[0][0])
    changed = 1 - similarity

    return {
        "syllabus_id": syllabus_id,
        "similarity": similarity,
        "changed_rate": changed,
        "status": "major_change" if changed > 0.35 else "minor_change"
    }
