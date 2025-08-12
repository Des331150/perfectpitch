from django.test import TestCase
from django.template import Context, Template


class TemplateTagsTest(TestCase):
    def test_score_class_filter(self):
        # Test the get_score_class filter
        template = Template("{% load resume_tags %}{{ value|get_score_class }}")

        # Test different score ranges
        test_cases = [
            (95, "score-excellent"),
            (85, "score-good"),
            (65, "score-fair"),
            (45, "score-poor"),
            ("invalid", ""),
        ]

        for score, expected in test_cases:
            context = Context({"value": score})
            rendered = template.render(context)
            self.assertEqual(rendered, expected, f"Failed for score {score}")

    def test_get_suggestions_filter(self):
        # Test the get_suggestions filter
        template = Template(
            "{% load resume_tags %}{{ suggestions|get_suggestions:category }}"
        )

        # Test suggestions dictionary
        suggestions = {
            "tone and style": ["Suggestion 1", "Suggestion 2"],
            "structure": ["Suggestion 3"],
        }

        # Test existing category
        context = Context({"suggestions": suggestions, "category": "tone and style"})
        rendered = template.render(context)
        self.assertEqual(rendered, "Suggestion 1,Suggestion 2")

        # Test non-existent category
        context = Context({"suggestions": suggestions, "category": "nonexistent"})
        rendered = template.render(context)
        self.assertEqual(rendered, "")

        # Test with invalid input
        context = Context({"suggestions": None, "category": "structure"})
        rendered = template.render(context)
        self.assertEqual(rendered, "")

    def test_format_score_label_filter(self):
        # Test the format_score_label filter
        template = Template("{% load resume_tags %}{{ value|format_score_label }}")

        test_cases = [
            ("tone_and_style_score", "Tone And Style Score"),
            ("overall_score", "Overall Score"),
            ("content_score", "Content Score"),
        ]

        for input_value, expected in test_cases:
            context = Context({"value": input_value})
            rendered = template.render(context)
            self.assertEqual(rendered, expected)
