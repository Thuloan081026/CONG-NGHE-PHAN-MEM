from workers.summary_task import summarize_content_task
from workers.diff_task import semantic_diff_task
from workers.clo_checker import clo_check_task

class AIService:

    @staticmethod
    def create_summary(content: str, syllabus_id: int):
        task = summarize_content_task.delay(syllabus_id, content)
        return task.id

    @staticmethod
    def create_diff(old: str, new: str, syllabus_id: int):
        task = semantic_diff_task.delay(syllabus_id, old, new)
        return task.id

    @staticmethod
    def check_clo(clos, plos, syllabus_id: int):
        task = clo_check_task.delay(syllabus_id, clos, plos)
        return task.id
