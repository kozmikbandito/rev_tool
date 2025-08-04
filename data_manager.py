import tkinter as tk
from tkinter import messagebox
from config import PUNCT_PRESETS, WORD_PRESETS

class DataManager:
    def __init__(self):
        self.vars = {
            "cat_issue": tk.StringVar(value="No"),
            "noise_issue": tk.StringVar(value="No"),
            "cat_wrong": tk.StringVar(),
            "cat_corr": tk.StringVar(),
            "cat_note": tk.StringVar(),
            "noise_note": tk.StringVar(),
            "add_notes": tk.StringVar(),
            "score": tk.StringVar(value="5/5")
        }
        self.lists = {"punct": [], "spell": [], "word_issues": []}

    def add_punct(self, word_var, preset_var, detail_var, lb):
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
        self.lists["punct"].append((word, det))
        lb.insert(tk.END, f"{word} – {det[:50]}{'...' if len(det) > 50 else ''}")
        word_var.set("")

    def add_word_issue(self, word_var, preset_var, detail_var, lb):
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
        self.lists["word_issues"].append((word, det))
        lb.insert(tk.END, f"{word} – {det[:50]}{'...' if len(det) > 50 else ''}")
        word_var.set("")

    def add_to_list(self, word_var, detail_var, target, lb):
        word = word_var.get().strip()
        det = detail_var.get().strip()
        if not word:
            messagebox.showwarning("Warning", "Word/Phrase field cannot be empty.")
            return
        target.append((word, det))
        lb.insert(tk.END, f"{word} – {det}")
        word_var.set("")
        detail_var.set("")

    def delete_from_list(self, lb, target):
        sel = lb.curselection()
        if not sel:
            return
        idx = sel[0]
        if messagebox.askyesno("Delete", "Delete selected item?"):
            lb.delete(idx)
            target.pop(idx)

    def collect_data(self):
        def pair(issue, w, c, n):
            if issue.get() == "No":
                return f"No issue{f' ({n.get().strip()})' if n.get().strip() else ''}"
            if w and c:
                inc, cor = w.get().strip(), c.get().strip()
                note = n.get().strip()
                return f"Incorrect: {inc} → Correct: {cor}{f' ({note})' if note else ''}" if (inc or cor) else f"Marked Yes but fields empty!{f' ({note})' if note else ''}"
            return f"Yes{f' ({n.get().strip()})' if n.get().strip() else ''}"

        def fmt_list(lst):
            if not lst:
                return "No issues"
            return "\n".join(f"- {w} – {d}" if d else f"- {w}" for w, d in lst)

        return {
            "Category": pair(self.vars["cat_issue"], self.vars["cat_wrong"], self.vars["cat_corr"], self.vars["cat_note"]),
            "Punctuation": fmt_list(self.lists["punct"]),
            "Spelling": fmt_list(self.lists["spell"]),
            "Word_Issues": fmt_list(self.lists["word_issues"]),
            "Noise": pair(self.vars["noise_issue"], None, None, self.vars["noise_note"]),
            "Notes": self.vars["add_notes"].get().strip() or "—",
            "Score": self.vars["score"].get()
        }