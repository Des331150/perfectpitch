from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from pitch.services import extract_text_from_pdf, process_resume, analyze_resume
from unittest.mock import patch, MagicMock
import tempfile
import os


class ServicesTest(TestCase):
    def setUp(self):
        # Create a temporary file
        self.temp_dir = tempfile.mkdtemp()
        self.pdf_path = os.path.join(self.temp_dir, "test_resume.pdf")

        # Create a sample PDF file with proper PDF structure
        pdf_content = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>endobj
4 0 obj<</Length 51>>stream
BT /F1 12 Tf 72 720 Td (Test resume content for testing) Tj ET
endstream endobj
xref
0 5
0000000000 65535 f
0000000010 00000 n
0000000056 00000 n
0000000107 00000 n
0000000192 00000 n
trailer<</Size 5/Root 1 0 R>>
startxref
293
%%EOF"""

        with open(self.pdf_path, "wb") as f:
            f.write(pdf_content)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)
        os.rmdir(self.temp_dir)

    def test_extract_text_from_pdf(self):
        # Test with valid PDF
        text = extract_text_from_pdf(self.pdf_path)
        self.assertIsNotNone(text)

        # Test with invalid file
        text = extract_text_from_pdf("nonexistent.pdf")
        self.assertIsNone(text)

    @patch("pitch.services.extract_text_from_pdf")
    @patch("pitch.services.analyze_resume")
    def test_process_resume(self, mock_analyze, mock_extract):
        # Setup the mock for text extraction
        mock_extract.return_value = "Sample resume text"

        # First test: successful case
        mock_response = {
            "overall_score": 85,
            "tone and style_score": 80,
            "structure_score": 85,
            "skills_score": 90,
            "content_score": 85,
            "suggestions": {
                "tone and style": ["suggestion1"],
                "structure": ["suggestion2"],
                "skills": ["suggestion3"],
                "content": ["suggestion4"],
            },
        }
        mock_analyze.return_value = mock_response

        # Test with valid PDF
        result = process_resume(
            self.pdf_path, "Software Engineer", "Test job description"
        )

        # First verify the result structure
        self.assertIsNotNone(result)
        self.assertIn("success", result)

        # Verify analyze_resume was called with correct arguments
        self.assertTrue(mock_analyze.called)
        args, kwargs = mock_analyze.call_args
        self.assertEqual(args[0], "Sample resume text")  # Check extracted text
        self.assertEqual(args[1], "Software Engineer")
        self.assertEqual(args[2], "Test job description")

        # Verify all expected fields are present
        self.assertTrue(result["success"])
        self.assertEqual(result["overall_score"], 85)

        # Second test: error case
        mock_analyze.reset_mock()
        mock_analyze.return_value = None
        result = process_resume(
            self.pdf_path, "Software Engineer", "Test job description"
        )
        self.assertFalse(result["success"])
        self.assertIn("error", result)

    @patch("pitch.services.client.chat.completions.create")
    def test_analyze_resume(self, mock_chat):
        # Create a proper mock response structure
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content="""{
                        "overall_score": 85,
                        "tone and style_score": 80,
                        "structure_score": 85,
                        "skills_score": 90,
                        "content_score": 85,
                        "suggestions": {
                            "tone and style": ["suggestion1"],
                            "structure": ["suggestion2"],
                            "skills": ["suggestion3"],
                            "content": ["suggestion4"]
                        }
                    }"""
                )
            )
        ]
        mock_chat.return_value = mock_response

        result = analyze_resume(
            "Test resume content",
            "Software Engineer",
            "Python developer with 3+ years experience",
        )

        self.assertIsInstance(result, dict)
        self.assertIn("overall_score", result)
        self.assertIn("suggestions", result)
