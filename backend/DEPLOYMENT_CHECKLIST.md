# 🚀 DEPLOYMENT CHECKLIST - Authentication & User Management Module

## 📋 Pre-Deployment Verification

### Environment Setup ✅
- [x] Python 3.8+ installed
- [x] Requirements installed: `pip install -r requirements.txt`
- [x] Virtual environment (recommended): `python -m venv venv`
- [ ] Environment variables configured (.env file)

### Code Quality ✅
- [x] All 13 endpoints implemented
- [x] RBAC fully functional
- [x] Error handling in place
- [x] Type hints added (optional)
- [x] Code follows PEP 8 standards

### Documentation ✅
- [x] README.md - Project overview
- [x] QUICK_START.md - Quick reference
- [x] AUTHENTICATION_USER_MANAGEMENT.md - Full docs
- [x] API_REFERENCE.md - Endpoint details
- [x] IMPLEMENTATION_SUMMARY.md - Summary

### Testing ✅
- [x] Swagger/OpenAPI docs working
- [x] PowerShell test script created
- [x] Bash test script created
- [x] Sample CSV data provided
- [x] All endpoints tested manually

---

## 🔧 Development Deployment (Local)

### Step 1: Prepare Environment
```powershell
cd d:\project cnpm\backend

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Development Server
```powershell
uvicorn app.main:app --reload --port 8000
```

### Step 3: Verify Server
- Open http://localhost:8000/docs in browser
- Should see Swagger UI with all endpoints

### Step 4: Test Endpoints
```powershell
powershell -ExecutionPolicy Bypass -File test_auth_api.ps1
```

### Step 5: Verify Results
- All 13 tests should pass
- JSON responses should be valid
- Tokens should be generated correctly

---

## 🔐 Security Hardening (Production)

### Critical: Secret Key
```powershell
# Generate secure random key
$key = -join ((1..32) | ForEach-Object { '{0:X}' -f (Get-Random -Minimum 0 -Maximum 16) })
Write-Host "SECRET_KEY=$key"
```

**Create .env file:**
```env
SECRET_KEY=<your-generated-key-here>
DATABASE_URL=mysql://user:password@localhost/smd_db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Update app/core/config.py:**
```python
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    # ... rest of config
    
    class Config:
        env_file = ".env"
```

### Database Security
```powershell
# Option 1: MySQL
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/smd_db

# Option 2: PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost:5432/smd_db
```

**Install MySQL driver:**
```powershell
pip install pymysql
```

**Install PostgreSQL driver:**
```powershell
pip install psycopg2-binary
```

### HTTPS/TLS Configuration
```powershell
# Use Nginx as reverse proxy
# SSL certificate from Let's Encrypt
# Enforce HTTPS in app
```

### Rate Limiting
```powershell
# Install slowapi
pip install slowapi
```

**Update app/main.py:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/auth/login")
@limiter.limit("5/minute")
def login(...):
    ...
```

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.smd.edu.vn", "https://student.smd.edu.vn"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📦 Deployment Steps (Server)

### Option 1: Traditional Linux/Windows Server

#### 1.1 Install Dependencies
```bash
sudo apt-get update
sudo apt-get install python3.10 python3-pip python3-venv mysql-server nginx
```

#### 1.2 Clone Repository
```bash
cd /var/www
git clone <repository-url> smd-backend
cd smd-backend
```

#### 1.3 Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 1.4 Setup Database
```bash
mysql -u root -p
CREATE DATABASE smd_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'smd_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON smd_db.* TO 'smd_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 1.5 Create .env File
```bash
sudo nano /var/www/smd-backend/.env
```

```env
SECRET_KEY=<generated-key>
DATABASE_URL=mysql+pymysql://smd_user:secure_password@localhost/smd_db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### 1.6 Run Migrations (if using Alembic)
```bash
alembic upgrade head
```

#### 1.7 Setup Systemd Service
**Create /etc/systemd/system/smd-backend.service:**
```ini
[Unit]
Description=SMD Backend API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/smd-backend
Environment="PATH=/var/www/smd-backend/venv/bin"
ExecStart=/var/www/smd-backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start smd-backend
sudo systemctl enable smd-backend
sudo systemctl status smd-backend
```

#### 1.8 Setup Nginx Reverse Proxy
**Create /etc/nginx/sites-available/smd-backend:**
```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.smd.edu.vn;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/smd-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 1.9 Setup SSL Certificate
```bash
sudo certbot certonly --nginx -d api.smd.edu.vn
sudo certbot renew --dry-run  # Test auto-renewal
```

---

### Option 2: Docker Deployment

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_pass
      MYSQL_DATABASE: smd_db
      MYSQL_USER: smd_user
      MYSQL_PASSWORD: smd_pass
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://smd_user:smd_pass@db:3306/smd_db
      SECRET_KEY: your-secret-key
    depends_on:
      - db
    volumes:
      - .:/app

volumes:
  db_data:
```

**Deploy:**
```bash
docker-compose up -d
docker-compose logs -f backend
```

---

### Option 3: Cloud Deployment (AWS)

#### AWS EC2 Deployment
1. Launch EC2 instance (Ubuntu 22.04)
2. Assign Elastic IP
3. Configure security groups (port 80, 443, 22)
4. Follow "Traditional Server" steps above
5. Setup Route53 DNS

#### AWS RDS Database
1. Create RDS MySQL instance
2. Configure security groups
3. Update DATABASE_URL in .env
4. Run migrations

---

## ✅ Post-Deployment Verification

### 1. Health Check
```bash
curl http://localhost:8000/docs
# Should return Swagger UI
```

### 2. Database Connection
```bash
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer <admin_token>"
# Should return list of users
```

### 3. Create Test User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","role":"student"}'
# Should return 201 with user data
```

### 4. Login Test
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
# Should return access and refresh tokens
```

### 5. Check Logs
```bash
# Linux/Mac
tail -f /var/log/syslog | grep smd-backend

# Windows
Get-Content C:\Logs\smd-backend.log -Tail 20 -Wait
```

---

## 📊 Monitoring & Maintenance

### Monitoring Setup
```bash
# Install Prometheus exporter
pip install prometheus-fastapi-instrumentator

# Add to app/main.py
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

### Logging Setup
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/smd-backend.log'),
        logging.StreamHandler()
    ]
)
```

### Daily Backup
```bash
# Create backup script: backup.sh
#!/bin/bash
BACKUP_DIR="/backups/smd-db"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mysqldump -u smd_user -p smd_db > $BACKUP_DIR/smd_db_$TIMESTAMP.sql
tar -czf $BACKUP_DIR/smd_db_$TIMESTAMP.tar.gz $BACKUP_DIR/smd_db_$TIMESTAMP.sql

# Schedule with crontab
0 2 * * * /path/to/backup.sh  # 2 AM daily
```

---

## 🔄 Update & Maintenance

### Update Dependencies
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
systemctl restart smd-backend
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Zero-Downtime Deployment
```bash
# Using systemd with socket activation or Kubernetes
# Rolling restart strategy
```

---

## 🎯 Go-Live Checklist

### 24 Hours Before
- [ ] Final code review
- [ ] Security audit completed
- [ ] Load testing performed
- [ ] Backup system verified
- [ ] Rollback plan documented

### 1 Hour Before
- [ ] All systems checked
- [ ] Database backed up
- [ ] Team on standby
- [ ] Communication channels open

### Deployment
- [ ] Deploy code
- [ ] Verify all endpoints
- [ ] Check logs for errors
- [ ] Monitor response times
- [ ] Test critical flows

### Post-Deployment
- [ ] Monitor metrics
- [ ] Check user feedback
- [ ] Review error logs
- [ ] Verify backups
- [ ] Document any issues

---

## 🚨 Troubleshooting Production Issues

### Issue: Server won't start
```bash
# Check logs
systemctl status smd-backend
journalctl -u smd-backend -n 50

# Verify ports
sudo netstat -tlnp | grep 8000

# Check database connection
python -c "from app.core.database import engine; engine.connect()"
```

### Issue: 500 errors
```bash
# Enable debug logging
# Check /var/log/smd-backend.log for stack traces
# Review recent code changes
# Check database connection pool
```

### Issue: Slow response times
```bash
# Enable slow query logging
# Review database indexes
# Monitor CPU/memory usage
# Check network latency
```

---

## 📞 Escalation Path

1. **Level 1:** Check logs, restart service
2. **Level 2:** Rollback to previous version
3. **Level 3:** Contact development team
4. **Level 4:** Incident response team

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [SQLAlchemy Production](https://docs.sqlalchemy.org/)
- [Nginx Config](https://nginx.org/en/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Security Best Practices](https://owasp.org/www-project-top-ten/)

---

**Deployment Status:** ✅ READY  
**Last Updated:** 2025-12-06  
**Version:** 1.0.0

