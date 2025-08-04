import tkinter as tk
from tkinter import messagebox
import json
from config import CATEGORY_PRESETS, NOISE_PRESETS, PUNCT_PRESETS, SPELL_PRESETS, WORD_PRESETS, SBQ_REASONS

class DataManager:
    def __init__(self):
        self.vars = {
            "category_issue": tk.StringVar(value="No"),
            "noise_issue": tk.StringVar(value="No"),
            "punct_issue": tk.StringVar(value="No"),
            "spell_issue": tk.StringVar(value="No"),
            "word_issues_issue": tk.StringVar(value="No"),
            "sbq_issue": tk.StringVar(value="No"),
            "add_notes": tk.StringVar(),
            "score": tk.StringVar(value="5/5"),
            "json_content": tk.StringVar()
        }
        self.lists = {"category": [], "noise": [], "punct": [], "spell": [], "word_issues": [], "sbq": []}
        self.json_data = None

    def parse_json(self):
        """Parse the JSON content and extract relevant information."""
        try:
            json_text = self.vars["json_content"].get().strip()
            if not json_text:
                return None
            
            self.json_data = json.loads(json_text)
            return self.json_data
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"Invalid JSON format: {str(e)}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing JSON: {str(e)}")
            return None

    def get_json_info(self):
        """Extract useful information from parsed JSON."""
        if not self.json_data:
            return {}
        
        metadata = self.json_data.get("metadata", {})
        
        return {
            "category": metadata.get("category", ""),
            "subcategory": metadata.get("subcategory", ""),
            "noise_level": metadata.get("noiseLevel", ""),
            "transcription": metadata.get("transcription", ""),
            "recording_location": metadata.get("distribution", {}).get("recordingLocation", ""),
            "content_category": metadata.get("distribution", {}).get("category", ""),
            "content_subcategory": metadata.get("distribution", {}).get("subcategory", "")
        }

    def add_issue(self, word_var, preset_var, detail_var, lb, key):
        word = word_var.get().strip()
        if not word:
            messagebox.showwarning("Warning", "Word/Phrase field cannot be empty.")
            return
        if preset_var.get() == "Custom (write below)":
            detail = detail_var.get().strip()
            if not detail:
                messagebox.showwarning("Warning", "Please enter custom detail.")
                return
        else:
            detail = preset_var.get()
        self.lists[key].append((word, detail))
        lb.insert(tk.END, f"{word} – {detail[:50]}{'...' if len(detail) > 50 else ''}")
        word_var.set("")

    def add_sbq_issue(self, preset_var, detail_var, lb):
        """Special method for adding SBQ issues."""
        if preset_var.get() == "Custom (write below)":
            detail = detail_var.get().strip()
            if not detail:
                messagebox.showwarning("Warning", "Please enter custom detail.")
                return
        else:
            detail = preset_var.get()
        
        # For SBQ, we don't need a specific word, just the reason
        self.lists["sbq"].append(("SBQ", detail))
        lb.insert(tk.END, f"SBQ – {detail[:50]}{'...' if len(detail) > 50 else ''}")

    def delete_from_list(self, lb, target):
        selection = lb.curselection()
        if not selection:
            return
        index = selection[0]
        if messagebox.askyesno("Delete", "Delete selected item?"):
            lb.delete(index)
            target.pop(index)

    def collect_data(self):
        def format_issue(key, presets):
            issue_var = self.vars[f"{key}_issue"]
            items = self.lists[key]
            if issue_var.get() == "No":
                return "No issue"
            if not items:
                return "Marked Yes but no issues added!"
            
            # Process single item
            word, detail = items[0]
            if detail in presets[:-1]:
                # Special processing for punctuation
                if key == "punct":
                    return detail.replace("after this word", f'after "{word}"')
                # Replace placeholders for other types
                return detail.replace("This word", f'"{word}"').replace("This location", f'"{word}"').replace("This noise level", f'"{word}"').replace("this word", f'"{word}"')
            return detail

        def format_sbq_issue():
            issue_var = self.vars["sbq_issue"]
            items = self.lists["sbq"]
            if issue_var.get() == "No":
                return "No"
            if not items:
                return "Marked Yes but no SBQ reason added!"
            
            # Return the SBQ reason
            _, detail = items[0]
            return detail

        return {
            "Category": format_issue("category", CATEGORY_PRESETS),
            "Noise": format_issue("noise", NOISE_PRESETS),
            "Punctuation": format_issue("punct", PUNCT_PRESETS),
            "Spelling": format_issue("spell", SPELL_PRESETS),
            "Word_Issues": format_issue("word_issues", WORD_PRESETS),
            "SBQ": format_sbq_issue(),
            "Notes": self.vars["add_notes"].get().strip() or "—",
            "Score": self.vars["score"].get(),
            "JSON_Info": self.get_json_info()
        }