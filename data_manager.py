import tkinter as tk
from tkinter import messagebox
from config import CATEGORY_PRESETS, NOISE_PRESETS, PUNCT_PRESETS, SPELL_PRESETS, WORD_PRESETS

class DataManager:
    def __init__(self):
        self.vars = {
            "category_issue": tk.StringVar(value="No"),
            "category_count": tk.StringVar(value="Single"),
            "noise_issue": tk.StringVar(value="No"),
            "noise_count": tk.StringVar(value="Single"),
            "punct_issue": tk.StringVar(value="No"),
            "punct_count": tk.StringVar(value="Single"),
            "spell_issue": tk.StringVar(value="No"),
            "spell_count": tk.StringVar(value="Single"),
            "word_issues_issue": tk.StringVar(value="No"),
            "word_issues_count": tk.StringVar(value="Single"),
            "add_notes": tk.StringVar(),
            "score": tk.StringVar(value="5/5")
        }
        self.lists = {"category": [], "noise": [], "punct": [], "spell": [], "word_issues": []}

    def add_issue(self, word_var, preset_var, detail_var, lb, key):
        word = word_var.get().strip()
        if not word:
            messagebox.showwarning("Warning", "Word/Phrase field cannot be empty.")
            return
        if preset_var.get() == "Custom (write below)":
            det = detail_var.get().strip()
            if not det:
                messagebox.showwarning("Warning", "Please enter custom detail.")
                return
        else:
            det = preset_var.get()
        self.lists[key].append((word, det))
        lb.insert(tk.END, f"{word} – {det[:50]}{'...' if len(det) > 50 else ''}")
        word_var.set("")

    def delete_from_list(self, lb, target):
        sel = lb.curselection()
        if not sel:
            return
        idx = sel[0]
        if messagebox.askyesno("Delete", "Delete selected item?"):
            lb.delete(idx)
            target.pop(idx)

    def collect_data(self):
        def format_issue(key, presets):
            issue_var = self.vars[f"{key}_issue"]
            count_var = self.vars[f"{key}_count"]
            items = self.lists[key]
            if issue_var.get() == "No":
                return "No issue"
            if not items:
                return "Marked Yes but no issues added!"
            
            if count_var.get() == "Single" or len(items) == 1:
                word, det = items[0]
                if det in presets[:-1]:
                    # Punctuation için özel işleme
                    if key == "punct":
                        return det.replace("bu sözcükten sonra", f"“{word}” sözcüğünden sonra")
                    return det.replace("Bu sözcük", f"“{word}”").replace("Bu konum", f"“{word}”").replace("Bu ses seviyesi", f"“{word}”").replace("İçeriğin", f"“{word}” için içeriğin")
                return det
            else:
                words = [w for w, _ in items]
                det = items[0][1]  # Aynı hata mesajını kullan
                if det in presets[:-1]:
                    words_str = ", ".join(f"“{w}”" for w in words[:-1]) + (f" ve “{words[-1]}”" if len(words) > 1 else f"“{words[0]}”")
                    if key == "punct":
                        return det.replace("bu sözcükten sonra", f"{words_str} sözcüklerinden sonra")
                    return det.replace("Bu sözcük", words_str).replace("Bu konum", words_str).replace("Bu ses seviyesi", words_str).replace("İçeriğin", f"{words_str} için içeriğin")
                return "\n".join(f"- {w} – {d}" for w, d in items)

        return {
            "Category": format_issue("category", CATEGORY_PRESETS),
            "Noise": format_issue("noise", NOISE_PRESETS),
            "Punctuation": format_issue("punct", PUNCT_PRESETS),
            "Spelling": format_issue("spell", SPELL_PRESETS),
            "Word_Issues": format_issue("word_issues", WORD_PRESETS),
            "Notes": self.vars["add_notes"].get().strip() or "—",
            "Score": self.vars["score"].get()
        }