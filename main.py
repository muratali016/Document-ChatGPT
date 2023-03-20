import PyPDF2
import openai
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import pyperclip
from tkinter.ttk import Progressbar

openai.api_key = "YOUR_API_KEY"


def extract_text(filepath, progress_var):
    # Open the PDF file in read-binary mode
    with open(filepath, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create an empty string to store the text
        text = ''

        # Loop through each page in the PDF file
        for page_num in range(len(pdf_reader.pages)):
            # Update the progress bar
            progress_var.set(page_num + 1)
            root.update_idletasks()
            root.update()

            # Get the page object
            page_obj = pdf_reader.pages[page_num]

            # Extract the text from the page
            page_text = page_obj.extract_text()

            # Add the text to the string
            text += page_text

    return text


def generate_summary(text, status_var):
    status_var.set('Generating summary...')
    words = text.split()
    max_words = 300
    prompt = " ".join(words[:max_words])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize this: {prompt}",
        temperature=0.9,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text
    status_var.set('Summary generated')
    progress_var.set(100)
    return summary


def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath.endswith('.pdf'):
        file_path_var.set(filepath)
        output_text.delete(1.0, tk.END)
    else:
        messagebox.showerror(title='Error', message='Please select a PDF file.')


def clear_output():
    output_text.delete(1.0, tk.END)


def copy_to_clipboard():
    pyperclip.copy(output_text.get(1.0, tk.END))


def save_summary():
    filepath = filedialog.asksaveasfilename(defaultextension='.txt')
    with open(filepath, 'w') as f:
        f.write(output_text.get(1.0, tk.END))


def summarize():
    filepath = file_path_var.get()
    if filepath:
        progress_var.set(0)
        pdf_text = extract_text(filepath, progress_var)
        summary = generate_summary(pdf_text, status_var)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, summary)
    else:
        messagebox.showerror(title='Error', message='Please select a PDF file.')


root = tk.Tk()
root.title('Chatgpt PDF Summarizer ')

# File path label and entry field
file_path_label = tk.Label(root, text='File path:')
file_path_label.pack(pady=10)

file_path_var = tk.StringVar()
file_path_entry = tk.Entry(root, textvariable=file_path_var, width=100)
file_path_entry.pack()

# Browse button
browse_button = tk.Button(root, text='Browse', command=browse_file)
browse_button.pack(pady=10)

# Clear button
clear_button = tk.Button(root, text='Clear', command=clear_output)
clear_button.pack(pady=10)

summarize_button = tk.Button(root, text='Generate Summary', command=summarize)
summarize_button.pack(pady=10)

download_summary_button = tk.Button(root, text='Download Summary', command=save_summary)
download_summary_button.pack(pady=10)

copy_button = tk.Button(root, text='Copy to Clipboard', command=copy_to_clipboard)
copy_button.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = Progressbar(root, variable=progress_var, maximum=50)
progress_bar.pack(pady=10)

status_var = tk.StringVar()
status_var.set('')
status_label = tk.Label(root, textvariable=status_var)
status_label.pack(pady=10)

output_label = tk.Label(root, text='Summary:')
output_label.pack(pady=10)

output_text = tk.Text(root, height=20)
output_text.pack()

root.mainloop()
