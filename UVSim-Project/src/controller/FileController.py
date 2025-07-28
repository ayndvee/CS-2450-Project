from tkinter import filedialog
from globals.Util import Globals
class FileController:
    def __init__(self, sim, view):
        self.sim = sim
        self.view = view

    def load_program(self):
        ##This opens up the file explorer for the user to select a file
        file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
        if file_path:
            try:
                filename = file_path.split("/")[-1]
                editor_lines = []
                memory_lines = []

                with open(file_path, 'r') as f:
                    for i, line in enumerate(f):
                        if i >= Globals.MEMORYSIZE_LARGE:
                            self.view.print_output("Error: Program is too large")
                            return
                        stripped = line.strip()
                        editor_lines.append(stripped + "\n")
                        memory_lines.append(stripped)

                editor_content = "".join(editor_lines)
                text_widget = self.view.tab_manager.add_tab(title=filename, content = editor_content)
                if self.sim.memory.load_program(memory_lines):
                    word_length = []
                    for line in memory_lines:
                        stripped_word = line.strip()
                        digits_only = stripped_word.lstrip("+-")
                        if digits_only.isdigit():
                            word_length.append(len(digits_only))
                    total_length = max(word_length) if word_length else 0
                    self.sim.memory.word_length = total_length
                    self.view.print_output("Successfully loaded file")
                    self.view.update_display()
                    editor = self.view.get_current_editor()
                    if editor:
                        editor.config(state='normal')
                        editor.delete("1.0", "end")
                        editor.insert("1.0", editor_content)
                        editor.config(state='normal')
                    self.view.update_display()
                        
                else:
                    self.view.print_output("File couldn't be read")
            except Exception as e:
                self.view.print_output(f"Error loading file: {e}")
    def save_file(self):
        """
        Saves the current memory state to a file.
        """
        ##This opens up the file explorer for the user to select a file
        try:
            file_path = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[("Text File", "*.txt")])
            if file_path:
                if self.sim.save_file(file_path.name):
                    self.view.print_output("File saved successfully")
                    self.view.update_display()

                else:
                    raise FileNotFoundError
        except Exception as e:
            self.view.print_output(f"Failed to save file: {e}")