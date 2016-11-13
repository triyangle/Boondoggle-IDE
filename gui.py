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
        self.escapes = {
                'find':self.goto,
                'terminate':self.record_toggle,
                'clear':self.clear
            }

        self.s2t = Speech2Text(self.escapes)
        self.filename = None
        self.code = self.raw = ''
        self.continyu = False
        self.autocorrect = False

        image1 = PhotoImage(file='background.gif')
        background_label = Label(self.master, image=image1)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = image1

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Creates and grids all of the necessary widgets for the application."""
        self.record_button = Button(self.master, text = "Record", command = self.record_toggle, font = self.myfont)
        self.record_button.grid(row=0, column=0)

        self.clear_button = Button(self.master, text = "Clear", command = self.clear, font = self.myfont)
        self.clear_button.grid(row=0, column=1)

        self.correction_checkbox = Checkbutton(self.master, text = "Autocorrect", command = self.correct, font = self.myfont)
        self.correction_checkbox.grid(row = 0, column = 2)

        self.text = Text(self.master, width=int(self.master.winfo_reqwidth()*2.5//self.myfont['size']), height = self.master.winfo_reqheight()*8//(self.myfont['size']*3)-2, font = self.myfont, wrap = WORD)
        self.text.insert(0.0, "")
        self.text.grid(row=1, column=0, columnspan = 4)

        def tab(arg):
            self.text.insert(INSERT, " " * 4)
            return 'break'

        self.text.bind("<Tab>", tab)

        def vim_v(arg):
            self.text.anchor

        self.menubar = Menu(self.master)
        self.fileMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New", command=self.new)
        self.fileMenu.add_command(label="Open", command=self.open)
        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_command(label="Save as", command=self.save_as)
        self.master.config(menu=self.menubar)

        self.convert_button = Button(self.master, text="Convert", command=self.convert, font=self.myfont)
        self.convert_button.grid(row=0, column=4)
        self.text2 = Text(self.master, width=int(self.master.winfo_reqwidth()*2.5//self.myfont['size']), height = self.master.winfo_reqheight()*8//(self.myfont['size']*3)-2, font = self.myfont, wrap = WORD)
        self.text2.grid(row=1, column=4)

        self.status=Label(self.master, text="Status", bd=1, relief=SUNKEN, anchor=W)
        self.status.grid(row=2,column=0,columnspan=4,sticky=W+E)

    def create_top_widgets(self):
        """Creates the widgets for the popout menu."""
        self.confirm = Toplevel()
        self.prompt_label = Label(self.confirm, text="You have unsaved changes. Do you want to save?")
        self.save_button = Button(self.confirm, text="Save", command=self.destroy_save, underline=1)
        self.dont_button = Button(self.confirm, text="Don't save", command=self.dont_save, underline=1)
        self.cancel_button = Button(self.confirm, text="Cancel", command=self.confirm.destroy, underline=1)

        self.prompt_label.grid(row=0, column=0, columnspan=3, sticky=W)
        self.save_button.grid(row=1, column=0, sticky=W)
        self.dont_button.grid(row=1, column=1, sticky=W)
        self.cancel_button.grid(row=1, column=2, sticky=W)

    def record_toggle(self):
        """Toggles the recording of speech."""
        self.recording = not self.recording
        if self.recording:
            print("Starting thread")
            self.record_button['state'] = DISABLED
            self.s2t.Joe = True
            self.record_thread = threading.Thread(target=self.record)
            self.record_thread.daemon = True
            self.record_thread.start()
            print("Started thread")

    def record(self):
        """Records speech and turns it into the string self.s2t.raw_result"""
        if self.recording:
            try:
                self.code = self.s2t.process(self.autocorrect)
                self.raw = self.s2t.result
            except MyException:
                pass
        self.recording = False
        self.record_button['state'] = NORMAL
        print("Ending thread")
        self.myprint()

    def myprint(self):
        """Prints the most recent code and inserts it at the cursor."""
        print(self.code)

        #self.text.insert(INSERT, self.code)
        self.text2.insert(INSERT, self.raw + ' ')

    def convert(self):
        self.raw = self.text2.get(0.0, END)
        self.code = convertstring(self.raw, self.autocorrect)
        self.text.insert(INSERT, self.code)

    def clear(self):
        """Clears the textbox."""
        self.text.delete(0.0, END)
        self.text2.delete(0.0, END)

    def correct(self):
        """Toggles autocorrection."""
        self.autocorrect = not self.autocorrect

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
        if self.filename:
            self.save()

    def destroy_save(self):
        """Saves the current file and destroys the popout menu."""
        self.save()
        self.confirm.destroy()

    def dont_save(self):
        """Does not save and destroys the popout menu."""
        self.continyu = True
        self.confirm.destroy()

    def goto(self, word):
        txt = self.text2.get(0.0, END)
        index = txt.find(word)
        if index == -1:
            index = len(txt)
        self.text2.mark_set(INSERT, "1.0+{0} chars".format(index))

    def record_toggle_event(self, event):
        self.record_toggle()
    def clear_event(self, event):
        self.clear()
    def convert_event(self, event):
        self.convert()
    def autocorrect_event(self, event):
        self.autocorrect = not self.autocorrect
    def new_event(self, event):
        self.new()
    def open_event(self, event):
        self.open()
    def save_event(self, event):
        self.save()
    def save_as_event(self, event):
        self.save_as()

def run():
    """Starts the program."""
    root = Tk()
    root.title("Boondoggle IDE")
    root.geometry("800x800")
    app = Application(root)
    app.bind_all("<Control-r>", app.record_toggle_event)
    app.bind_all("<Control-c>", app.clear_event)
    app.bind_all("<Control-e>", app.convert_event)
    app.bind_all("<Control-a>", app.autocorrect_event)
    app.bind_all("<Control-n>", app.new_event)
    app.bind_all("<Control-o>", app.open_event)
    app.bind_all("<Control-s>", app.save_event)
    app.bind_all("<Control-S>", app.save_as_event)
    # Keyboard shortcut syntax: app.bind_all("n", app.your_method_here)
    root.lift()

    root.mainloop()

if __name__ == "__main__":
    run()
