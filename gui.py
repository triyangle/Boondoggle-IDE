#gui stuff here
from tkinter import *
import tkinter.font as font
from speech2text import *
import threading

class Application(Frame):
    def __init__(self, master):
        """Creates the structure and functionality of the application."""
        Frame.__init__(self, master)
        self.myfont = font.Font(family='Helvetica', size=24) # Customizable font
        self.recording = False
        self.s2t = Speech2Text()

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Creates and grids all of the necessary widgets for the application."""
        # Syntax examples:
        # self.korean_label = Label(self, font = self.myfont)
        # self.korean_label.grid(row = 0, column = 1, sticky = W)
        # self.english_button = Button(self, text = "Meaning?", command = self.show_korean, font = self.myfont, underline = 0)
        # self.english_button.grid(row = 3, column = 0, sticky = W)
        self.record_button = Button(self, text = "Record", command = self.record_toggle, font = self.myfont, underline = 0)
        self.record_button.grid(row=0, column=0, sticky=W)

        self.print_button = Button(self, text = "Print", command = self.myprint, font = self.myfont, underline = 0)
        self.print_button.grid(row=0, column=1, sticky=W)

        self.clear_button = Button(self, text = "Clear", command = self.clear, font = self.myfont, underline = 0)
        self.clear_button.grid(row=0, column=2, sticky=W)

        self.text = Text(self, width=35, height = 5, font = self.myfont, wrap = WORD)
        self.text.insert(0.0, "Text")
        self.text.grid(row=1, column=0, columnspan = 3, sticky=W)

    def record_toggle(self):
        """Toggles the recording of speech."""
        self.recording = not self.recording
        if self.recording:
            print("Starting thread")
            self.record_thread = threading.Thread(target=self.record)
            self.record_thread.daemon = True
            self.record_thread.start()

    def record(self):
        """Records speech and turns it into the string self.s2t.raw_result"""
        while self.recording:
            self.code = self.s2t.process()
        print("Ending thread")

    def myprint(self):
        print(self.code)
        self.text.insert(0.0, self.code)

    def clear(self):
        self.text.delete(0.0, END)

def run():
    """Starts the program."""
    root = Tk()
    root.title("Speech to Code")
    root.geometry("600x280")
    app = Application(root)
    # Keyboard shortcut syntax: app.bind_all("n", app.your_method_here)
    root.lift()
    root.mainloop()

if __name__ == "__main__":
    run()
