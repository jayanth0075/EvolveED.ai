# notes/ai_service.py
import openai
import requests
import PyPDF2
import io
from urllib.parse import urlparse, parse_qs
from django.conf import settings
import json
import re

openai.api_key = settings.OPENAI_API_KEY


class NotesAIService:

    @staticmethod
    def extract_youtube_video_id(url):
        """Extract video ID from YouTube URL"""
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            if parsed_url.path[:7] == '/embed/':
                return parsed_url.path.split('/')[2]
            if parsed_url.path[:3] == '/v/':
                return parsed_url.path.split('/')[2]
        return None

    @staticmethod
    def get_youtube_transcript(video_id):
        """Get transcript from YouTube video (mock implementation)"""
        # In real implementation, you would use youtube-transcript-api
        # For now, we'll return a mock transcript
        return f"Mock transcript for video {video_id}. This would contain the actual video content in a real implementation."

    @staticmethod
    def extract_pdf_text(pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"

    @staticmethod
    def generate_notes_from_text(text, title="", source_type="text"):
        """Generate structured notes using OpenAI"""
        try:
            prompt = f"""
            Create comprehensive study notes from the following {source_type} content.
            Title: {title}

            Content:
            {text[:4000]}  # Limit content length for API

            Please provide:
            1. A clear summary (2-3 paragraphs)
            2. Key points (bullet points)
            3. Important concepts or definitions
            4. Study questions (5-10 questions)
            5. Difficulty level (Beginner/Intermediate/Advanced)
            6. Estimated reading time in minutes

            Format the response as JSON with the following structure:
            {{
                "summary": "...",
                "content": "Full detailed notes...",
                "key_points": ["point1", "point2", ...],
                "questions": ["question1", "question2", ...],
                "difficulty_level": "...",
                "estimated_read_time": number,
                "tags": ["tag1", "tag2", ...]
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an AI tutor that creates comprehensive study notes. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            # Fallback response if AI fails
            return {
                "summary": f"Summary of {title}: This content covers important topics that require further study.",
                "content": f"Detailed Notes:\n\n{text[:2000]}...",
                "key_points": ["Key concept 1", "Key concept 2", "Key concept 3"],
                "questions": [
                    "What are the main topics covered?",
                    "How can this knowledge be applied?",
                    "What are the key takeaways?"
                ],
                "difficulty_level": "Intermediate",
                "estimated_read_time": max(1, len(text) // 250),
                "tags": ["study", "notes", source_type]
            }

    @staticmethod
    def process_youtube_url(url, title=""):
        """Process YouTube URL and generate notes"""
        video_id = NotesAIService.extract_youtube_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        # Get transcript (mock for now)
        transcript = NotesAIService.get_youtube_transcript(video_id)

        if not title:
            title = f"YouTube Video Notes - {video_id}"

        return NotesAIService.generate_notes_from_text(transcript, title, "YouTube video")

    @staticmethod
    def process_pdf_file(pdf_file, title=""):
        """Process PDF file and generate notes"""
        text = NotesAIService.extract_pdf_text(pdf_file)

        if not title:
            title = f"PDF Notes - {pdf_file.name}"

        return NotesAIService.generate_notes_from_text(text, title, "PDF document")

    @staticmethod
    def process_text_input(text, title):
        """Process raw text input and generate notes"""
        return NotesAIService.generate_notes_from_text(text, title, "text input")

    @staticmethod
    def enhance_existing_notes(note_content):
        """Enhance existing notes with additional insights"""
        try:
            prompt = f"""
            Enhance the following study notes by adding:
            1. Additional insights
            2. Real-world applications
            3. Memory techniques
            4. Related topics to explore

            Original notes:
            {note_content[:3000]}

            Provide the enhancement as JSON:
            {{
                "insights": ["insight1", "insight2", ...],
                "applications": ["application1", "application2", ...],
                "memory_techniques": ["technique1", "technique2", ...],
                "related_topics": ["topic1", "topic2", ...]
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an AI tutor that enhances study materials. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            return {
                "insights": ["Consider the broader implications of this topic"],
                "applications": ["This knowledge can be applied in practical scenarios"],
                "memory_techniques": ["Create mental associations", "Use spaced repetition"],
                "related_topics": ["Related subject areas worth exploring"]
            }