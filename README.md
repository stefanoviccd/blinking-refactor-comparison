# Blinking-refactor-comparison method

🔷 Purpose of the method is to compare two files with same structure and to show if they match. If files are identical, we get the message and if they not, all the differences will be displayed in the result file.

🔷 Required inputs:

1️⃣ --dev_file_path : absolute path to our first file, whitch we want to compare.
2️⃣ --new_file_path : absolute path to the second file for comparison
3️⃣ --keys : key values we expect our objects to contain. Thoose are parts of the document readed (e.g. front data, back data, mrz data)
4️⃣ --result_file_path : absolute path to the document where we want to write our result. Document can exist, but if not, it will be created on the path and with name specified.


🔷 Method output: As the result of the method, we get .txt file on the path specified as --result_file_path parameter, whitch displays all the differences between first file, whitch path is specified as --dev_file_path parameter and the second one, on --new_file_path.

🔷 Method call: We can execute method through command prompt, by typhing: 
  python SCRIPT_NAME.py **//--dev_file_path** PATH_TO_FIRST_FILE **--new_file_path** PATH_TO_SECOND_FILE **--keys** 'first key name' 'secont key name' .. 'nth key     name' **--result_file_path** PATH_TO_RESULT_FILE
  
  File paths need to be passed without quotation marks. For --keys parameter, every key is passed with single quotation marks and keys are separated with one blank   space. Key names must be lowercase.
  
  ‼️ NOTE: Statistics from the end of both dev and new file should be removed before processing files with method.
  

