# notes/ai_service.py
import requests
import PyPDF2
import io
from urllib.parse import urlparse, parse_qs
from django.conf import settings
import json
import re
import time


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
    def call_huggingface_api(prompt, max_retries=3, delay=1):
        """Make API call to Hugging Face with retry logic"""
        headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }

        # Using Flan-T5 for better instruction following and note generation
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload)

                if response.status_code == 503:
                    # Model is loading, wait and retry
                    time.sleep(delay * (attempt + 1))
                    continue
                elif response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', '')
                    return result.get('generated_text', '')
                else:
                    print(f"HuggingFace API error: {response.status_code} - {response.text}")
                    break

            except Exception as e:
                print(f"API call attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay)

        return None

    @staticmethod
    def generate_notes_from_text(text, title="", source_type="text"):
        """Generate structured notes using Hugging Face API"""
        try:
            # Create a more conversational prompt for better results
            prompt = f"""Create comprehensive study notes from this {source_type} content.

Title: {title}

Content: {text[:3000]}

Please provide structured notes with:
1. Summary (2-3 paragraphs)
2. Key points (bullet format)
3. Important concepts
4. Study questions (5-10)
5. Difficulty level
6. Reading time estimate

Format as organized text with clear sections."""

            ai_response = NotesAIService.call_huggingface_api(prompt)

            if ai_response:
                # Parse the AI response and structure it
                parsed_result = NotesAIService.parse_ai_response(ai_response, text, title, source_type)
                return parsed_result
            else:
                raise Exception("Failed to get response from Hugging Face API")

        except Exception as e:
            print(f"AI generation failed: {str(e)}")
            # Fallback response if AI fails
            return NotesAIService.create_fallback_notes(text, title, source_type)

    @staticmethod
    def parse_ai_response(ai_response, original_text, title, source_type):
        """Parse AI response and structure it into the expected format"""
        try:
            # Extract different sections from the AI response
            summary = NotesAIService.extract_section(ai_response, ["summary", "overview"], 2)
            key_points = NotesAIService.extract_bullet_points(ai_response)
            questions = NotesAIService.extract_questions(ai_response)
            difficulty = NotesAIService.extract_difficulty(ai_response)

            # Generate tags based on content
            tags = NotesAIService.generate_tags(original_text, source_type)

            return {
                "summary": summary,
                "content": f"Detailed Notes for {title}:\n\n{ai_response}",
                "key_points": key_points,
                "questions": questions,
                "difficulty_level": difficulty,
                "estimated_read_time": max(1, len(original_text) // 250),
                "tags": tags
            }
        except Exception as e:
            print(f"Parsing failed: {str(e)}")
            return NotesAIService.create_fallback_notes(original_text, title, source_type)

    @staticmethod
    def extract_section(text, keywords, min_sentences=1):
        """Extract a specific section from AI response"""
        text_lower = text.lower()
        lines = text.split('\n')

        for keyword in keywords:
            for i, line in enumerate(lines):
                if keyword in line.lower() and len(line.strip()) > 0:
                    # Found section header, extract following content
                    section_text = []
                    for j in range(i + 1, min(i + 5, len(lines))):
                        if lines[j].strip():
                            section_text.append(lines[j].strip())

                    if section_text:
                        return ' '.join(section_text[:3])  # Take first 3 non-empty lines

        # Fallback: return first few sentences
        sentences = text.split('.')[:min_sentences + 1]
        return '. '.join(sentences).strip()

    @staticmethod
    def extract_bullet_points(text):
        """Extract bullet points from AI response"""
        points = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            # Look for various bullet point formats
            if (line.startswith('•') or line.startswith('-') or
                    line.startswith('*') or re.match(r'^\d+\.', line)):
                clean_point = re.sub(r'^[•\-*\d\.]\s*', '', line)
                if clean_point and len(clean_point) > 10:
                    points.append(clean_point)

        # If no bullet points found, extract key sentences
        if not points:
            sentences = text.split('.')
            for sentence in sentences[:5]:
                if len(sentence.strip()) > 20:
                    points.append(sentence.strip())

        return points[:8]  # Limit to 8 points

    @staticmethod
    def extract_questions(text):
        """Extract questions from AI response"""
        questions = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if line.endswith('?') and len(line) > 10:
                questions.append(line)

        # If no questions found, generate some basic ones
        if not questions:
            questions = [
                "What are the main topics covered in this content?",
                "How can this knowledge be practically applied?",
                "What are the key concepts to remember?",
                "What questions remain unanswered?"
            ]

        return questions[:10]  # Limit to 10 questions

    @staticmethod
    def extract_difficulty(text):
        """Determine difficulty level from AI response"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['advanced', 'complex', 'difficult', 'expert']):
            return "Advanced"
        elif any(word in text_lower for word in ['intermediate', 'moderate', 'medium']):
            return "Intermediate"
        else:
            return "Beginner"

    @staticmethod
    def generate_tags(text, source_type):
        """Generate relevant tags based on content"""
        tags = [source_type, "study", "notes"]

        # Simple keyword extraction for tags
        common_academic_terms = [
            'science', 'mathematics', 'history', 'literature', 'technology',
            'business', 'economics', 'psychology', 'medicine', 'engineering',
            'art', 'philosophy', 'education', 'research', 'analysis'
        ]

        text_lower = text.lower()
        for term in common_academic_terms:
            if term in text_lower:
                tags.append(term)
                if len(tags) >= 6:  # Limit tags
                    break

        return tags

    @staticmethod
    def create_fallback_notes(text, title, source_type):
        """Create fallback notes when AI fails"""
        return {
            "summary": f"Summary of {title}: This content covers important topics that require further study. The material appears to contain valuable information for learning and reference.",
            "content": f"Detailed Notes for {title}:\n\n{text[:2000]}{'...' if len(text) > 2000 else ''}",
            "key_points": [
                "This content contains important information",
                "Further analysis and study is recommended",
                "Key concepts should be reviewed carefully"
            ],
            "questions": [
                "What are the main topics covered?",
                "How can this knowledge be applied?",
                "What are the key takeaways?",
                "What additional research might be helpful?"
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
        """Enhance existing notes with additional insights using Hugging Face"""
        try:
            prompt = f"""Enhance these study notes by adding insights, applications, and study techniques:

Original notes: {note_content[:2500]}

Please provide:
- Additional insights
- Real-world applications  
- Memory techniques
- Related topics to explore

Format as clear sections with specific suggestions."""

            ai_response = NotesAIService.call_huggingface_api(prompt)

            if ai_response:
                # Parse enhancement response
                return {
                    "insights": NotesAIService.extract_enhancement_section(ai_response, "insight"),
                    "applications": NotesAIService.extract_enhancement_section(ai_response, "application"),
                    "memory_techniques": NotesAIService.extract_enhancement_section(ai_response, "memory"),
                    "related_topics": NotesAIService.extract_enhancement_section(ai_response, "topic")
                }
            else:
                raise Exception("Failed to get enhancement from Hugging Face API")

        except Exception as e:
            print(f"Enhancement failed: {str(e)}")
            return {
                "insights": ["Consider the broader implications of this topic"],
                "applications": ["This knowledge can be applied in practical scenarios"],
                "memory_techniques": ["Create mental associations", "Use spaced repetition"],
                "related_topics": ["Related subject areas worth exploring"]
            }

    @staticmethod
    def extract_enhancement_section(text, section_type):
        """Extract specific enhancement sections from AI response"""
        lines = text.split('\n')
        items = []

        for line in lines:
            line = line.strip()
            if section_type.lower() in line.lower() or any(marker in line for marker in ['•', '-', '*']):
                clean_line = re.sub(r'^[•\-*\d\.]\s*', '', line)
                if clean_line and len(clean_line) > 10:
                    items.append(clean_line)

        # Fallback: extract relevant sentences
        if not items:
            sentences = text.split('.')
            for sentence in sentences[:3]:
                if len(sentence.strip()) > 15:
                    items.append(sentence.strip())

        return items[:4]  # Limit to 4 items per section