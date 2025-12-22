# Quick Fix for Render Build Error

## The Problem
Render is using Python 3.13, which causes `KeyError: '__version__'` errors during package installation.

## The Solution

### Step 1: Python Version File
Create or verify `.python-version` file exists in `backend/` directory:
```
3.12.7
```

### Step 2: Update Build Command in Render Dashboard

Go to your Render service → Settings → Build & Deploy

**Set Build Command to:**
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**OR use the build script:**
```bash
chmod +x backend/build.sh && backend/build.sh
```

### Step 3: Set Python Version Environment Variable (Alternative)

In Render Dashboard → Environment:
- Add variable: `PYTHON_VERSION` = `3.12.7`

### Step 4: Redeploy

Click "Manual Deploy" → "Deploy latest commit"

## Files Created/Fixed

✅ `.python-version` - Tells Render to use Python 3.12.7
✅ `backend/build.sh` - Build script that upgrades tools first
✅ `requirements.txt` - Updated with compatible package versions
✅ `render.yaml` - Optional: Complete Render configuration

## Verification

After deployment, check logs to confirm:
- Python version shows 3.12.7 (not 3.13)
- All packages install successfully
- No `KeyError: '__version__'` errors

