============================================================
PYTHON PROJECT DIRECTORY STRUCTURE (NO +--)
Syllabus Management and Digitalization System (SMD)
Project Code: SP26SE001
============================================================


1. CORE BACKEND SERVICE (PYTHON – FASTAPI)
------------------------------------------------------------

backend\
|
|__ app\
|   |
|   |__ api\                             // API Layer
|   |   |
|   |   |__ v1\
|   |       |
|   |       |__ auth.py                 // Authentication APIs
|   |       |__ users.py                // User management
|   |       |__ syllabus.py             // Syllabus CRUD
|   |       |__ workflow.py             // Review & approval flow
|   |       |__ notification.py         // Notifications
|   |
|   |__ models\                          // ORM Models
|   |   |
|   |   |__ base.py
|   |   |__ user.py
|   |   |__ role.py
|   |   |__ syllabus.py
|   |   |__ clo.py
|   |   |__ plo.py
|   |   |__ workflow.py
|   |   |__ audit_log.py
|   |
|   |__ schemas\                         // Pydantic Schemas
|   |   |
|   |   |__ user_schema.py
|   |   |__ syllabus_schema.py
|   |   |__ clo_schema.py
|   |   |__ plo_schema.py
|   |   |__ workflow_schema.py
|   |
|   |__ repositories\                   // Data Access Layer
|   |   |
|   |   |__ user_repository.py
|   |   |__ syllabus_repository.py
|   |   |__ clo_repository.py
|   |   |__ plo_repository.py
|   |   |__ workflow_repository.py
|   |
|   |__ services\                        // Business Logic
|   |   |
|   |   |__ auth_service.py
|   |   |__ user_service.py
|   |   |__ syllabus_service.py
|   |   |__ workflow_service.py
|   |   |__ notification_service.py
|   |
|   |__ middlewares\                     // Cross-cutting concerns
|   |   |
|   |   |__ auth_middleware.py
|   |   |__ logging_middleware.py
|   |   |__ error_handler.py
|   |
|   |__ utils\
|   |   |
|   |   |__ security.py
|   |   |__ constants.py
|   |   |__ helpers.py
|   |
|   |__ core\
|   |   |
|   |   |__ config.py
|   |   |__ database.py
|   |   |__ redis.py
|   |
|   |__ tasks\
|       |
|       |__ notification_tasks.py
|
|__ migrations\                          // Database migrations
|
|__ tests\
|   |
|   |__ unit\
|   |__ integration\
|
|__ main.py                              // Backend entry point
|__ requirements.txt
|__ .env.example


------------------------------------------------------------
2. AI & NLP MICROSERVICE (PYTHON – FASTAPI + CELERY)
------------------------------------------------------------

ai-service\
|
|__ app\
|   |
|   |__ api\                             // AI APIs
|   |   |
|   |   |__ compare.py                  // Semantic diff
|   |   |__ clo_plo_check.py            // CLO–PLO validation
|   |   |__ summarization.py            // AI summary
|   |
|   |__ workers\                        // Celery workers
|   |   |
|   |   |__ diff_worker.py
|   |   |__ summary_worker.py
|   |   |__ clo_plo_worker.py
|   |
|   |__ nlp\                            // NLP core
|   |   |
|   |   |__ embeddings.py
|   |   |__ semantic_similarity.py
|   |   |__ keyword_extraction.py
|   |
|   |__ llm\                            // GenAI integration
|   |   |
|   |   |__ llama_client.py
|   |   |__ openai_client.py
|   |
|   |__ ocr\                            // OCR processing
|   |   |
|   |   |__ pdf_parser.py
|   |   |__ image_ocr.py
|   |
|   |__ crawlers\                       // Crawlers
|   |   |
|   |   |__ syllabus_crawler.py
|   |
|   |__ vector_store\                  // Vector database
|   |   |
|   |   |__ pgvector_client.py
|   |
|   |__ core\
|   |   |
|   |   |__ config.py
|   |   |__ celery_app.py
|   |   |__ redis.py
|   |
|   |__ utils\
|       |
|       |__ text_cleaner.py
|
|__ tests\
|   |
|   |__ ai_unit_tests\
|
|__ main.py                              // AI service entry point
|__ requirements.txt
|__ .env.example


============================================================
END OF DIRECTORY STRUCTURE
============================================================
