
IR Project:

Framework/Language: Python
Install and Download Packages:
1. Create a python environment and install packages from requirements.txt
	Command: pip install -r requirements.txt
2. For the dataset, download from the drive link and place it in the 191-Project-IR-FLARE folder.
	Download and extract the zip such that 'dataset' folder is in 191-Project-IR-FLARE folder, with dataset1 and dataset2 inside it.
	Dataset Link: https://webhose.io/free-datasets/popular-blog-posts/
Running the program:
1. For the GUI:
	Navigate to SearchEngine and run: python ./searchWindow.py
	This pops up a tkinter window which has the search and autocomplete functionalities.
	Since building index for about 20k documents takes time, the window shows not responding sometimes. 
		a. In this case minimize the window, the time taken will be displayed in about 3-5 minutes.
		b. However, the search functionality runs without building the index as well. Since the trie is already stored in trie.txt
	
2. For the CLI:
	Navigate to SearchEngine and uncomment the last few lines of code (mentioned there as well) in query.py
	Now, run: python ./query.py in the SearchEngine folder to use the Command Line Interface for querying.