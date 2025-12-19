# Quick Setup Guide

## Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

## Backend Setup

1. **Create and activate virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file:**
   Create a `.env` file in the `backend` directory with:
   ```
   SECRET_KEY=your-secret-key-here-change-in-production
   DEBUG=True
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`

## Running Both Servers

You'll need to run both servers simultaneously:

1. **Terminal 1 - Frontend:**
   ```bash
   cd frontend
   npm start
   ```

2. **Terminal 2 - Backend:**
   ```bash
   cd backend
   python manage.py runserver
   ```

## Notes

- The frontend is configured to communicate with the backend at `http://localhost:8000`
- CORS is configured to allow requests from `http://localhost:3000`
- The logo image is located at `frontend/public/logo.png` and can be used in components if needed

## Troubleshooting

### Frontend Issues
- If port 3000 is in use, React will prompt to use another port
- Clear browser cache if you see old styles

### Backend Issues
- Make sure Python virtual environment is activated
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that `.env` file exists with proper SECRET_KEY

### Database Issues
- If you get database errors, run: `python manage.py migrate`
- To reset database (development only): Delete `db.sqlite3` and run migrations again
