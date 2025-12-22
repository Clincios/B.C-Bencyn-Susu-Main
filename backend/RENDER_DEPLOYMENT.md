# Render Deployment Guide - B.C BENCYN SUSU Backend

This guide will help you deploy the B.C BENCYN SUSU backend to Render.

## 🚀 Quick Setup

### 1. Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name:** `bencyn-susu-api` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn bencyn_susu.wsgi:application --bind 0.0.0.0:$PORT`
   - **Root Directory:** `backend`

### 2. Python Version Configuration

**IMPORTANT:** The `.python-version` file in the `backend/` directory (and root) specifies Python 3.12.7. This ensures compatibility with all packages.

**Render uses `.python-version` file (not `runtime.txt` which is for Heroku).**

If you need to change the Python version, edit `.python-version`:
```
3.12.7
```

Supported versions:
- `3.12.7` (recommended)
- `3.11.9`
- `3.10.13`

**Note:** Python 3.13 may cause build errors with some packages. Stick with 3.12 or 3.11.

**Alternative:** You can also set `PYTHON_VERSION` environment variable in Render dashboard to `3.12.7`.

### 3. Environment Variables

Set these in Render Dashboard → Environment:

#### Required Variables

```bash
# Django Settings
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
# IMPORTANT: Replace with your actual Render service domain
ALLOWED_HOSTS=b-c-bencyn-susu-main.onrender.com,yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-frontend.netlify.app
```

**Note:** The code now auto-detects Render domains from `RENDER_SERVICE_URL`, but it's recommended to set `ALLOWED_HOSTS` explicitly to avoid issues.

# Database (Render provides this automatically for PostgreSQL)
# DATABASE_URL is auto-set if you add a PostgreSQL database
# OR set manually:
DB_NAME=bencyn_susu
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
```

#### Optional Variables

```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Security (optional, defaults are set in settings.py)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### 4. Database Setup

1. In Render Dashboard, go to your service
2. Click "Add" → "PostgreSQL"
3. Create a new PostgreSQL database
4. Render will automatically set the `DATABASE_URL` environment variable
5. The Django settings will automatically use this `DATABASE_URL`

### 5. Build and Deploy

Render will automatically:
1. Detect `runtime.txt` and use Python 3.12.7
2. Install dependencies from `requirements.txt`
3. Run migrations (if configured)
4. Start the service with Gunicorn

## 📋 Pre-Deployment Checklist

- [ ] `runtime.txt` exists in `backend/` directory
- [ ] `requirements.txt` includes `setuptools` and `wheel`
- [ ] Environment variables are set in Render dashboard
- [ ] PostgreSQL database is created and connected
- [ ] `SECRET_KEY` is generated and set (not the default)
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] `CORS_ALLOWED_ORIGINS` includes your frontend domain(s)
- [ ] Backend API URL is set in frontend environment variables

## 🔧 Build Configuration

### Build Command

**Option 1: Using build script (Recommended)**
```bash
chmod +x backend/build.sh && backend/build.sh
```

**Option 2: Manual build command**
```bash
pip install --upgrade pip setuptools wheel && pip install -r backend/requirements.txt && cd backend && python manage.py collectstatic --noinput
```

The build script (`backend/build.sh`) automatically:
- Upgrades pip, setuptools, and wheel
- Installs all requirements
- Collects static files

### Start Command
```bash
gunicorn bencyn_susu.wsgi:application --bind 0.0.0.0:$PORT
```

**Note:** Render automatically sets the `$PORT` environment variable. Do not hardcode a port number.

### Root Directory
Set to: `backend`

## 🔄 Running Migrations

### Option 1: Manual Migration (Recommended for first deploy)

1. After first deployment, open Render Shell:
   - Go to your service → "Shell"
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

### Option 2: Automatic Migration (Add to build command)

Modify build command to:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput
```

**Note:** This runs migrations on every deploy. Use with caution.

## 🐛 Troubleshooting

### Build Fails with "KeyError: '__version__'"

**Solution:** 
1. Ensure `.python-version` file exists in `backend/` directory with:
   ```
   3.12.7
   ```
2. Or set `PYTHON_VERSION` environment variable in Render dashboard to `3.12.7`
3. Use the build script (`backend/build.sh`) which upgrades pip/setuptools first

This error occurs when using Python 3.13, which some packages don't support yet. The `.python-version` file tells Render to use Python 3.12.7 instead.

### Build Fails with "subprocess-exited-with-error"

**Solution:** 
1. Check that `setuptools` and `wheel` are in `requirements.txt`
2. Verify Python version in `runtime.txt` is 3.12 or 3.11
3. Check build logs for specific package errors

### Database Connection Errors

**Solution:**
1. Verify PostgreSQL database is created and running
2. Check `DATABASE_URL` is set automatically (if using Render PostgreSQL)
3. Or verify individual DB_* variables are set correctly
4. Ensure database is in the same region as your service

### Static Files Not Loading

**Solution:**
1. Add to build command: `python manage.py collectstatic --noinput`
2. Or modify build command:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
3. WhiteNoise is configured to serve static files automatically

### CORS Errors

**Solution:**
1. Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
2. Use `https://` (not `http://`) for production
3. Include both `www` and non-`www` versions if applicable
4. Check backend logs for CORS-related errors

### Service Won't Start

**Solution:**
1. Verify start command uses `$PORT` (not hardcoded port)
2. Check environment variables are set correctly
3. Review service logs for specific errors
4. Ensure `ALLOWED_HOSTS` includes your Render domain

## 📊 Monitoring

### View Logs
- Go to your service → "Logs" tab
- Real-time logs are available
- Download logs for analysis

### Health Checks
Render automatically monitors your service. You can add a health check endpoint:

```python
# In your views.py or urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Use Render environment variables
2. **Use strong SECRET_KEY** - Generate with:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. **Enable HTTPS** - Render provides SSL automatically
4. **Set DEBUG=False** - Always in production
5. **Restrict ALLOWED_HOSTS** - Only include your domains
6. **Configure CORS properly** - Only allow your frontend domains

## 📝 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | Yes | Django secret key | Generated string |
| `DEBUG` | Yes | Debug mode | `False` |
| `ALLOWED_HOSTS` | Yes | Allowed hostnames | `your-app.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | Yes | Frontend origins | `https://your-site.netlify.app` |
| `DATABASE_URL` | Auto | PostgreSQL connection | Auto-set by Render |
| `EMAIL_HOST` | No | SMTP server | `smtp.gmail.com` |
| `EMAIL_HOST_USER` | No | Email username | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | No | Email password | App password |

## 🔗 Related Documentation

- [Render Python Documentation](https://render.com/docs/deploy-python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://gunicorn.org/)

---

**Last Updated:** 2024-12-21
**Version:** 1.0

