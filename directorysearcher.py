import os, subprocess, platform
import tkinter as tk
import time
import concurrent.futures
import threading
from tkinter import filedialog, messagebox, Scrollbar, Listbox
import PyPDF2
import magic
import openpyxl
import docx


class DirectorySearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Searcher")
        self.directory_path = ""
        self.keywords = []
        self.create_main_page()

    def create_main_page(self):
        # Main page layout
        for widget in self.root.winfo_children():
            widget.destroy()
        label = tk.Label(self.root, text="Directory searcher", font=("Arial", 20))
        label.pack(pady=20)

        choose_path_btn = tk.Button(self.root, text="Choose path", command=self.choose_path)
        choose_path_btn.pack(pady=10)

        exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_btn.pack(pady=10)

    def choose_path(self):
        # Prompt user to select directory
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.create_search_page()

    def create_search_page(self):
        # Search page layout
        for widget in self.root.winfo_children():
            widget.destroy()

        self.keywords = []  # Reset keywords list
        
        path_label = tk.Label(self.root, text="Path:", font=("Arial", 12))
        path_label.pack(anchor="w", padx=10)

        path_display = tk.Text(self.root, height=2, wrap="word", font=("Arial", 12))
        path_display.insert(tk.END, self.directory_path)  # Insert the directory path
        path_display.config(state=tk.DISABLED)  # Disable editing
        path_display.pack(fill="x", padx=10, pady=5)

        keyword_label = tk.Label(self.root, text="Keywords:", font=("Arial", 12))
        keyword_label.pack(anchor="w", padx=10)

        # Frame to hold keyword buttons
        self.keyword_frame = tk.Frame(self.root)
        self.keyword_frame.pack(fill="x", padx=10)

        self.keyword_entry = tk.Entry(self.root)
        self.keyword_entry.pack(fill="x", padx=10, pady=5)
        self.keyword_entry.bind("<Return>", self.add_keyword)

        # Main button frame
        row_1_button_frame = tk.Frame(self.root)
        row_1_button_frame.pack(fill="y", padx=10, pady=5)

        # Configure the button frame's grid to center the buttons
        row_1_button_frame.grid_columnconfigure(0, weight=1)
        row_1_button_frame.grid_columnconfigure(1, weight=1)

        

        # Deep search checkbox - Place it next to the Search button
        self.deep_search_var = tk.BooleanVar(value=False)  # Default to unchecked
        deep_search_check = tk.Checkbutton(row_1_button_frame, text="Deep search", variable=self.deep_search_var)
        deep_search_check.grid(row=0, column=0, padx=5, pady=5)  # Align to the left

        self.file_types = ["PDF", "Excel", "Word"]
        self.choosen_file_type_var = tk.StringVar(value=self.file_types[0])
        file_type_dropdown = tk.OptionMenu(row_1_button_frame, self.choosen_file_type_var, *self.file_types)
        file_type_dropdown.grid(row=0, column=1, padx=5, pady=5)

        row_2_button_frame = tk.Frame(self.root)
        row_2_button_frame.pack(fill="y", padx=10, pady=5)
        
        # Search button - Center this frame within the root window
        search_btn = tk.Button(row_2_button_frame, text="Search", command=self.perform_search)
        search_btn.grid(row=0, column=0, padx=5, pady=5)  # Align to the right

        # Other buttons
        clear_btn = tk.Button(row_2_button_frame, text="Clear all", command=self.clear_all_keywords)
        clear_btn.grid(row=1, column=0, padx=5, pady=5)  # Center in the next row

        choose_path_btn = tk.Button(row_2_button_frame, text="Choose path", command=self.choose_path)
        choose_path_btn.grid(row=2, column=0, padx=5, pady=5)  # Center in the next row

        exit_btn = tk.Button(row_2_button_frame, text="Exit", command=self.root.quit)
        exit_btn.grid(row=3, column=0, padx=5, pady=5)  # Center in the next row

    def add_keyword(self, event=None):
        keyword = self.keyword_entry.get().strip()
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)
            self.keyword_entry.delete(0, tk.END)
            self.update_keyword_buttons()

    def update_keyword_buttons(self):
        # Clear current keyword buttons
        for widget in self.keyword_frame.winfo_children():
            widget.destroy()
        # Create a button for each keyword with an "x" to remove it
        for keyword in self.keywords:
            keyword_btn = tk.Button(self.keyword_frame, text=keyword + "  x", command=lambda k=keyword: self.remove_keyword(k))
            keyword_btn.pack(side="left", padx=5, pady=5)

    def remove_keyword(self, keyword):
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.update_keyword_buttons()

    def clear_all_keywords(self):
        self.keywords = []
        self.update_keyword_buttons()

    def perform_search(self):

        if not self.keywords:
            messagebox.showwarning("No Keywords", "Please enter at least one keyword.")
            return
        if not self.directory_path:
            messagebox.showwarning("No Directory", "Please choose a directory.")
            return
        
        time.sleep(0.1)
        self.show_searching_text()
        # Perform the search
        self.search_files(self.directory_path, self.keywords)

    def search_files(self, directory, keywords):
        # Define the file type filter
        allowed_extensions = {".pdf", ".xlsx", ".docx"}  # Set of allowed extensions
        
        choosen_file_type = self.choosen_file_type_var.get().lower()

        if choosen_file_type == "word":
            allowed_extensions = {".docx"}
        elif choosen_file_type == "excel":
            allowed_extensions = {".xlsx"}
        elif choosen_file_type == "pdf":
            allowed_extensions = {".pdf"}
            
        print(f"Choosen file type: {allowed_extensions}")

        # Batch size for loading files in chunks
        batch_size = 1000

        def file_batch_generator(directory, allowed_extensions, batch_size):
            """Generator to yield batches of filtered files."""
            for root, dirs, files in os.walk(directory):
                # Filter out files that don't have the allowed extensions
                filtered_files = [f for f in files if any(f.lower().endswith(ext) for ext in allowed_extensions)]
                #filtered_files = [f for f in files if any(f.lower().endswith(choosen_file_type))]

                # Yield the current batch of files in chunks
                for i in range(0, len(filtered_files), batch_size):
                    yield [os.path.join(root, f) for f in filtered_files[i:i + batch_size]]

        try:
            # Initialize a list to hold the matched files
            matched_files = []

            # Create a generator for batches of files
            file_batches = file_batch_generator(directory, allowed_extensions, batch_size)

            # Iterate over each batch of files
            for batch in file_batches:
                matched_files.extend(batch)

            # Launch a separate thread for the file search, ensuring the GUI remains responsive
            threading.Thread(target=self.run_search_in_thread, args=(matched_files, keywords)).start()

        except Exception as e:
            print(f"Error searching files: {e}")
            return []
    
    def show_searching_text(self):
        self.searching_label = tk.Label(self.root, text="Searching...", font=("Arial", 14))
        self.searching_label.pack(pady=10)

    def hide_searching_text(self):
        if hasattr(self, "searching_label"):
            self.searching_label.pack_forget()

    def no_results_found(self):
        if hasattr(self, "searching_label"):
            self.searching_label.pack_forget()

        messagebox.showinfo("No Results", "No results found. Please try again.")
    
    def run_search_in_thread(self, file_paths, keywords):
        """
        Function to start searches in parallel using multithreading.
        """

        # Use ThreadPoolExecutor to process files in parallel, avoiding multiprocessing for GUI issues
        matched_files = []
        must_have_keys = []

        for i, key in enumerate(keywords):
            if key[-1] == "!":
                keywords[i] = key[:-1]
                must_have_keys.append(key)

        if len(must_have_keys) > 1:
            keywords = [key for key in keywords if key not in must_have_keys]
            #print(f"keywords: {keywords}\nsuggestive_keys: {must_have_keys}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            
            results = executor.map(self.process_file, zip(file_paths, [keywords]*len(file_paths), [must_have_keys]*len(file_paths)))
            for result in results:
                if result:
                    matched_files.append(result)

        if len(matched_files) < 1:
            self.root.after(500, self.no_results_found)  # No results found, return to search page
            self.root.after(500, self.create_search_page)  # No results found, return to search page
        else:
            # Once search is done, update the UI on the main thread
            self.root.after(500, self.hide_searching_text)
            self.root.after(1000, self.create_result_page, matched_files)

    def read_pdf(self, file_path):
        """
        Retrives PDF content page by page.
        """

        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                pdf_text = []

                for page in reader.pages:
                    pdf_text.append(page.extract_text())
                    return pdf_text
        except Exception as e:
            return file_path, f"Error while reading PDF content.\nBecause: {e}"
    
    def read_excel(self, file_path):
        """
        Retrives Excel content row by row
        """
        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet_content = []

            for sheet in workbook.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    sheet_content.append(row)
            return sheet_content
        except Exception as e:
            return file_path, f"Error while reading Excel content.\nBecause: {e}"
        
    def read_word(self, file_path):
        """
        Retrives content from word documents paragraph by paragraph
        """
        doc = docx.Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)

        
    def check_file_type(self, file_path):
        """
        Uses python-magic the check and return file type
        """
        file_magic = magic.Magic()
        file_type = file_magic.from_file(file_path)

        #print(f"Filetype is: {file_type}")

        return file_type


    def process_file(self, args):
        """
        Function to process each file and check if the keywords match.
        This function is designed to run in parallel using multiprocessing.
        """
        #file_path, keywords, suggestive_keys = zip(*args)
        file_path = args[0]
        keywords = args[1]
        must_have_keys = args[2]

        def must_contain_keywords(target, must_have_keys):
            """Check if all keywords are present in the target string."""
            return all(keyword.lower() in target.lower() for keyword in must_have_keys)
        
        def can_contain_keywords(target, keywords):
            """Check if any suggestive key is present in the target string (optional)."""
            return any(s_key.lower() in target.lower() for s_key in keywords)
        
        try:
            file_name = os.path.basename(file_path)

            if len(must_have_keys) > 0:

                if can_contain_keywords(file_path, keywords) or must_have_keys(file_path, must_have_keys):
                    #print(f"Added: {file_name} to results")
                    return file_path
                elif can_contain_keywords(file_name, keywords) or must_have_keys(file_name, must_have_keys):
                    #print(f"Added: {file_name} to results")
                    return file_path                
                elif self.deep_search_var.get():

                    file_type = self.check_file_type(file_path)

                    if "pdf" in file_type.lower():
                        content = self.read_pdf(file_path)

                        for page in content:
                            if can_contain_keywords(page, keywords) or must_contain_keywords(page, must_have_keys):
                                ##print(f"Added: {file_name} to results")
                                return file_path
                            
                    elif "excel" in file_type.lower():
                        content = self.read_excel(file_path)

                        for sheet in content:
                            if can_contain_keywords(sheet, keywords) or must_contain_keywords(sheet, must_have_keys):
                                #print(f"Added: {file_name} to results")
                                return file_path
                            
                    elif "word" in file_type.lower():
                        content = self.read_word(file_path)

                        for paragraph in content:
                            if can_contain_keywords(paragraph, keywords) or must_contain_keywords(paragraph, must_have_keys):
                                #print(f"Added: {file_name} to results")
                                return file_path
                            
                    else:
                        print(f"Filetype is not supported {file_name}")

            else:
                if can_contain_keywords(file_name, keywords):
                    #print(f"Added: {file_name} to results")
                    return file_path
                elif can_contain_keywords(file_path, keywords):
                    #print(f"Added: {file_name} to results")
                    return file_path
                elif self.deep_search_var.get():
                    #if self.check_file_type_1(file_path) == "application/pdf":
                    file_type = self.check_file_type(file_path)

                    if "pdf" in file_type.lower():
                        #content = self.read_pdf_1(file_path)
                        content = self.read_pdf(file_path)

                        for page in content:
                            if can_contain_keywords(page, keywords):
                                #print(f"Added: {file_name} to results")
                                return file_path

                    elif "excel" in file_type.lower():
                        content = self.read_excel(file_path)

                        for sheet in content:
                            if can_contain_keywords(sheet, keywords):
                                #print(f"Added: {file_name} to results")
                                return file_path
                    
                    elif "word" in file_type.lower():
                        content = self.read_word(file_path)

                        for paragraph in content:
                            if can_contain_keywords(paragraph, keywords):
                                #print(f"Added: {file_name} to results")
                                return file_path
                    else:
                        print(f"Filetype is not supported {file_name}")
                            
            return None
        
        except Exception as e:
            print(f"Error reading file {file_path}\nBecause: {e}")
            return None

    def create_result_page(self, results):
    # Result page layout
        for widget in self.root.winfo_children():
            widget.destroy()

        result_label = tk.Label(self.root, text="Results:", font=("Arial", 12))
        result_label.pack(anchor="w", padx=10)

        # Create a Text widget to display the results with word wrapping
        result_text = tk.Text(self.root, wrap="word", height=10)
        result_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Add a scrollbar to the Text widget
        scrollbar = Scrollbar(result_text)
        result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=result_text.yview)
        scrollbar.pack(side="right", fill="y")

        if results is not None:
            # Insert the results into the Text widget
            for result in results:
                result_text.insert(tk.END, result + "\n\n")  # Add each result on a new line

        # Disable editing the Text widget
        result_text.config(state=tk.DISABLED)

        result_text.bind("<ButtonRelease-1>", lambda event: self.on_text_click(result_text, event))

        # Retry button
        retry_btn = tk.Button(self.root, text="Retry", command=self.create_search_page)
        retry_btn.pack(pady=5)

        # Choose path button
        choose_path_btn = tk.Button(self.root, text="Choose path", command=self.choose_path)
        choose_path_btn.pack(pady=5)

        # Exit button
        exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_btn.pack(pady=5)


    def on_text_click(self, text_widget, event):
        """
        Retrieves the file_path based on where the user has clicked.
        """
        try:
            index = text_widget.index(f"@{event.x},{event.y}")
            file_path = text_widget.get(f"{index.split('.')[0]}.0", f"{index.split('.')[0]}.end").strip().replace("/", "\\")

            self.open_file(file_path)
        except Exception as e:
            return file_path, f"Error when finding path"

    def open_file(self, file_path):
        """
        Opens file at the given path
        """

        try:
            if platform.system() == "Windows":
                #print(f"Trying to open file at path: {file_path}")
                os.startfile(file_path)
            elif platform.system() == 'Darwin':
                subprocess.call(('open', file_path))
            elif platform.system == 'Linux':
                subprocess.call(('xdg-open', file_path))
            else:
                print(f"Error, system platform is not supported.\nCurrent system platform: {platform.system()}")
            
        except Exception as e:
            return file_path, f"Error while trying to open file on given path"

# Main execution
root = tk.Tk()
app = DirectorySearcherApp(root)
root.geometry("500x400")
root.mainloop()