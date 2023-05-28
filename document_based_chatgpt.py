import tkinter as tk
from tkinter import filedialog
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os

os.environ['OPENAI_API_KEY'] = 'sk-'# Your API key

class MyApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(bg='#f0f0f0')
        self.pack(fill='both', expand=True)
        self.create_widgets()
        
    def create_widgets(self):
        self.title_label = tk.Label(self, text="Document Chatbot", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self.title_label.pack(pady=10)
        
        self.select_dir_button = tk.Button(self, text="Choose Directory", command=self.select_directory, bg='#0c7cd5', fg='white', activebackground='#0a5ca1', activeforeground='white', borderwidth=0, padx=10, pady=5)
        self.select_dir_button.pack(pady=(10,0))
        
        self.selected_dir_label = tk.Label(self, text="", font=('Arial', 12), bg='#f0f0f0')
        self.selected_dir_label.pack(pady=(0,10))
        
        self.query_label = tk.Label(self, text="Query:", font=('Arial', 12), bg='#f0f0f0')
        self.query_label.pack()
        
        self.query_entry = tk.Entry(self, font=('Arial', 12), bd=2)
        self.query_entry.pack(pady=(0,10), ipady=5, ipadx=10)
        
        self.search_button = tk.Button(self, text="Search Documents", command=self.search, bg='#0c7cd5', fg='white', activebackground='#0a5ca1', activeforeground='white', borderwidth=0, padx=10, pady=5)
        self.search_button.pack(pady=(0,10))
        
        self.results_text = tk.Text(self, height=10, font=('Arial', 12), bg='#f5f5f5', fg='#333333', bd=2, padx=10, pady=10)
        self.results_text.tag_configure('highlight', background='#bbeeff')
        self.results_text.pack(fill='both', expand=True, padx=10)
        
    def select_directory(self):
        self.directory = filedialog.askdirectory()
        self.selected_dir_label.configure(text=f"Selected directory: {self.directory}")
        
    def search(self):
        try:
            documents = SimpleDirectoryReader(self.directory).load_data()
        except AttributeError:
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, "Please select a directory first.")
            return
        
        index = GPTSimpleVectorIndex(documents)
        index.save_to_disk('index.json')
       
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        
        query = self.query_entry.get()
        response = index.query(query)
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, response)
        
        if len(response) > 0:
            start = '1.0'
            while True:
                start = self.results_text.search(query, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(query)}c"
                self.results_text.tag_add('highlight', start, end)
                start = end

root = tk.Tk()
 
root.title("Document Chatbot")
root.geometry("500x500")
app = MyApp(root)
app.mainloop()

