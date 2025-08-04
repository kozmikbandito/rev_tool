import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import FONT, COLPAD, PUNCT_PRESETS, WORD_PRESETS, FEEDBACK_TEMPLATES
from data_manager import DataManager
from feedback_generator import FeedbackGenerator

class ScrollableFrame(ttk.Frame):
    """Dikey kaydırılabilir çerçeve."""
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
        """Uygulamaya font uygula."""
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

        # Sol sütun
        r0 = 0
        r0 = self._pair_issue(form, r0, 0, "CATEGORY issue?",
                              self.data_manager.vars["cat_issue"],
                              self.data_manager.vars["cat_wrong"],
                              self.data_manager.vars["cat_corr"],
                              self.data_manager.vars["cat_note"])
        r0 = self._pair_issue(form, r0, 0, "NOISE LEVEL issue?",
                              self.data_manager.vars["noise_issue"],
                              None, None, self.data_manager.vars["noise_note"])

        # Orta sütun
        r1 = 0
        r1 = self._punct_section(form, r1, 1)
        r1 = self._list_section(form, r1, 1, "Spelling Issues", "spell")
        r1 = self._word_issues_section(form, r1, 1)

        # Sağ sütun
        r2 = 0
        r2 = self._score_section(form, r2, 2)

        # Satır hizalama
        max_rows = max(r0, r1, r2)
        for i in range(max_rows):
            if i >= r0:
                ttk.Frame(form).grid(row=i, column=0)
            if i >= r1:
                ttk.Frame(form).grid(row=i, column=1)
            if i >= r2:
                ttk.Frame(form).grid(row=i, column=2)

        # Ek notlar
        notes = ttk.LabelFrame(form, text="Additional Notes", padding=4)
        notes.grid(row=max_rows, column=0, columnspan=3, sticky="ew", pady=4)
        notes.columnconfigure(0, weight=1)
        ttk.Entry(notes, textvariable=self.data_manager.vars["add_notes"]).grid(
            row=0, column=0, sticky="ew")

        self._summary_section(form, max_rows + 1)

    def _pair_issue(self, parent, row, col, title, issue_var, wrong_var, corr_var, note_var):
        lf = ttk.LabelFrame(parent, text=title, padding=4)
        lf.grid(row=row, column=col, sticky="ew",
                padx=(0, COLPAD) if col == 0 else (COLPAD, 0), pady=3)
        lf.columnconfigure(1, weight=1)
        if wrong_var and corr_var:
            lf.columnconfigure(3, weight=1)
        lf.columnconfigure(5, weight=2)

        ttk.Radiobutton(lf, text="Yes", value="Yes", variable=issue_var,
                        command=lambda: self._toggle_pair(issue_var, w_ent, c_ent, n_ent)).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(lf, text="No", value="No", variable=issue_var,
                        command=lambda: self._toggle_pair(issue_var, w_ent, c_ent, n_ent)).grid(row=0, column=1, sticky="w")

        row_idx = 1
        if wrong_var and corr_var:
            ttk.Label(lf, text="Wrong:").grid(row=row_idx, column=0, sticky="e", padx=2)
            w_ent = ttk.Entry(lf, textvariable=wrong_var, width=15)
            w_ent.grid(row=row_idx, column=1, sticky="ew", padx=2)
            ttk.Label(lf, text="Correct:").grid(row=row_idx, column=2, sticky="e", padx=2)
            c_ent = ttk.Entry(lf, textvariable=corr_var, width=15)
            c_ent.grid(row=row_idx, column=3, sticky="ew", padx=2)
            row_idx += 1
        else:
            w_ent = c_ent = None

        ttk.Label(lf, text="Note:").grid(row=row_idx, column=0, sticky="e", padx=2)
        n_ent = ttk.Entry(lf, textvariable=note_var)
        n_ent.grid(row=row_idx, column=1, columnspan=3 if wrong_var else 5, sticky="ew", padx=2)

        self._toggle_pair(issue_var, w_ent, c_ent, n_ent)
        return row + 1

    @staticmethod
    def _toggle_pair(issue_var, wrong_ent, corr_ent, note_ent):
        if issue_var.get() == "Yes":
            if wrong_ent:
                wrong_ent.config(state="normal")
            if corr_ent:
                corr_ent.config(state="normal")
            note_ent.config(state="normal")
        else:
            if wrong_ent:
                wrong_ent.config(state="disabled")
                wrong_ent.delete(0, tk.END)
            if corr_ent:
                corr_ent.config(state="disabled")
                corr_ent.delete(0, tk.END)
            note_ent.config(state="disabled")
            note_ent.delete(0, tk.END)

    def _punct_section(self, parent, row, col):
        lf = ttk.LabelFrame(parent, text="Punctuation Issues", padding=4)
        lf.grid(row=row, column=col, sticky="ew",
                padx=(0, COLPAD) if col == 0 else (COLPAD, 0), pady=3)
        lf.columnconfigure(0, weight=1)

        word_var = tk.StringVar()
        preset_var = tk.StringVar(value=PUNCT_PRESETS[0])
        detail_var = tk.StringVar()

        word_frame = ttk.Frame(lf)
        word_frame.grid(row=0, column=0, sticky="ew")
        word_frame.columnconfigure(0, weight=1)
        ttk.Entry(word_frame, textvariable=word_var).pack(side="left", fill="x", expand=True)
        ttk.Button(word_frame, text="Add",
                   command=lambda: self.data_manager.add_punct(word_var, preset_var, detail_var, lb)).pack(side="right", padx=(4,0))

        cb = ttk.Combobox(lf, values=PUNCT_PRESETS, textvariable=preset_var, state="readonly")
        cb.grid(row=1, column=0, sticky="ew", pady=2)
        detail_entry = ttk.Entry(lf, textvariable=detail_var)
        detail_entry.grid(row=2, column=0, sticky="ew")
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

        lb = tk.Listbox(lf, height=3)
        lb.grid(row=3, column=0, sticky="ew", pady=2)
        lb.bind("<Double-1>", lambda e: self.data_manager.delete_from_list(lb, self.data_manager.lists["punct"]))

        return row + 1

    def _word_issues_section(self, parent, row, col):
        lf = ttk.LabelFrame(parent, text="Word Issues", padding=4)
        lf.grid(row=row, column=col, sticky="ew",
                padx=(0, COLPAD) if col == 0 else (COLPAD, 0), pady=3)
        lf.columnconfigure(0, weight=1)

        word_var = tk.StringVar()
        preset_var = tk.StringVar(value=WORD_PRESETS[0])
        detail_var = tk.StringVar()

        word_frame = ttk.Frame(lf)
        word_frame.grid(row=0, column=0, sticky="ew")
        word_frame.columnconfigure(0, weight=1)
        ttk.Entry(word_frame, textvariable=word_var).pack(side="left", fill="x", expand=True)
        ttk.Button(word_frame, text="Add",
                   command=lambda: self.data_manager.add_word_issue(word_var, preset_var, detail_var, lb)).pack(side="right", padx=(4,0))

        cb = ttk.Combobox(lf, values=WORD_PRESETS, textvariable=preset_var, state="readonly")
        cb.grid(row=1, column=0, sticky="ew", pady=2)
        detail_entry = ttk.Entry(lf, textvariable=detail_var)
        detail_entry.grid(row=2, column=0, sticky="ew")
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

        lb = tk.Listbox(lf, height=3)
        lb.grid(row=3, column=0, sticky="ew", pady=2)
        lb.bind("<Double-1>", lambda e: self.data_manager.delete_from_list(lb, self.data_manager.lists["word_issues"]))

        return row + 1

    def _list_section(self, parent, row, col, title, key):
        lf = ttk.LabelFrame(parent, text=title, padding=4)
        lf.grid(row=row, column=col, sticky="ew",
                padx=(0, COLPAD) if col == 0 else (COLPAD, 0), pady=3)
        lf.columnconfigure(0, weight=1)

        word_var = tk.StringVar()
        detail_var = tk.StringVar()

        entry_frame = ttk.Frame(lf)
        entry_frame.grid(row=0, column=0, sticky="ew")
        entry_frame.columnconfigure(0, weight=2)
        entry_frame.columnconfigure(1, weight=1)
        ttk.Entry(entry_frame, textvariable=word_var).grid(row=0, column=0, sticky="ew", padx=(0,2))
        ttk.Entry(entry_frame, textvariable=detail_var).grid(row=0, column=1, sticky="ew", padx=(2,2))
        ttk.Button(entry_frame, text="Add",
                   command=lambda: self.data_manager.add_to_list(word_var, detail_var, self.data_manager.lists[key], lb)).grid(row=0, column=2, padx=(2,0))

        lb = tk.Listbox(lf, height=3)
        lb.grid(row=1, column=0, sticky="ew", pady=2)
        lb.bind("<Double-1>", lambda e: self.data_manager.delete_from_list(lb, self.data_manager.lists[key]))

        return row + 1

    def _score_section(self, parent, row, col):
        lf = ttk.LabelFrame(parent, text="Score Selection", padding=4)
        lf.grid(row=row, column=col, sticky="nsew",
                padx=(COLPAD, 0), pady=3)
        lf.columnconfigure(0, weight=1)

        self.data_manager.vars["score"] = tk.StringVar(value="5/5")
        cb = ttk.Combobox(lf, values=["5/5", "4/5", "3/5", "2/5"], textvariable=self.data_manager.vars["score"], state="readonly")
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
        messagebox.showinfo("Copied", "Feedback copied to clipboard.")

    def reset_form(self):
        self.root.destroy()
        new_root = tk.Tk()
        QAFeedbackApp(new_root)
        new_root.mainloop()