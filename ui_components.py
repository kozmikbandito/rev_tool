import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import FONT, COLPAD, CATEGORY_PRESETS, NOISE_PRESETS, PUNCT_PRESETS, SPELL_PRESETS, WORD_PRESETS, FEEDBACK_TEMPLATES
from data_manager import DataManager
from feedback_generator import FeedbackGenerator

class ScrollableFrame(ttk.Frame):
    """Vertically scrollable frame."""
    def __init__(self, container):
        super().__init__(container)
        canvas = tk.Canvas(self, highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.interior = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=self.interior, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        self.interior.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

class QAFeedbackApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QA Review Form")
        self._apply_font_to_app()
        try:
            self.root.state("zoomed")  # Windows
        except tk.TclError:
            self.root.attributes("-zoomed", True)  # Linux/macOS

        self.data_manager = DataManager()
        self.feedback_generator = FeedbackGenerator()
        self._build_ui()

    def _apply_font_to_app(self):
        """Apply font to application."""
        self.root.option_add("*TLabel*Font", FONT)
        self.root.option_add("*TButton*Font", FONT)
        self.root.option_add("*TEntry*Font", FONT)
        self.root.option_add("*TCombobox*Font", FONT)
        self.root.option_add("*TRadiobutton*Font", FONT)
        self.root.option_add("*Listbox*Font", FONT)

    def _build_ui(self):
        wrapper = ScrollableFrame(self.root)
        wrapper.pack(fill="both", expand=True, padx=4, pady=4)
        form = wrapper.interior
        form.columnconfigure(0, weight=1, uniform="col")
        form.columnconfigure(1, weight=1, uniform="col")
        form.columnconfigure(2, weight=1, uniform="col")

        # Left column
        r0 = 0
        r0 = self._issue_section(form, r0, 0, "Category Issues", "category", CATEGORY_PRESETS)
        r0 = self._issue_section(form, r0, 0, "Noise Level Issues", "noise", NOISE_PRESETS)

        # Middle column
        r1 = 0
        r1 = self._issue_section(form, r1, 1, "Punctuation Issues", "punct", PUNCT_PRESETS)
        r1 = self._issue_section(form, r1, 1, "Spelling Issues", "spell", SPELL_PRESETS)
        r1 = self._issue_section(form, r1, 1, "Word Issues", "word_issues", WORD_PRESETS)

        # Right column
        r2 = 0
        r2 = self._score_section(form, r2, 2)

        # Row alignment
        max_rows = max(r0, r1, r2)
        for i in range(max_rows):
            if i >= r0:
                ttk.Frame(form).grid(row=i, column=0)
            if i >= r1:
                ttk.Frame(form).grid(row=i, column=1)
            if i >= r2:
                ttk.Frame(form).grid(row=i, column=2)

        # Additional notes
        notes = ttk.LabelFrame(form, text="Additional Notes", padding=4)
        notes.grid(row=max_rows, column=0, columnspan=3, sticky="ew", pady=4)
        notes.columnconfigure(0, weight=1)
        ttk.Entry(notes, textvariable=self.data_manager.vars["add_notes"]).grid(
            row=0, column=0, sticky="ew")

        self._summary_section(form, max_rows + 1)

    def _issue_section(self, parent, row, col, title, key, presets):
        lf = ttk.LabelFrame(parent, text=title, padding=4)
        lf.grid(row=row, column=col, sticky="ew",
                padx=(0, COLPAD) if col == 0 else (COLPAD, 0), pady=3)
        lf.columnconfigure(0, weight=1)

        issue_var = self.data_manager.vars[f"{key}_issue"]
        word_var = tk.StringVar()
        preset_var = tk.StringVar(value=presets[0])
        detail_var = tk.StringVar()

        # Yes/No selection
        issue_frame = ttk.Frame(lf)
        issue_frame.grid(row=0, column=0, sticky="ew")
        ttk.Radiobutton(issue_frame, text="Yes", value="Yes", variable=issue_var,
                        command=lambda: self._toggle_issue(issue_var, word_frame, cb, detail_entry, lb, preset_var)).pack(side="left")
        ttk.Radiobutton(issue_frame, text="No", value="No", variable=issue_var,
                        command=lambda: self._toggle_issue(issue_var, word_frame, cb, detail_entry, lb, preset_var)).pack(side="left", padx=10)

        # Word input and add button
        word_frame = ttk.Frame(lf)
        word_frame.grid(row=1, column=0, sticky="ew")
        word_frame.columnconfigure(0, weight=1)
        ttk.Entry(word_frame, textvariable=word_var).pack(side="left", fill="x", expand=True)
        ttk.Button(word_frame, text="Add",
                   command=lambda: self.data_manager.add_issue(word_var, preset_var, detail_var, lb, key)).pack(side="right", padx=(4,0))

        # Preset options
        cb = ttk.Combobox(lf, values=presets, textvariable=preset_var, state="readonly")
        cb.grid(row=2, column=0, sticky="ew", pady=2)
        detail_entry = ttk.Entry(lf, textvariable=detail_var)
        detail_entry.grid(row=3, column=0, sticky="ew")
        detail_entry.grid_remove()

        def preset_changed(*_):
            if preset_var.get() == "Custom (write below)":
                detail_entry.grid()
                detail_entry.focus_set()
            else:
                detail_entry.grid_remove()
                detail_var.set("")

        cb.bind("<<ComboboxSelected>>", preset_changed)
        self._create_tooltip(cb, preset_var)

        # Issue list
        lb = tk.Listbox(lf, height=3)
        lb.grid(row=4, column=0, sticky="ew", pady=2)
        lb.bind("<Double-1>", lambda e: self.data_manager.delete_from_list(lb, self.data_manager.lists[key]))

        self._toggle_issue(issue_var, word_frame, cb, detail_entry, lb, preset_var)
        return row + 1

    def _toggle_issue(self, issue_var, word_frame, cb, detail_entry, lb, preset_var):
        state = "normal" if issue_var.get() == "Yes" else "disabled"
        for widget in word_frame.winfo_children():
            widget.config(state=state)
        cb.config(state=state)
        detail_entry.config(state=state if preset_var.get() == "Custom (write below)" else "disabled")
        lb.config(state=state)
        if state == "disabled":
            for widget in word_frame.winfo_children():
                if isinstance(widget, ttk.Entry):
                    widget.delete(0, tk.END)

    def _score_section(self, parent, row, col):
        lf = ttk.LabelFrame(parent, text="Score Selection", padding=4)
        lf.grid(row=row, column=col, sticky="nsew",
                padx=(COLPAD, 0), pady=3)
        lf.columnconfigure(0, weight=1)

        self.data_manager.vars["score"] = tk.StringVar(value="5/5")
        cb = ttk.Combobox(lf, values=["5/5", "4/5", "3/5", "2/5", "2/5 + SBQ (Wrong Location)", "2/5 + SBQ (Not Natural)", "1/5"], textvariable=self.data_manager.vars["score"], state="readonly")
        cb.grid(row=0, column=0, sticky="ew", pady=2)

        return row + 1

    def _create_tooltip(self, widget, text_var):
        def show_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text_var.get(),
                             background="lightyellow",
                             relief="solid",
                             borderwidth=1,
                             font=FONT,
                             wraplength=400)
            label.pack()
            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def _summary_section(self, parent, row):
        lf = ttk.LabelFrame(parent, text="Feedback Output", padding=4)
        lf.grid(row=row, column=0, columnspan=3, sticky="nsew", pady=6)
        parent.rowconfigure(row, weight=1)
        lf.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)

        self.summary_box = scrolledtext.ScrolledText(lf, height=10, wrap="word")
        self.summary_box.grid(row=0, column=0, sticky="nsew")

        btns = ttk.Frame(lf)
        btns.grid(row=1, column=0, sticky="ew", pady=2)
        btns.columnconfigure(0, weight=1)
        btn_container = ttk.Frame(btns)
        btn_container.grid(row=0, column=1, sticky="e")
        ttk.Button(btn_container, text="Generate Feedback",
                   command=self.generate_feedback).pack(side="left", padx=2)
        ttk.Button(btn_container, text="Copy",
                   command=self.copy_feedback).pack(side="left", padx=2)
        ttk.Button(btn_container, text="Reset",
                   command=self.reset_form).pack(side="left", padx=2)

    def generate_feedback(self):
        feedback = self.feedback_generator.generate_feedback(self.data_manager.collect_data())
        self.summary_box.delete("1.0", tk.END)
        self.summary_box.insert(tk.END, feedback)

    def copy_feedback(self):
        txt = self.summary_box.get("1.0", tk.END)
        if not txt.strip():
            messagebox.showinfo("Info", "Please click 'Generate Feedback' first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(txt)
        # Removed pop-up message

    def reset_form(self):
        self.root.destroy()
        new_root = tk.Tk()
        QAFeedbackApp(new_root)
        new_root.mainloop()