from tkinter import ttk
import tkinter as tk
class TabManager:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.tabs = {}  # tab_id -> text_widget

    def add_tab(self, title="Untitled", content=""):
        frame = tk.Frame(self.notebook)
        text_widget = tk.Text(frame, height=10, width=50, wrap=tk.NONE)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", content)
        self.notebook.add(frame, text=title)
        tab_id = self.notebook.tabs()[-1]
        self.tabs[tab_id] = text_widget
        self.notebook.select(frame)
        return tab_id

    def bind_tab_change(self, callback):
        self.notebook.bind("<<NotebookTabChanged>>", callback, add= "+")

    def get_active_text_widget(self):
        current_tab = self.notebook.select()
        return self.tabs.get(current_tab, None)

    def close_tab(self, tab_id=None):
        if tab_id is None:
            tab_id = self.notebook.select()
        if tab_id in self.tabs:
            self.notebook.forget(tab_id)
            del self.tabs[tab_id]