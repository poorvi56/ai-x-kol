# AI+X Knots of Love

This project was designed to extract text from yarn label images to determine if they were on the required list for Knots of Love. It used web scraping tools to create a database of all yarns and their sub brands as a reference for FuzzyMatching to output the correct label. It uses KerasOCR and Pytesseract to improve efficiency and accuracy.

## HOWTO
 * Download KerasOCR.
 * Downlaod Pytesseract under pyt folder
 * db is already populated with yarn brands and sub brands, but database.py will scrape https://yarnsub.com/yarns to collect and structure data in txt file.
 * pyt_test.py is the actual system that runs Pytesseract and KerasOCR. Test images can be found in the images folder. Pytesseract will run first, and KerasOCR will be used if Pytesseract fails at reading the label.