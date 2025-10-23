# EvolveEdu.AI

A comprehensive learning platform combining AI-powered features with personalized education.

## Features
- AI-powered notes and summaries
- Auto-generated study planner
- Quiz and roadmap creation
- Personalized AI tutor

## Usage Tips
- Use the planner to organize your study week
- Generate notes from YouTube links or text
- Create quizzes for self-assessment
- Explore roadmaps for skill progression
- Chat with the AI tutor for instant help

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jayanth0075/EvolveED.ai.git
cd EvolveED.ai
```

2. Set up Python virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
npm install
npm run install:all
```

### Running the Application

#### Development Mode
Run both frontend and backend together:
```bash
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
