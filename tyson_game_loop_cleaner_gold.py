import os
import re
import shutil
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

VERSION = "Tyson Game Loop Cleaner Gold"
AUTHOR = "Tyson 2026"
DISCORD = "t.y.s.o.n1"

HEADER_BY_EXT = {
    ".py": [
        "# --------------------------------------------------",
        "# Tyson Game Loop Cleaner",
        "# Author: Tyson 2026",
        "# Discord: t.y.s.o.n1",
        "# Copyright (c) 2026 Tyson. All rights reserved.",
        "# --------------------------------------------------",
        ""
    ],
    ".js": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".ts": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".cs": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".cpp": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".c": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".java": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".go": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".rs": [
        "// --------------------------------------------------",
        "// Tyson Game Loop Cleaner",
        "// Author: Tyson 2026",
        "// Discord: t.y.s.o.n1",
        "// Copyright (c) 2026 Tyson. All rights reserved.",
        "// --------------------------------------------------",
        ""
    ],
    ".lua": [
        "-- --------------------------------------------------",
        "-- Tyson Game Loop Cleaner",
        "-- Author: Tyson 2026",
        "-- Discord: t.y.s.o.n1",
        "-- Copyright (c) 2026 Tyson. All rights reserved.",
        "-- --------------------------------------------------",
        ""
    ]
}

EXCLUDED_DIRS = {
    ".git", "node_modules", "venv", "__pycache__", "dist", "build",
    ".idea", ".vscode", "bin", "obj", ".pytest_cache"
}

TARGET_EXTENSIONS = {
    ".py", ".js", ".ts", ".cs", ".cpp", ".c", ".java", ".go",
    ".rs", ".lua", ".h", ".hpp"
}

COMMON_BLOCK_MARKERS = [
    ("# GAME LOOP START", "# GAME LOOP END"),
    ("// GAME LOOP START", "// GAME LOOP END"),
    ("/* GAME LOOP START */", "/* GAME LOOP END */"),
    ("-- GAME LOOP START", "-- GAME LOOP END"),
    ("<GAME LOOP START>", "<GAME LOOP END>")
]

COMMON_LOOP_PATTERNS = [
    r"\n\s*while\s+True\s*:\s*.*?(?=\n\s*(def\s+\w+|class\s+\w+|if\s+__name__\s*==\s*[\"']__main__[\"']|async\s+def\s+\w+|for\s+\w+\s+in\s+|while\s+\w+|print\s*\(|return\s+|$))",
    r"\n\s*while\s+true\s*:\s*.*?(?=\n\s*(def\s+\w+|class\s+\w+|if\s+__name__\s*==\s*[\"']__main__[\"']|async\s+def\s+\w+|for\s+\w+\s+in\s+|while\s+\w+|print\s*\(|return\s+|$))",
    r"\n\s*setInterval\s*\([^\n]*\)\s*;?\s*",
    r"\n\s*requestAnimationFrame\s*\([^\n]*\)\s*;?\s*",
    r"\n\s*game_loop\s*\([^\n]*\)\s*;?\s*",
    r"\n\s*while\s*\([^\)]*\)\s*\{.*?\}\s*",
    r"\n\s*for\s*\([^\)]*\)\s*\{.*?\}\s*",
]

class GoldApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tyson Game Loop Cleaner")
        self.geometry("980x700")
        self.minsize(980, 700)
        self.configure(bg="#1a1205")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#1a1205")
        self.style.configure("TLabel", background="#1a1205", foreground="#fef3c7", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="#2b1d08", foreground="#fef3c7")
        self.style.configure("TCheckbutton", background="#1a1205", foreground="#fef3c7")
        self.style.configure("Gold.TButton", background="#facc15", foreground="#1a1205", font=("Segoe UI", 10, "bold"))
        self.style.configure("Blue.TButton", background="#f59e0b", foreground="#1a1205", font=("Segoe UI", 10, "bold"))
        self.style.configure("Dark.TButton", background="#3a2d14", foreground="#fef3c7", font=("Segoe UI", 10, "bold"))

        self.target_path = tk.StringVar(value="")
        self.backup = tk.BooleanVar(value=True)
        self.dry_run = tk.BooleanVar(value=False)

        self.make_ui()

    def make_ui(self):
        top = tk.Frame(self, bg="#1a1205", padx=24, pady=18)
        top.pack(fill="x")

        title = tk.Label(top, text="Tyson Game Loop Cleaner", bg="#1a1205", fg="#facc15", font=("Segoe UI", 26, "bold"))
        title.pack(anchor="w")

        sub = tk.Label(top, text=f"Author: {AUTHOR}   •   Discord: {DISCORD}", bg="#1a1205", fg="#f5d38f", font=("Segoe UI", 10))
        sub.pack(anchor="w", pady=(6, 0))

        main = tk.Frame(self, bg="#231809", padx=20, pady=20)
        main.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        row = tk.Frame(main, bg="#231809")
        row.pack(fill="x")

        tk.Label(row, text="Project Folder", bg="#231809", fg="#fef3c7", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.path_entry = tk.Entry(row, textvariable=self.target_path, width=70, bg="#2b1d08", fg="#fef3c7", insertbackground="#fef3c7", bd=1, relief="solid")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(12, 10))

        ttk.Button(row, text="Browse", command=self.select_folder, style="Blue.TButton").pack(side="left")

        options = tk.Frame(main, bg="#231809", pady=14)
        options.pack(fill="x")
        ttk.Checkbutton(options, text="Create backup (.bak)", variable=self.backup).pack(side="left")
        ttk.Checkbutton(options, text="Dry run only", variable=self.dry_run).pack(side="left", padx=(18, 0))

        buttons = tk.Frame(main, bg="#231809", pady=10)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Clean Project", command=self.start_cleaning, style="Gold.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons, text="Clear Log", command=self.clear_log, style="Dark.TButton").pack(side="left")

        log_wrap = tk.Frame(main, bg="#231809")
        log_wrap.pack(fill="both", expand=True)
        tk.Label(log_wrap, text="Activity Log", bg="#231809", fg="#fef3c7", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))

        self.log_text = tk.Text(log_wrap, bg="#120d05", fg="#fef3c7", insertbackground="#fef3c7", height=18, wrap="word", padx=12, pady=12, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True)

        self.log("Gold edition is ready.")
        self.log(f"Version: {VERSION}")
        self.log("Tip: Choose a project folder, then click Clean Project.")

    def log(self, text):
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select target project folder")
        if folder:
            self.target_path.set(folder)
            self.log(f"Selected folder: {folder}")

    def clear_log(self):
        self.log_text.delete("1.0", "end")
        self.log("Log cleared.")

    def start_cleaning(self):
        path = self.target_path.get().strip()
        if not path:
            messagebox.showwarning("No path selected", "Please select a project folder first.")
            return
        if not os.path.exists(path):
            messagebox.showerror("Invalid path", "The selected file or folder does not exist.")
            return

        threading.Thread(target=self.run_cleaner, args=(path,), daemon=True).start()

    def run_cleaner(self):
        try:
            target = Path(self.target_path.get())
            self.log("Starting scan...")
            count = self.clean_path(target, backup=self.backup.get(), dry_run=self.dry_run.get())
            self.log(f"Completed successfully. Files processed: {count}")
            messagebox.showinfo("Done", f"Processing finished. {count} file(s) handled.")
        except Exception as exc:
            self.log(f"[ERROR] {exc}")
            messagebox.showerror("Error", str(exc))

    def add_header(self, content, file_path):
        header = HEADER_BY_EXT.get(file_path.suffix.lower())
        if not header:
            return content
        if "Tyson Game Loop Cleaner" in content:
            return content
        return "\n".join(header) + "\n\n" + content

    def create_backup(self, file_path):
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        if backup_path.exists():
            backup_path.unlink()
        shutil.copy2(file_path, backup_path)
        return backup_path

    def strip_marked_blocks(self, content):
        for start, end in COMMON_BLOCK_MARKERS:
            pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL | re.IGNORECASE)
            content = pattern.sub("", content)
        return content

    def strip_common_loop_patterns(self, content):
        for pattern in COMMON_LOOP_PATTERNS:
            content = re.sub(pattern, "\n", content, flags=re.DOTALL | re.IGNORECASE)
        return content

    def clean_file(self, file_path, backup=False):
        try:
            original = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                original = file_path.read_text(encoding="latin-1")
            except Exception:
                return False
        except Exception:
            return False

        new_content = self.strip_marked_blocks(original)
        new_content = self.strip_common_loop_patterns(new_content)
        new_content = self.add_header(new_content, file_path)

        if new_content == original:
            return False

        if backup:
            self.create_backup(file_path)

        file_path.write_text(new_content, encoding="utf-8")
        return True

    def should_process(self, file_path):
        return file_path.is_file() and file_path.suffix.lower() in TARGET_EXTENSIONS

    def clean_path(self, root, backup=False, dry_run=False):
        changed = 0
        for item in root.iterdir():
            if item.name in EXCLUDED_DIRS:
                continue
            if item.is_dir():
                changed += self.clean_path(item, backup=backup, dry_run=dry_run)
                continue
            if self.should_process(item):
                if dry_run:
                    self.log(f"[DRY RUN] {item}")
                    changed += 1
                else:
                    if self.clean_file(item, backup):
                        self.log(f"[CLEANED] {item}")
                        changed += 1
                    else:
                        self.log(f"[UNCHANGED] {item}")
        return changed

if __name__ == "__main__":
    app = GoldApp()
    app.mainloop()
