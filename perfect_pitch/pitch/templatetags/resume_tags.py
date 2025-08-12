from django import template

register = template.Library()


@register.filter
def get_score_class(value):
    """Returns a CSS class based on the score value"""
    try:
        score = int(value)
        if score >= 90:
            return "score-excellent"
        elif score >= 70:
            return "score-good"
        elif score >= 50:
            return "score-fair"
        else:
            return "score-poor"
    except (ValueError, TypeError):
        return ""


@register.filter
def get_suggestions(suggestions_dict, category):
    """Gets suggestions for a specific category from the suggestions dictionary"""
    try:
        suggestions = suggestions_dict.get(category, [])
        return ",".join(suggestions) if suggestions else ""
    except (AttributeError, KeyError):
        return ""


@register.filter
def format_score_label(score_key):
    """Formats a score key into a readable label"""
    return score_key.replace("_", " ").title()
