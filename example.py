import tkinter


class MainWindow(object):
    def __init__(self):
        print("initiated ..")
        self.root = tkinter.Tk()

    def __enter__(self):
        print("entered ..")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Main Window is closing, call any function you'd like here!")


with MainWindow() as w:
    w.root.mainloop()

print("end of script ..")
