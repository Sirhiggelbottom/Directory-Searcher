# *Directory Searcher*

*Directory Searcher is a Python application built using the Tkinter library. It allows users to search for files within a selected directory based on specified keywords. The application supports both shallow and deep search modes and has the option to both open files and add results to an archive.*

## *Features*

* ***Directory Selection** : Users can select a directory to search within.*
* ***Keyword Search** : Users can add multiple keywords to search for files.*
* ***Keyword Matching:** By enclosing a keyword like this "keyword", each result must contain that keyword in one way or another*
* ***Keyword Exclusion:** By starting a keyword like this !keyword, results containing that keyword will be ignored*
* ***Deep Search** : Option to search within file contents, off by default.*
* ***Batch Processing** : Files are processed in batches to improve performance.*
* ***Multithreading** : Uses multithreading to speed up file search.*
* ***Archive Results** : Saves the results to an archive at a chosen path.*

## *Limitations*

* ***File Amount** : Directories with more than 10,000 files will increase the processing time.*

## *Requirements*

* *Python 3.x*
* *Tkinter (usually included with Python installations)*
* *PyPDF2*
* *python-magic*
* *openpyxl*
* *python-docx*
* *zipfile*
* *rarfile*
* *py7zr*
* *tarfile*

## *Installation*

1. *Clone the repository*
2. *Ensure you have Python 3.x and the required packages installed on your machine.*

## *Usage*

1. *Run the script using Python while in the same directory:*

   ```powershell

   python directorysearcher.py

   ```
2. *Or run it in the Code Editor with Python*
3. *The application window will open.*

### *Main Page*

* ***Choose Path** : Click to select the directory you want to search in.*
* ***Exit** : Click to exit the application.*

### *Search Page*

* ***Path** : Displays the selected directory path.*
* ***Keywords** : Enter keywords to search for files. Press Enter to add the keyword.*
* ***Search** : Click to start the search.*
* ***Deep Search** : Check this option to search within file contents.*
* ***Clear All** : Click to clear all added keywords.*
* ***Choose Path** : Click to select a different directory.*
* ***Exit** : Click to exit the application.*

### *Results Page*

* ***Save to archive** : If the search returned any results, you can save these files to an archive.*
* ***Results** : Displays the search results. Open file by clicking on the path.*
* ***Retry** : Click to perform a new search, this clears any keyword.*
* ***Choose Path** : Click to select a different directory, this clears any keyword.*
* ***Exit** : Click to exit the application.*

## *How It Works*

1. ***Directory Selection** : The user selects a directory using the file dialog.*
2. ***Keyword Entry** : The user enters keywords to search for files.*
3. ***Search Execution** : The application searches for files that match the keywords in the selected directory. If "Deep Search" is enabled, it also searches within the file contents.*
4. ***Results Display** : The results are displayed as absolute paths. Files can be opened by clicking on their path*

## *Code Overview*

 ***DirectorySearcherApp** : Main application class.*

* *[`__init__`]: Initializes the application.*
* *[`create_main_page`]: Creates the main page layout.*
* *[`choose_path`]: Prompts the user to select a directory.*
* *[`create_search_page`]: Creates the search page layout.*
* *[`add_keyword`]: Adds a keyword to the search list.*
* *[`update_keyword_buttons`]: Updates the keyword buttons.*
* *[`remove_keyword`]: Removes a keyword from the search list.*
* *[`clear_all_keywords`]: Clears all keywords.*
* *[`get_chosen_file_type`]: Returns a set containing the chosen file types*
* *[`perform_search`]: Initiates the search process.*
* *[`search_files`]: Searches for files in the selected directory.*
* *[`show_searching_text`]: Displays a "Searching..." message.*
* *[`hide_searching_text`]: Hides the "Searching..." message.*
* *[`no_results_found`]: Displays a "No Results" message.*
* *[`run_search_in_thread`]: Runs the search in separate threads.*
* *[`read_pdf`]: Retrieves PDF content page by page.*
* *[`read_excel`]: Retrieves Excel content row by row*
* *[`read_word`]: Retrieves content from word documents paragraph by paragraph*
* *[`read_zipfile`]: Returns list of filenames from zip archive*
* *[`read_rarfile`]: Returns list of filenames from rar archive*
* *[`read_7zfile`]: Returns list of filenames from 7z archive*
* *[`read_tarfile`]: Returns list of filenames from tar archive*
* *[`check_file_type`]: Uses python-magic to check and return file type*
* *[`process_file`]: Processes each file to check for keyword matches.*
* *[`create_result_page`]: Creates the results page layout.*
* *[`on_text_click`]: Retrieves the file_path based on where the user has clicked.*
* *[`open_file`]: Opens file at the given path*
* *[`add_directories_to_archive`]: Saves the directories and or files from the results to an archive at a chosen path*

## *License*

*This project is licensed under the [MIT License](LICENSE)*
