# Fix for ALLOWED_HOSTS Error on Render

## The Error
```
Invalid HTTP_HOST header: 'b-c-bencyn-susu-main.onrender.com'. 
You may need to add 'b-c-bencyn-susu-main.onrender.com' to ALLOWED_HOSTS.
```

## Quick Fix (Choose One)

### Option 1: Set Environment Variable in Render Dashboard (Recommended)

1. Go to **Render Dashboard** → Your Service → **Environment**
2. Add or update the environment variable:
   - **Key:** `ALLOWED_HOSTS`
   - **Value:** `b-c-bencyn-susu-main.onrender.com`
3. **Save** and **Redeploy**

### Option 2: Auto-Detection (Already Implemented)

The code now automatically detects Render deployments and adds the domain from `RENDER_SERVICE_URL`.

**However**, if `RENDER_SERVICE_URL` is not set by Render, you need to use Option 1.

### Option 3: Multiple Domains

If you have multiple domains (custom domain + Render domain):

Set `ALLOWED_HOSTS` to:
```
b-c-bencyn-susu-main.onrender.com,yourdomain.com,www.yourdomain.com
```

## Verification

After setting the environment variable and redeploying:

1. Check the logs - no more `Invalid HTTP_HOST header` errors
2. Visit your service URL - should work without 400 errors
3. API endpoints should respond correctly

## Why This Happens

Django's security feature requires explicitly listing allowed hostnames to prevent HTTP Host header attacks. In production (`DEBUG=False`), Django is strict about this.

## Current Auto-Detection

The updated `settings.py` now:
- Detects if running on Render (`RENDER=true`)
- Reads `RENDER_SERVICE_URL` environment variable
- Automatically adds the domain to `ALLOWED_HOSTS`

**But** if `RENDER_SERVICE_URL` is not available, you must set `ALLOWED_HOSTS` manually.

## Your Specific Domain

Your Render service domain is: **b-c-bencyn-susu-main.onrender.com**

Set this in the `ALLOWED_HOSTS` environment variable in Render.

