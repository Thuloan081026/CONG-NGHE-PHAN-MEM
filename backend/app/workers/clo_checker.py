from celery import Celery
from sentence_transformers import SentenceTransformer, util

app = Celery("clo_checker", broker="redis://localhost:6379/0")

model = SentenceTransformer("keepitreal/vietnamese-sbert")

@app.task(name="clo.check")
def clo_check_task(syllabus_id: int, clos, plos):

    result = []

    for clo in clos:
        scores = []
        for plo in plos:
            clo_emb = model.encode(clo, convert_to_tensor=True)
            plo_emb = model.encode(plo, convert_to_tensor=True)
            sim = float(util.cos_sim(clo_emb, plo_emb)[0][0])
            scores.append({"plo": plo, "score": sim})

        result.append({
            "clo": clo,
            "best_match": max(scores, key=lambda x: x["score"])
        })

    return {
        "syllabus_id": syllabus_id,
        "mapping": result
    }
