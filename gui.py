#gui stuff here
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from speech2text import *
import threading

# Helper functions
def fill():
    """A filler function."""
    print("filled")

def same(f1name, text):
    """Compares a file to a string and returns TRUE iff they are identical."""
    if not f1name:
        return False
    f = open(f1name, mode='r')
    contents = f.read().strip()
    text = text.strip()
    f.close()
    if contents != text:
        return False
    return True


# The main class
class Application(Frame):
    def __init__(self, master):
        """Creates the structure and functionality of the application."""
        Frame.__init__(self, master)
        self.myfont = font.Font(family='Helvetica', size=24) # Customizable font
        self.recording = False
        self.s2t = Speech2Text()
        self.filename = None
        self.code = ''
        self.continyu = False

        image1 = PhotoImage(file='background.gif')
        background_label = Label(self.master, image=image1)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = image1

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Creates and grids all of the necessary widgets for the application."""
        self.record_button = Button(self.master, text = "Record", command = self.record_toggle, font = self.myfont, underline = 0)
        self.record_button.grid(row=0, column=0, sticky=W)

        self.print_button = Button(self.master, text = "Print", command = self.myprint, font = self.myfont, underline = 0)
        self.print_button.grid(row=0, column=1, sticky=W)

        self.clear_button = Button(self.master, text = "Clear", command = self.clear, font = self.myfont, underline = 0)
        self.clear_button.grid(row=0, column=2, sticky=W)

        self.text = Text(self.master, width=35, height = 5, font = self.myfont, wrap = WORD)
        self.text.insert(0.0, "")
        self.text.grid(row=1, column=0, columnspan = 3, sticky=W)

        self.menubar = Menu(self.master)
        self.fileMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New", command=self.new)
        self.fileMenu.add_command(label="Open", command=self.open)
        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_command(label="Save as", command=self.save_as)
        self.master.config(menu=self.menubar)

    def create_top_widgets(self):
        """Creates the widgets for the popout menu."""
        self.confirm = Toplevel()
        self.save_button = Button(self.confirm, text="Save", command=self.destroy_save)
        self.dont_button = Button(self.confirm, text="Don't save", command=self.dont_save)
        self.cancel_button = Button(self.confirm, text="Cancel", command=self.confirm.destroy)

        self.save_button.grid(row=0, column=0, sticky=W)
        self.dont_button.grid(row=0, column=1, sticky=W)
        self.cancel_button.grid(row=0, column=2, sticky=W)

    # def create_top_widgets2(self):
    #     """Creates the widgets for the second popout menu."""
    #     self.confirm2 = Toplevel()
    #     self.code_label = Label(self.confirm2, text=self.code)
    #     self.ask_label = Label(self.confirm2, text="Is this correct?")
    #     self.yes_button = Button(self.confirm2, text="Close enough", command=self.yes)
    #     self.no_button = Button(self.confirm2, text="No", command=self.no)
    #     self.code_label.grid(row=0, column=1, columnspan=2, sticky=W)
    #     self.ask_label.grid(row=1, column=1, columnspan=2, sticky=W)
    #     self.yes_button.grid(row=2, column=1, sticky=W)
    #     self.no_button.grid(row=2, column=2, sticky=W)
    #
    # def yes(self):
    #     self.good = True
    #     self.confirm2.destroy()
    #
    # def no(self):
    #     self.good = False
    #     self.confirm2.destroy()

    def record_toggle(self):
        """Toggles the recording of speech."""
        self.recording = not self.recording
        if self.recording:
            print("Starting thread")
            self.s2t.Joe = True
            self.record_thread = threading.Thread(target=self.record)
            self.record_thread.daemon = True
            self.record_thread.start()
        else:
            self.s2t.Joe = False

    def record(self):
        """Records speech and turns it into the string self.s2t.raw_result"""
        while self.recording:
            try:
                self.code = self.s2t.process()
            except MyException:
                pass
            # self.create_top_widgets2()
            # self.master.wait_window(self.confirm2)
            # if self.good:
            #     break
        print("Ending thread")

    def myprint(self):
        """Prints the most recent code and inserts it at the cursor."""
        print(self.code)
        self.text.insert(INSERT, self.code)

    def clear(self):
        """Clears the textbox."""
        self.text.delete(0.0, END)

    def check_save(self):
        """Checks if the file needs to be saved and handles various cases."""
        if not same(self.filename, self.text.get(0.0, END)):
            print(repr(self.text.get(0.0, END)))
            self.create_top_widgets()
            self.master.wait_window(self.confirm)

    def new(self):
        """Creates a new file."""
        self.continyu = False
        self.check_save()
        if self.continyu:
            self.filename = None
            self.text.delete(0.0, END)
        print(self.filename)

    def open(self):
        """Opens a preexisting file."""
        self.continyu = False
        self.check_save()
        if self.continyu:
            self.filename = filedialog.askopenfilename(initialdir="./",title="Select file")
            self.text.delete(0.0, END)
            with open(self.filename, 'r') as f:
                self.text.insert(0.0, f.read())
        print(self.filename)

    def save(self):
        """Saves the current file."""
        self.continyu = True
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(self.text.get(0.0, END))
            print(self.filename)
        else:
            self.save_as()

    def save_as(self):
        """Saves the current file with a new name."""
        self.filename = filedialog.asksaveasfilename(initialdir="./", title="Save as...")
        self.save()

    def destroy_save(self):
        """Saves the current file and destroys the popout menu."""
        self.save()
        self.confirm.destroy()

    def dont_save(self):
        """Does not save and destroys the popout menu."""
        self.continyu = True
        self.confirm.destroy()


def run():
    """Starts the program."""
    root = Tk()
    root.title("Speech to Code")
    root.geometry("800x800")
    app = Application(root)
    # Keyboard shortcut syntax: app.bind_all("n", app.your_method_here)
    root.lift()
    root.mainloop()

if __name__ == "__main__":
    run()
