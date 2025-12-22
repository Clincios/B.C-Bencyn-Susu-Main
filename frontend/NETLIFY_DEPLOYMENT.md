# Netlify Production Deployment Guide - B.C BENCYN SUSU Frontend

This guide will help you deploy the B.C BENCYN SUSU frontend to Netlify in production mode.

## 🚀 Quick Setup

### 1. Connect Your Repository to Netlify

1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Click "Add new site" → "Import an existing project"
3. Connect your Git provider (GitHub, GitLab, or Bitbucket)
4. Select your repository

### 2. Configure Build Settings

Netlify will automatically detect the `netlify.toml` file, but you can also set these manually:

- **Base directory:** `frontend`
- **Build command:** `npm run build`
- **Publish directory:** `frontend/build`

### 3. Set Environment Variables

**CRITICAL:** You must set the production API URL in Netlify's environment variables.

1. Go to **Site settings** → **Environment variables**
2. Add the following variable:

```
REACT_APP_API_URL = https://your-backend-api-domain.com
```

**Important Notes:**
- Replace `https://your-backend-api-domain.com` with your actual backend API URL
- Do NOT include a trailing slash
- Use `https://` (not `http://`) for production
- Example: `https://api.bencynsusu.com` or `https://bencynsusu-api.herokuapp.com`

### 4. Deploy

1. Click "Deploy site"
2. Netlify will automatically:
   - Install dependencies (`npm install`)
   - Build your React app (`npm run build`)
   - Deploy to production

## 📋 Pre-Deployment Checklist

- [ ] Backend API is deployed and accessible
- [ ] Backend CORS settings include your Netlify domain
- [ ] `REACT_APP_API_URL` environment variable is set in Netlify
- [ ] Backend API URL uses HTTPS
- [ ] Test the production build locally: `npm run build && npx serve -s build`

## 🔧 Configuration Files

### `netlify.toml`

This file contains:
- Build configuration
- Security headers
- Cache settings for static assets
- SPA routing redirects

### `public/_redirects`

This file ensures React Router works correctly by redirecting all routes to `index.html`.

## 🌐 Custom Domain Setup

1. Go to **Site settings** → **Domain management**
2. Add your custom domain
3. Follow Netlify's DNS configuration instructions
4. Update your backend `CORS_ALLOWED_ORIGINS` to include your custom domain

## 🔒 Security Headers

The `netlify.toml` file includes security headers:
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

## ⚡ Performance Optimization

- Static assets are cached for 1 year
- Build output is optimized by React Scripts
- Lazy loading is configured for routes

## 🔄 Continuous Deployment

Netlify automatically deploys when you push to your main branch. You can:
- Set up branch previews for pull requests
- Configure deploy contexts (production, staging, etc.)
- Set up deploy notifications

## 🐛 Troubleshooting

### Build Fails

1. Check build logs in Netlify dashboard
2. Ensure Node.js version is compatible (18.x recommended)
3. Verify all dependencies are in `package.json`

### API Calls Fail

1. Verify `REACT_APP_API_URL` is set correctly
2. Check backend CORS settings include your Netlify domain
3. Ensure backend API is accessible and uses HTTPS
4. Check browser console for CORS errors

### Routes Not Working (404 errors)

1. Verify `_redirects` file is in `public/` folder
2. Check `netlify.toml` redirects configuration
3. Ensure React Router is using `BrowserRouter`

### Environment Variables Not Working

1. Environment variables must start with `REACT_APP_` to be accessible in React
2. Redeploy after adding/changing environment variables
3. Check variable names match exactly (case-sensitive)

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API base URL (required) | `https://api.bencynsusu.com` |

## 🔗 Related Documentation

- [Netlify Documentation](https://docs.netlify.com/)
- [React Deployment](https://create-react-app.dev/docs/deployment/)
- [Netlify Environment Variables](https://docs.netlify.com/environment-variables/overview/)

---

**Last Updated:** 2024-12-21
**Version:** 1.0

