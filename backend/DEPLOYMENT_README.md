## 🗄️ MySQL Database Setup (XAMPP)

### 1. Cài đặt và cấu hình XAMPP

1. **Download và cài đặt XAMPP**:
   - Download từ: https://www.apachefriends.org/
   - Chạy installer và chọn MySQL

2. **Start MySQL service**:
   - Mở XAMPP Control Panel
   - Click "Start" cho MySQL module
   - Đảm bảo port 3306 không bị conflict

3. **Truy cập phpMyAdmin**:
   - Click "Admin" cho MySQL hoặc mở: http://localhost/phpmyadmin
   - Default credentials: root / (empty password)

### 2. Cấu hình Backend cho MySQL

1. **Cập nhật requirements.txt**:
   ```txt
   pymysql>=1.0.2
   ```

2. **Cập nhật config.py**:
   ```python
   DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/syllabus_db"
   ```

3. **Cập nhật database.py**:
   ```python
   engine = create_engine(
       settings.DATABASE_URL,
       pool_pre_ping=True,
       pool_recycle=300,
       echo=False
   )
   ```

### 3. Tạo Database và Tables

```bash
# Tạo database
python setup_mysql.py

# Start server (tables sẽ được tạo tự động)
uvicorn app.main:app --reload
```

### 4. Migrate từ SQLite (nếu có data cũ)

```bash
# Migrate data từ SQLite sang MySQL
python migrate_to_mysql.py

# Sau khi migrate thành công, có thể xóa file SQLite
rm database.db
```

### 5. Cấu hình Production

**Environment Variables**:
```bash
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/syllabus_db
```

**Docker với MySQL**:
```yaml
services:
  backend:
    environment:
      - DATABASE_URL=mysql+pymysql://root:@db:3306/syllabus_db
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: syllabus_db
      MYSQL_USER: syllabus_user
      MYSQL_PASSWORD: syllabus_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - mysql_data:/var/lib/mysql
```

### 6. Troubleshooting MySQL

**Connection Issues**:
```bash
# Test MySQL connection
python -c "import pymysql; pymysql.connect(host='localhost', user='root', password='', db='syllabus_db')"
```

**Common Errors**:
- `Access denied`: Check username/password
- `Can't connect`: Check if MySQL is running on port 3306
- `Unknown database`: Run `python setup_mysql.py`
- `Table doesn't exist`: Restart server để tạo tables

**Check MySQL Status**:
```bash
# Windows
netstat -ano | findstr :3306

# Linux/Mac
lsof -i :3306
```

### Prerequisites
- Docker installed
- docker-compose installed

### Deploy Steps

1. **Clone/Build the project**
   ```bash
   cd backend
   ```

2. **Run deploy script**
   ```bash
   # On Linux/Mac
   ./deploy.sh

   # Or manually
   docker-compose up --build -d
   ```

3. **Check deployment**
   ```bash
   # Check if running
   docker-compose ps

   # View logs
   docker-compose logs -f backend

   # Test API
   curl http://localhost:8000/docs
   ```

## 📋 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token

### Syllabus Management
- `GET /syllabus/` - List syllabuses
- `POST /syllabus/` - Create syllabus
- `GET /syllabus/{id}` - Get syllabus details
- `PUT /syllabus/{id}` - Update syllabus
- `DELETE /syllabus/{id}` - Delete syllabus

### Workflow Management
- `POST /workflow/submit` - Lecturer submit syllabus
- `POST /workflow/hod-approve` - HOD approve
- `POST /workflow/aa-approve` - AA approve
- `POST /workflow/final-approve` - Principal final approve
- `GET /workflow/{syllabus_id}/events` - View workflow history

## 🔧 Manual Development Setup

### Local Development
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run workflow tests
python test_workflow.py

# Run with different database
DATABASE_URL="sqlite:///./test.db" python test_workflow.py
```

## 🏗️ Architecture

- **Framework**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Documentation**: Auto-generated OpenAPI/Swagger

## 🔒 Security Features

- JWT token authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- CORS enabled
- Input validation with Pydantic

## 📊 Database Schema

- **Users**: Authentication & roles
- **Syllabuses**: Main content
- **SyllabusVersions**: Version control
- **WorkflowEvents**: Audit trail

## 🚦 Health Checks

- Application health: `GET /docs`
- Database connectivity: Automatic on startup
- Container health: Built-in Docker health checks

## 🔄 Production Deployment

For production, consider:
- Use PostgreSQL instead of SQLite
- Set strong SECRET_KEY
- Enable HTTPS/SSL
- Configure proper logging
- Set up monitoring
- Use reverse proxy (nginx)

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill process or change port
   ```

2. **Database connection failed**
   - Check DATABASE_URL in environment
   - Ensure database server is running
   - Check database permissions

3. **Import errors**
   - Ensure all dependencies installed
   - Check Python path
   - Verify virtual environment activated

### Logs
```bash
# View application logs
docker-compose logs -f backend

# View with timestamps
docker-compose logs -f --timestamps backend
```