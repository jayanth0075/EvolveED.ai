# EvolveEdu.AI

A comprehensive AI-powered learning platform combining intelligent features with personalized education.

## ✨ Key Features
- 🤖 **AI-powered Notes & Summaries**: Generate intelligent notes from YouTube, PDFs, and text
- 📅 **Smart Study Planner**: Auto-generated study schedules based on learning goals
- 🎯 **Quiz System**: Create and take adaptive quizzes for skill assessment
- 🗺️ **Career Roadmaps**: Personalized learning paths and career development guides
- 💬 **AI Tutor**: 24/7 intelligent tutor for instant learning support
- 📊 **Progress Tracking**: Monitor your learning journey with detailed analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm 6+

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/jayanth0075/EvolveED.ai.git
cd EvolveED.ai
```

2. **Setup Backend**:
```bash
cd evolveedu-ai/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. **Setup Frontend**:
```bash
cd ../frontend
npm install
npm start
```

### Running Tests
npm run dev
```

Or run them separately:

Backend:
```bash
npm run start:backend
```

Frontend:
```bash
npm run start:frontend
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

#### Production Build
1. Build the frontend:
```bash
npm run build:frontend
```

2. Run the production server:
```bash
cd evolveedu-ai/backend
python manage.py collectstatic
python manage.py runserver
```

Visit http://localhost:8000 to see the application.

## Project Structure

```
EvolveED.ai/
├── evolveedu-ai/
│   ├── backend/         # Django backend
│   │   ├── accounts/    # User authentication
│   │   ├── notes/       # Notes feature
│   │   ├── quizzes/     # Quiz feature
│   │   ├── roadmaps/    # Learning roadmaps
│   │   └── tutor/       # AI tutor feature
│   └── frontend/        # React frontend
│       ├── public/
│       └── src/
├── requirements.txt     # Python dependencies
└── package.json        # Node.js dependencies
```

## Roadmap
- Add more AI models
- Improve UI/UX
- Expand quiz and roadmap features
- Integrate more learning resources

## Frontend Build
To build the frontend, run:
```
npm run build
```

## Backend Run
To run the backend, use:
```
python manage.py runserver
```

## API Usage Example
```
POST /api/notes/
{
  "content": "Your note text here"
}
```

## Environment Setup
Set environment variables in a .env file for secrets and API keys.

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
