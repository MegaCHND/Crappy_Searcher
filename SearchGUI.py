from tkinter import *
from tkinter import messagebox
import sys
import Searcher

class SearchWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.search_terms = StringVar()
        self.num_results = StringVar()
        self.initUI()

    def initUI(self):
        self.parent.title("Search Engine")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)
        
        query_label = Label(frame1, text="Query:", width=10)
        query_label.pack(side=LEFT, padx=5, pady=5)

        search_textbox = Entry(frame1, textvariable=self.search_terms)
        search_textbox.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)
        
        num_results_label = Label(frame2, text="# of Results:", width=10)
        num_results_label.pack(side=LEFT, padx=5, pady=5)

        num_results_textbox = Entry(frame2, textvariable=self.num_results)
        num_results_textbox.pack(fill=X, padx=5, expand=True)
        num_results_textbox.insert(0, "1")

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)
        
        quit_button = Button(frame3, text="Quit", command=self.parent.destroy)
        quit_button.pack(side=LEFT, padx=5, pady=5)
        
        search_button = Button(frame3, text="Search", command=self.search)
        search_button.pack(side=RIGHT, padx=5, pady=5)

    def search(self):
        try:
            global data
            search_terms = self.search_terms.get().lower()
            num_results = int(self.num_results.get())
            results = Searcher.get_results(search_terms, num_results)
            if len(results) == 0:
                messagebox.showerror("Error","No results found. Please search again.")
            else:
                self.createResultsWindow(results)
        except:
            print(sys.exc_info())
            messagebox.showerror("Error","Please enter a valid number of results to show.")            
    def createResultsWindow(self, results):
        try:
            resultWindow = Toplevel()
            resultWindow.title("Search Results")
            frame = Frame(resultWindow, bd=0, relief=SUNKEN)

            scrollbar = Scrollbar(frame, orient=VERTICAL)
            scrollbar.pack(side=RIGHT, fill=Y)

            max_length = 10
            for result in results:
                if len(result) > max_length:
                    max_length = len(result)
            listbox = Listbox(frame, bd=0, width=max_length)
            listbox.pack(side=LEFT, fill=BOTH, expand=1)
            
            for result in results:
                listbox.insert(END, result)

            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)
            
            frame.pack()

            frame2 = Frame(resultWindow, bd=0)

            exit_button = Button(frame2, text="Quit", command=resultWindow.destroy)
            exit_button.pack(padx=5, pady=5)

            frame2.pack()
            resultWindow.geometry("")
        except:
            print(sys.exc_info())

root = Tk()
root.geometry("300x100+300+300")
app = SearchWindow(root)
root.mainloop()