# Production Deployment Checklist - B.C BENCYN SUSU

This guide will help you deploy the B.C BENCYN SUSU backend to production.

## 🔴 CRITICAL: Before Deployment

### 1. Environment Variables (.env file)

Create a `.env` file in the `backend/` directory (copy from `env_template.txt`) and configure:

```bash
# REQUIRED - Generate a new secret key
SECRET_KEY=your-generated-secret-key-here

# REQUIRED - Set to False
DEBUG=False

# REQUIRED - Add your production domain(s)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# REQUIRED - Add your frontend domain(s) with https://
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Generate Secret Key

Run this command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and set it as `SECRET_KEY` in your `.env` file.

### 3. Database Configuration

**Option A: Using DATABASE_URL (Recommended for Heroku, Railway, etc.)**

```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

**Option B: Using Individual Settings**

```bash
DB_NAME=bencyn_susu
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

**Note:** SQLite is used as fallback if no database configuration is provided, but PostgreSQL is **strongly recommended** for production.

### 4. Install Production Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- Django and DRF
- PostgreSQL adapter (psycopg2-binary)
- dj-database-url (for DATABASE_URL support)
- Gunicorn (WSGI server)
- WhiteNoise (static file serving)
- Other dependencies

## 📋 Pre-Deployment Steps

### 1. Run Migrations

```bash
python manage.py migrate
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Create Superuser (if needed)

```bash
python manage.py createsuperuser
```

### 4. Test Production Settings

```bash
# Set DEBUG=False in .env, then:
python manage.py check --deploy
```

This will check for common production issues.

## 🚀 Deployment Options

### Option 1: Using Gunicorn (Recommended)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with Gunicorn
gunicorn bencyn_susu.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Option 2: Using uWSGI

```bash
pip install uwsgi
uwsgi --http :8000 --module bencyn_susu.wsgi --processes 4 --threads 2
```

### Option 3: Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "bencyn_susu.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🔒 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is set and secure (not the default)
- [ ] `ALLOWED_HOSTS` includes your domain(s)
- [ ] `CORS_ALLOWED_ORIGINS` includes your frontend domain(s)
- [ ] Database uses PostgreSQL (not SQLite)
- [ ] HTTPS is enabled (SECURE_SSL_REDIRECT=True)
- [ ] Static files are served via WhiteNoise or CDN
- [ ] Media files are served securely (consider using S3/Cloud Storage)
- [ ] Email backend is configured for production
- [ ] Logging is configured (file-based or logging service)

## 📧 Email Configuration

For production email, configure SMTP settings in `.env`:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## 📊 Monitoring & Logging

### File-Based Logging

The settings include file-based logging configuration. Uncomment the file handler in `settings.py`:

```python
'file': {
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'logs' / 'django.log',
    'maxBytes': 1024 * 1024 * 10,  # 10 MB
    'backupCount': 5,
    'formatter': 'verbose',
},
```

### Logging Services

Consider using services like:
- Sentry (error tracking)
- Loggly
- Papertrail
- AWS CloudWatch

## 🌐 Reverse Proxy Setup (Nginx Example)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/your/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/your/media/;
    }
}
```

## ✅ Post-Deployment Verification

1. **Check Health Endpoint** (if configured)
   ```bash
   curl https://api.yourdomain.com/api/
   ```

2. **Verify Static Files**
   - Check that CSS/JS files load correctly
   - Verify admin panel static files work

3. **Test API Endpoints**
   - Test public endpoints
   - Verify CORS headers
   - Check rate limiting

4. **Security Headers**
   - Verify HTTPS redirect works
   - Check security headers are present
   - Test CSRF protection

## 🔄 Maintenance

### Regular Tasks

1. **Backup Database**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Clear Cache** (if using)
   ```bash
   python manage.py clear_cache
   ```

## 📝 Environment-Specific Notes

### Heroku
- Set environment variables in Heroku dashboard
- Use `DATABASE_URL` (automatically provided)
- Use `gunicorn` as process type
- Static files handled by WhiteNoise

### Railway
- Set environment variables in Railway dashboard
- Use `DATABASE_URL` for PostgreSQL
- Configure start command: `gunicorn bencyn_susu.wsgi:application`

### DigitalOcean / VPS
- Install PostgreSQL: `sudo apt-get install postgresql`
- Set up Nginx as reverse proxy
- Use systemd for process management
- Set up SSL with Let's Encrypt

## 🆘 Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check `DEBUG=False` and review logs
   - Verify `ALLOWED_HOSTS` includes your domain
   - Check database connection

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Verify `STATIC_ROOT` is set correctly
   - Check WhiteNoise configuration

3. **CORS Errors**
   - Verify `CORS_ALLOWED_ORIGINS` includes frontend domain
   - Check that frontend uses `https://` in production

4. **Database Connection Errors**
   - Verify database credentials
   - Check database server is running
   - Verify network/firewall settings

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [WhiteNoise Documentation](https://whitenoise.evans.io/)

---

**Last Updated:** 2024-12-21
**Version:** 1.0

