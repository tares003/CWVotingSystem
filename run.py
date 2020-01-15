# This is for starting up the server
from flask_login import LoginManager
from voting_system.VotingSystem import app, read_student_text_file, read_candadates_text_file
from voting_system.models import Student, Candidate
import csv

# flask run --host=0.0.0.0 fore external access
# pip freeze > requirements.txt #auto updates all the requirements and the packages



# TODO: Make that a gui of starting server + Loading the text file of students + candidates
def tk_gui():
    pass




if __name__ == "__main__":
    
    app.config.from_object("config.DevelopmentConfig")

    read_student_text_file('voting_system/RandomStudents.csv',remove_dups=True)
    read_candadates_text_file('voting_system/RandomCandidates.csv',remove_dups=True)


    # Can use cfg files by parsing as VOTINGSYS_SETTINGS=path/to/Config/file.cfg
    # overrides the the setting from the previous setting
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass
    except:
        pass
    app.run(port=2222)

    
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("File dialog")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="open candidates", command=self.onOpen)
        menubar.add_cascade(label="open students", menu=fileMenu)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)


    def onOpen(self):

        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text


def main():

    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()



# import tkinter
# from  tkinter import filedialog
#
#
# if __name__== "__main__":
#     window = tkinter.Tk()
#     window.file_candidates = filedialog.askopenfilename(initialdir="/", title="Open Candidates",
#                                                  filetypes = (("csv files","*.csv"),("all files","*.*")))
#     print(window.file_candidates)
#     window.file_students = filedialog.askopenfilename(initialdir="/", title="Open Candidates",
#                                                  filetypes = (("csv files","*.csv"),("all files","*.*")))
#     print(window.file_students)
#     window.title("Button GUI")
#     button_widget = tkinter.Button(window, text="Start Server")
#     button_widget.pack()
#     button_widget = tkinter.Button(window, text="Stop Server")
#     button_widget.pack()
#     tkinter.mainloop()
    
