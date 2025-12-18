from celery import Celery
import ollama   # HOẶC openai nếu bạn dùng API
# import openai

app = Celery("summary", broker="redis://localhost:6379/0")

@app.task(name="summary.generate")
def summarize_content_task(syllabus_id: int, content: str):

    # Gọi model AI – ví dụ dùng Llama 3 qua Ollama
    prompt = f"Tóm tắt nội dung sau thành 5–7 câu, ngắn gọn:\n\n{content}"

    response = ollama.generate(model="llama3", prompt=prompt)
    result = response["response"]

    # TODO: Save summary vào DB
    print(f"[SUMMARY DONE] Syllabus {syllabus_id}")

    return {
        "syllabus_id": syllabus_id,
        "summary": result
    }
