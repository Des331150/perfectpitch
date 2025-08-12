from django.test import TestCase
from django.template import Context, Template


class TemplateTagsTest(TestCase):
    def test_custom_filters(self):
        # Test your custom template filters here
        template = Template("{% load your_template_tags %}{{ value|your_filter }}")
        context = Context({"value": "test"})
        rendered = template.render(context)
        self.assertEqual(rendered, "expected_output")
