from config import FEEDBACK_TEMPLATES

class FeedbackGenerator:
    def generate_feedback(self, data):
        score = data["Score"]
        template = FEEDBACK_TEMPLATES[score]
        issues = []

        if data["Category"] != "No issue":
            issues.append(f"Category: {data['Category']}")
        if data["Punctuation"] != "No issues":
            issues.append(f"Punctuation: {data['Punctuation']}")
        if data["Spelling"] != "No issues":
            issues.append(f"Spelling: {data['Spelling']}")
        if data["Word_Issues"] != "No issues":
            issues.append(f"Word Issues: {data['Word_Issues']}")
        if data["Noise"] != "No issue":
            issues.append(f"Noise Level: {data['Noise']}")
        if data["Notes"] != "—":
            issues.append(f"Additional Notes: {data['Notes']}")

        issues_text = template["issues"] + "\n" + "\n".join(issues) if issues else template["issues"]
        return f"{template['intro']}\n{issues_text}\n{template['outro']}"