from config import FEEDBACK_TEMPLATES, SBQ_FEEDBACK_TEMPLATES

class FeedbackGenerator:
    def generate_feedback(self, data):
        # Check if task should be sent back to queue
        if data["SBQ"] != "No" and data["SBQ"] != "Marked Yes but no SBQ reason added!":
            return self._generate_sbq_feedback(data)
        else:
            return self._generate_normal_feedback(data)
    
    def _generate_sbq_feedback(self, data):
        """Generate feedback for SBQ (Send Back to Queue) cases."""
        sbq_reason = data["SBQ"]
        
        if sbq_reason in SBQ_FEEDBACK_TEMPLATES:
            base_message = SBQ_FEEDBACK_TEMPLATES[sbq_reason]["message"]
        else:
            # Custom SBQ reason
            base_message = f"This task has been sent back to queue. Reason: {sbq_reason}"
        
        # Add JSON context if available
        json_info = data.get("JSON_Info", {})
        context_info = ""
        
        if json_info:
            if json_info.get("category") or json_info.get("subcategory"):
                context_info += f"\n\nTask Details:\n- Selected Category: {json_info.get('category', 'N/A')} - {json_info.get('subcategory', 'N/A')}"
            if json_info.get("noise_level"):
                context_info += f"\n- Selected Noise Level: {json_info.get('noise_level', 'N/A')}"
        
        return f"{base_message}{context_info}"
    
    def _generate_normal_feedback(self, data):
        """Generate normal feedback for regular scoring."""
        score = data["Score"]
        template = FEEDBACK_TEMPLATES[score]
        issues = []

        # Collect issues from different categories
        for key in ["Category", "Noise", "Punctuation", "Spelling", "Word_Issues"]:
            if data[key] != "No issue":
                issues.append(f"{key}: {data[key]}")
        
        if data["Notes"] != "—":
            issues.append(f"Additional Notes: {data['Notes']}")
        
        # Add JSON comparison insights if available
        json_info = data.get("JSON_Info", {})
        if json_info:
            json_insights = self._generate_json_insights(data, json_info)
            if json_insights:
                issues.extend(json_insights)

        issues_text = template["issues"] + "\n" + "\n".join(issues) if issues else template["issues"]
        return f"{template['intro']}\n{issues_text}\n{template['outro']}"
    
    def _generate_json_insights(self, data, json_info):
        """Generate additional insights based on JSON data."""
        insights = []
        
        # Add task context
        if json_info.get("category") and json_info.get("subcategory"):
            insights.append(f"Task Context: {json_info['category']} - {json_info['subcategory']}")
        
        if json_info.get("noise_level"):
            insights.append(f"Reported Noise Level: {json_info['noise_level']}")
        
        if json_info.get("transcription"):
            word_count = len(json_info['transcription'].split())
            insights.append(f"Transcript Length: {word_count} words")
        
        return insights