from config import FEEDBACK_TEMPLATES

class FeedbackGenerator:
    def generate_feedback(self, data):
        score = data["Score"]
        template = FEEDBACK_TEMPLATES[score]
        issues = []

        for key in ["Category", "Noise", "Punctuation", "Spelling", "Word_Issues"]:
            if data[key] != "No issue":
                issues.append(f"{key}: {data[key]}")
        if data["Notes"] != "—":
            issues.append(f"Additional Notes: {data['Notes']}")

        issues_text = template["issues"] + "\n" + "\n".join(issues) if issues else template["issues"]
        return f"{template['intro']}\n{issues_text}\n{template['outro']}"