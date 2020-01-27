# This is for starting up the server

from flask_login import LoginManager
from voting_system.VotingSystem import app, read_student_text_file, read_candadates_text_file
from voting_system.models import Student, Candidate
import subprocess as sub
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, Button
import csv
import pandas as pd
import matplotlib as plt
from matplotlib.pyplot import subplots


# flask run --host=0.0.0.0 fore external access
# pip freeze > requirements.txt #auto updates all the requirements and the packages


# TODO: Make that a gui of starting server + Loading the text file of students + candidates

class start_server_gui(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()
        self.app = None

    def initUI(self):
        self.parent.title("File dialog")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="open candidates", command=self.onOpen)
        fileMenu.add_command(label="open student", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.parent.title("student server setup")
        button_widget = Button(self.parent, text="Start Server", command=self.start_server)
        button_widget.pack()
        button_widget = Button(self.parent, text="Stop Server", command=self.stop_server)
        button_widget.pack()
        button_widget = Button(self.parent, text="Visualise Votes", command=visualise_votes)
        button_widget.pack()

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

    def onOpen(self):
        ftypes = [('csv files', '*.csv'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text

    def start_server(self):
        # Can use cfg files by parsing as VOTINGSYS_SETTINGS=path/to/Config/file.cfg
        # overrides the the setting from the previous setting
        app.config.from_object("config.DevelopmentConfig")
        try:
            app.config.from_envvar('APP_CONFIG_FILE')
        except RuntimeError:
            pass
        except:
            pass
        read_student_text_file('voting_system/RandomStudents.csv', remove_dups=True)
        read_candadates_text_file('voting_system/RandomCandidates.csv', remove_dups=True)
        self.app = app.run(port=2222)

    def stop_server(self):
        raise RuntimeError("Server going down")

def visualise_votes():
    df = pd.read_csv(r"G:\sampledata.csv")
    df = df.set_index("first_name")

    fig, ax = subplots()

    df.plot(kind='bar', ax=ax)

    ax.grid(color='gray', linestyle='-', alpha=0.3)

    plt.show()

def main():
    root = Tk()
    ex = start_server_gui(root)
    root.geometry("500x500")
    root.mainloop()


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

if __name__ == "__main__":
    main()
    

