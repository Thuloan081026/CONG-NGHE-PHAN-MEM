============================================================
PYTHON PROJECT DIRECTORY STRUCTURE (NO +--)
Syllabus Management and Digitalization System (SMD)
Project Code: SP26SE001
============================================================

1. CORE BACKEND SERVICE (PYTHON – FASTAPI)
------------------------------------------------------------

backend
|__ app
|   |__ api                       // API Layer
|   |   |__ v1
|   |       |__ auth.py            // Authentication APIs
|   |       |__ users.py           // User management APIs
|   |       |__ syllabus.py        // Syllabus CRUD APIs
|   |       |__ workflow.py        // Review & approval workflow
|   |       |__ notification.py    // Notification APIs
|   |
|   |__ models                    // ORM Models
|   |   |__ base.py
|   |   |__ user.py
|   |   |__ role.py
|   |   |__ syllabus.py
|   |   |__ clo.py
|   |   |__ plo.py
|   |   |__ workflow.py
|   |   |__ audit_log.py
|   |
|   |__ schemas                   // Pydantic Schemas
|   |   |__ user_schema.py
|   |   |__ syllabus_schema.py
|   |   |__ clo_schema.py
|   |   |__ plo_schema.py
|   |   |__ workflow_schema.py
|   |
|   |__ repositories              // Data Access Layer
|   |   |__ user_repository.py
|   |   |__ syllabus_repository.py
|   |   |__ clo_repository.py
|   |   |__ plo_repository.py
|   |   |__ workflow_repository.py
|   |
|   |__ services                  // Business Logic Layer
|   |   |__ auth_service.py
|   |   |__ user_service.py
|   |   |__ syllabus_service.py
|   |   |__ workflow_service.py
|   |   |__ notification_service.py
|   |
|   |__ middlewares               // Cross-cutting Concerns
|   |   |__ auth_middleware.py
|   |   |__ logging_middleware.py
|   |   |__ error_handler.py
|   |
|   |__ utils
|   |   |__ security.py
|   |   |__ constants.py
|   |   |__ helpers.py
|   |
|   |__ core
|   |   |__ config.py
|   |   |__ database.py
|   |   |__ redis.py
|   |
|   |__ tasks
|       |__ notification_tasks.py
|
|__ migrations                   // Database migrations
|
|__ tests
|   |__ unit
|   |__ integration
|
|__ main.py                       // Application entry point
|__ requirements.txt
|__ .env.example
