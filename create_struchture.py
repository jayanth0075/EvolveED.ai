import os

# Root folder
root = "evolveedu-ai"

# Directories to create
dirs = [
    # Backend
    f"{root}/backend/evolveedu",
    f"{root}/backend/accounts/migrations",
    f"{root}/backend/notes/migrations",
    f"{root}/backend/roadmaps/migrations",
    f"{root}/backend/quizzes/migrations",
    f"{root}/backend/tutor/migrations",
    # Frontend
    f"{root}/frontend/public",
    f"{root}/frontend/src/api",
    f"{root}/frontend/src/components",
    f"{root}/frontend/src/pages",
    f"{root}/frontend/src/styles",
]

# Create directories
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Files with basic placeholders
files = {
    # Backend core
    f"{root}/backend/evolveedu/__init__.py": "",
    f"{root}/backend/evolveedu/settings.py": "# Django settings placeholder\n",
    f"{root}/backend/evolveedu/urls.py": "# Project urls placeholder\n",
    f"{root}/backend/evolveedu/wsgi.py": "# WSGI placeholder\n",
    f"{root}/backend/evolveedu/asgi.py": "# ASGI placeholder\n",

    # Backend apps
    **{f"{root}/backend/{app}/{fname}": f"# {fname} for {app}\n"
       for app in ["accounts","notes","roadmaps","quizzes","tutor"]
       for fname in ["__init__.py","models.py","views.py","serializers.py","urls.py","tests.py"]},

    # Frontend public
    f"{root}/frontend/public/index.html": "<!DOCTYPE html>\n<html><head><title>EvolveEdu.ai</title></head><body><div id='root'></div></body></html>",
    f"{root}/frontend/public/favicon.ico": "",

    # Frontend src
    f"{root}/frontend/src/api/api.js": "// Axios API config placeholder\n",
    f"{root}/frontend/src/components/Navbar.js": "// Navbar component placeholder\n",
    f"{root}/frontend/src/components/Sidebar.js": "// Sidebar component placeholder\n",
    f"{root}/frontend/src/components/Loader.js": "// Loader component placeholder\n",
    f"{root}/frontend/src/components/AnimatedCard.js": "// Animated card placeholder\n",
    f"{root}/frontend/src/components/Modal.js": "// Modal popup placeholder\n",
    **{f"{root}/frontend/src/pages/{page}.js": f"// {page} page placeholder\n"
       for page in ["Login","Signup","Dashboard","Notes","Roadmap","Quiz","Tutor"]},
    f"{root}/frontend/src/styles/global.css": "/* Global styles placeholder */\n",
    f"{root}/frontend/src/styles/components.css": "/* Components styles placeholder */\n",
    f"{root}/frontend/src/styles/animations.css": "/* Animations placeholder */\n",
    f"{root}/frontend/src/App.js": "// App component placeholder\n",
    f"{root}/frontend/src/index.js": "// React entry point placeholder\n",
    f"{root}/frontend/src/routes.js": "// Routes placeholder\n",

    # Root level files
    f"{root}/.env": "# API keys and DB credentials\n",
    f"{root}/requirements.txt": "django\ndjangorestframework\nyoutube-transcript-api\nopenai\ntransformers\ntorch\nsentencepiece\n",
    f"{root}/package.json": "{\n  \"name\": \"evolveedu-frontend\",\n  \"version\": \"1.0.0\"\n}\n",
    f"{root}/README.md": "# EvolveEdu.ai\n",
    f"{root}/backend/manage.py": "# Django manage.py placeholder\n",
    f"{root}/backend/db.sqlite3": "",  # Optional, can be empty
}

# Create files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ EvolveEdu.ai structure created successfully.")
