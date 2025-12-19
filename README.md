# B.C BENCYN SUSU - Financial Institution Website

A modern, responsive website for B.C BENCYN SUSU, a financial institution specializing in susu collection services.

## Tech Stack

- **Frontend**: React 18 with React Router, Framer Motion for animations
- **Backend**: Django 4.2 with Django REST Framework
- **Styling**: Custom CSS with CSS Variables for theming

## Features

- 🎨 Modern, responsive UI design
- 🎨 Color scheme adapted from company logo (Orange & Green)
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🚀 Fast and smooth animations
- 📧 Contact form with backend integration
- 🔒 Secure API endpoints
- 📊 Admin panel for content management

## Project Structure

```
BENCYN/
├── frontend/          # React application
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/           # Django application
│   ├── api/           # API app
│   ├── bencyn_susu/   # Django project settings
│   └── manage.py
└── README.md
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory (copy from `.env.example`):
```bash
cp .env.example .env
```

6. Update the `.env` file with your settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

7. Run migrations:
```bash
python manage.py migrate
```

8. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

9. Start the development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

## API Endpoints

- `GET /api/services/` - List all active services
- `GET /api/testimonials/` - List featured testimonials
- `POST /api/contact/` - Submit a contact form message
- `GET /api/contact/list/` - List all contact messages (admin)

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` after creating a superuser.

## Color Scheme

The website uses colors adapted from the company logo:

- **Primary Orange**: `#FF8C00` - Used for primary actions and accents
- **Primary Green**: `#7FFF00` - Used for secondary actions and highlights
- **Neutral Colors**: Various shades of gray for text and backgrounds

## Pages

- **Home**: Hero section, features, statistics, and call-to-action
- **About**: Company story, values, timeline, mission, and vision
- **Services**: Detailed service offerings with features
- **Contact**: Contact form and company information

## Development

### Frontend Development

The React app uses:
- React Router for navigation
- Framer Motion for animations
- Axios for API calls
- Custom CSS with CSS Variables

### Backend Development

The Django backend provides:
- RESTful API endpoints
- Admin interface for content management
- CORS configuration for frontend integration
- SQLite database (can be changed to PostgreSQL for production)

## Production Deployment

### Frontend

1. Build the production bundle:
```bash
cd frontend
npm run build
```

2. Deploy the `build` folder to your hosting service (Netlify, Vercel, etc.)

### Backend

1. Set `DEBUG=False` in your production environment
2. Update `ALLOWED_HOSTS` in `settings.py`
3. Configure a production database (PostgreSQL recommended)
4. Set up proper static file serving
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Configure environment variables securely

## License

This project is proprietary software for B.C BENCYN SUSU.

## Support

For questions or support, please contact the development team.
