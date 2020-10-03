import os
import logging
from tkinter import Tk, ttk, Menu, Text, messagebox
from tkinter.filedialog import askopenfile, asksaveasfile
currentdir = os.path.dirname(os.path.realpath(__file__))
save_extensions = [('Text File', '.txt'),('C source code', '.c'), ('CPP source code','.cpp'), ('Python Source code','.py'), ("Java source code",'.java'),('PHP', '.php'), ('HyperText Markup Language','.html'), ('Comma separated values','.csv')]
open_extensions = [('All Files', '.*'), ('Text File', '.txt'),('C source code', '.c'), ('CPP source code','.cpp'), ('Python Source code','.py'), ("Java source code",'.java'),('PHP', '.php'), ('HyperText Markup Language','.html'), ('Comma separated values','.csv')]
#----------------------------------------------------------------------------
openedfile = "Blank Document"
content = ''
#-----------Functions---------------------------------------------------------
class Editor:
    def __init__(self):
        '''
        Create new editor window
        '''
        global openedfile, content
        self.root = Tk()
        self.root.title("J's TEXT EDITOR:- [{}]".format(openedfile))
        self.root.geometry("600x600")  
        self.input_text = Text(self.root, bg="white", fg="black", font=("Cambria", 12), height="600", width="600")       
        self.input_text.insert("1.0", content)
        self.input_text.pack()
        self.menu()
        self.root.mainloop()

    def menu(self):
        '''
        creates menubar 
        '''
        self.menubar = Menu(self.root)
        self.file = Menu(self.menubar, tearoff=0)
        self.file.add_command(label="New File")
        self.file.add_command(label="Save File", command=lambda:self.save(self.input_text.get("1.0", "end")))
        self.file.add_command(label="Save File As", command=lambda:self.save_as(self.input_text.get("1.0", "end")))
        self.file.add_command(label="Open File", command=self.open_file)
        self.file.add_separator()
        self.file.add_command(label="New Window", command=self.CreateWindow)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=lambda:self.exitRoot(self.input_text.get("1.0", "end")))
        self.menubar.add_cascade(label="File", menu=self.file)
        
        self.edit = Menu(self.menubar, tearoff=0)
        self.edit.add_command(label="Copy")
        self.edit.add_command(label="Cut")
        self.edit.add_separator()
        self.edit.add_command(label="Undo")
        self.edit.add_command(label="Redo")
        self.edit.add_separator()
        self.edit.add_command(label="Select All")
        self.menubar.add_cascade(label="Edit", menu=self.edit)

        self.format = Menu(self.menubar, tearoff=0)
        self.format.add_command(label="Font", command=lambda:self.ChangeFont)
        self.format.add_command(label="Change Mode", command=lambda:self.ChangeMode)
        self.menubar.add_cascade(label="Format", menu=self.format)

        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_command(label="Help")
        self.help.add_separator()
        self.help.add_command(label="About our developer")
        self.help.add_command(label="About Text Editor")
        self.menubar.add_cascade(label="Help", menu=self.help)

        self.root.config(menu=self.menubar)

    def CreateWindow(self):
        self.__init__()
    
    @staticmethod
    def get_path_to_save():
        global save_extensions
        '''
        asks user where to save a file and returns its path
        '''
        path = asksaveasfile(filetypes = save_extensions, defaultextension = save_extensions)
        if path != None:
            return path.name
    
    @staticmethod
    def change_mode():
        #empty
        pass

    def save(self, text_in_editor):
        '''
        Save a file 
        '''
        global openedfile
        if(openedfile == "Blank Document"):
            self.save_as(text_in_editor)
            return
        try:
            file_name = openedfile[:]
            fileref = open(file=str(file_name), mode="w")
            print("Opened: ",fileref.name)
            fileref.write(text_in_editor)
            fileref.close()
            messagebox.showinfo("Success", "File {} Saved succesfully.".format(file_name), parent=self.root)
        except Exception as e:
            messagebox.showerror("Failed", e, parent=self.root)

    def save_as(self, text_in_editor):
        '''
        Save a file as
        '''
        global openedfile
        file_name = Editor.get_path_to_save()
        if file_name == None:
            return
        try:
            fileref = open(file=str(file_name), mode="w")
            print("Opened: ",fileref.name)
            fileref.write(text_in_editor)
            fileref.close()
            messagebox.showinfo("Success", "File {} Saved succesfully.".format(file_name))
        except Exception as e:
            messagebox.showerror("Failed", e)

    def exitRoot(self, text_in_editor):
        '''
        exiting procedure
        '''
        inp = messagebox.askyesnocancel("Are you sure?", "Save file before exiting?", parent=self.root)
        if(inp==0):
            self.root.destroy()
        elif(inp==1):
            self.save(text_in_editor)
            self.root.destroy()
        elif(inp==-1):
            return

    def open_file(self):
        '''
        open new file
        '''
        global openedfile, content, open_extensions
        fileref = askopenfile(mode='r', filetypes=open_extensions)
        if openedfile == fileref.name:
            messagebox.showerror("Error", "File is already open in the editor.", parent=self.root)
        else:
            lastopenedfile = openedfile
            openedfile = fileref.name
            content = fileref.read()
            fileref.close()
            fileref = open(openedfile, 'w')
            fileref.write(content)
            fileref.close()
            if(lastopenedfile == "Blank Document"):
                self.root.destroy()
            self.CreateWindow()
    
    
if __name__ == '__main__':
    editor = Editor()