import pymupdf
import re
from typing import Optional
from openai import OpenAI
import json  # Import json module for parsing JSON responses

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="<Chatbot_key>",
)


def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    # Remove extra whitespace and normalize line endings
    text = re.sub(r"\s+", " ", text)
    # Remove special characters but keep punctuation
    text = re.sub(r"[^\w\s.,!?-]", "", text)
    return text.strip()


def extract_text_from_pdf(filepath: str) -> Optional[str]:
    """Extract and preprocess text from PDF file"""
    try:
        with pymupdf.open(filepath) as doc:
            # Check if PDF is empty
            if doc.page_count == 0:
                print("PDF file is empty.")
                return None

            # Check if PDF is password protected
            if doc.needs_pass:
                print("PDF is password protected.")
                return None

            # Extract text from all pages
            full_text = ""
            for page in doc:
                full_text += page.get_text()

            # Clean and normalize the text
            cleaned_text = clean_text(full_text)

            # Validate extracted content
            if not cleaned_text:
                print("No text content found in PDF.")
                return None

            return cleaned_text

    except FileNotFoundError:
        print(f"File {filepath} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return None


def analyze_resume(resume_text: str, job_title: str, job_description: str) -> dict:
    """
    Analyze resume content using OpenAI API
    Returns a dictionary with analysis results
    """
    # System message to guide the AI
    system_message = """You are an expert resume analyzer. Analyze the resume and rate it based on the job title and description. The rating can be low if it is bad. Be thorough and detailed. Don't be afraid to point out mistakes or areas for improvement. If there is a lot to improve, don't hesitate to give low scores. This is to help the user. Provide feedback in the following format:
    {
        "tone and style_score": <score 0-100>,
        "structure_score": <score 0-100>,
        "skills_score": <score 0-100>,
        "content_score": <score 0-100>,
        "overall_score": <score 0-100>,
        "suggestions": {
            "tone and style": ["suggestion1", "suggestion2"],
            "structure": ["suggestion1", "suggestion2"],
            "skills": ["suggestion1", "suggestion2"],
            "content": ["suggestion1", "suggestion2"]
        }
    }
    Base your analysis on professional resume writing standards."""

    # Prepare the messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Here is the resume to analyze:\n\n{resume_text}"},
        {"role": "user", "content": f"This is for the position of: {job_title}"},
        {
            "role": "user",
            "content": f"Here is the job description:\n\n{job_description}",
        },
    ]

    try:
        # Make the API call
        response = client.chat.completions.create(
            extra_body={},
            model="openai/gpt-oss-20b:free",
            messages=messages,
            temperature=0.7,  # Add some creativity but keep it professional
        )

        # Parse the response JSON string into a dictionary
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            print(f"Error parsing API response: {e}")
            return None
        except Exception as e:
            print(f"Error processing API response: {e}")
            return None

    except Exception as e:
        print(f"Error during API call: {e}")
        return None


def process_resume(pdf_path: str, job_title: str, job_description: str) -> dict:
    """
    Process a resume PDF and return analysis results
    """
    try:
        # Extract text from PDF
        resume_text = extract_text_from_pdf(pdf_path)
        if not resume_text:
            return {"error": "Could not extract text from PDF", "success": False}

        # Analyze the resume
        analysis = analyze_resume(resume_text, job_title, job_description)
        if not analysis:
            return {"error": "Could not analyze resume", "success": False}

        # Add success flag to the response
        analysis["success"] = True
        return analysis

    except Exception as e:
        print(f"Error processing resume: {e}")
        return {"error": str(e), "success": False}
