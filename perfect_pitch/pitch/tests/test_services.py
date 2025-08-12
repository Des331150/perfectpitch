from django.test import TestCase
from pitch.services import extract_text_from_pdf, process_resume, analyze_resume
from unittest.mock import patch, MagicMock


class ServicesTest(TestCase):
    def test_extract_text_from_pdf(self):
        # Test with valid PDF
        with open("path/to/test.pdf", "rb") as pdf_file:
            text = extract_text_from_pdf(pdf_file.name)
            self.assertIsNotNone(text)

        # Test with invalid file
        text = extract_text_from_pdf("nonexistent.pdf")
        self.assertIsNone(text)

    @patch("pitch.services.analyze_resume")
    def test_process_resume(self, mock_analyze):
        mock_analyze.return_value = {
            "overall_score": 85,
            "suggestions": {"style": [], "tone": [], "skills": [], "format": []},
        }

        result = process_resume(
            "path/to/test.pdf", "Software Engineer", "Test job description"
        )
        self.assertEqual(result["overall_score"], 85)
