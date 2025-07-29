from .ExecutionController import ExecutionController
from .FileController import FileController
from .ThemeController import ThemeController
class UVSIM_Controller:
    def __init__(self, sim, view):
        self.sim = sim
        self.view = view

        self.execution = ExecutionController(sim, view)
        self.file = FileController(sim, view, self.execution)
        self.theme = ThemeController(view)

        self.view.bind_controller(self)

    def run(self):
        """Start continuous program execution."""
        self.execution.run()

    def pause(self):
        """Pause the current program execution."""
        self.execution.pause()

    def step(self):
        """Execute a single instruction."""
        self.execution.step()

    def reset(self):
        """Reset the simulator to its initial state."""
        self.execution.reset()

    def submit_input(self):
        """Submit user input to the simulator."""
        self.execution.submit_input()

    def prev_memory(self):
        """Scroll to the previous 10 memory addresses in the view."""
        self.execution.prev_memory()

    def next_memory(self):
        """Scroll to the next 10 memory addresses in the view."""
        self.execution.next_memory()

    def cut_text(self, event=None):
        """Cut selected text from the editor."""
        return self.execution.cut_text(event)

    def copy_text(self, event=None):
        """Copy selected text from the editor."""
        return self.execution.copy_text(event)

    def paste_text(self, event=None):
        """Paste text into the editor."""
        return self.execution.paste_text(event)
    
    def reload_memory_from_editor(self, content_lines):
        """Reload memory using content lines from the editor."""
        self.execution.reload_memory_from_editor(content_lines)

    def load_from_editor(self):
        """Load program instructions from the active editor tab."""
        self.execution.load_from_editor()

    # File delegation
    def load_program(self):
        """Load a program from a file into memory."""
        self.file.load_program()

    def save_file(self):
        """Save the current editor contents to a file."""
        self.file.save_file()

    # Theme delegation
    def change_theme(self):
        """Switch to the newly selected theme."""
        self.theme.change_theme()

    def reset_theme(self):
        """Reset the theme to the default setting."""
        self.theme.reset_theme()