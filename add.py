import cv2
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pyzbar.pyzbar import decode
import time

# Function to capture ISBN from camera using OpenCV and pyzbar
def capture_isbn_from_camera():
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    isbn = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            if len(barcode_data) == 13 and barcode_data.isdigit():
                isbn = barcode_data
                break

        if isbn:
            break

        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return isbn

# Function to get book information from OpenLibrary API
def get_book_info_openlibrary(isbn):
    try:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get(url, timeout=10)  # Adding a timeout
        data = response.json()
        book_data = data.get(f"ISBN:{isbn}", {})
        return {
            "ISBN": isbn,
            "Title": book_data.get("title", "No title available"),
            "Author": ", ".join([author["name"] for author in book_data.get("authors", [])]) if "authors" in book_data else "No authors available",
            "Description": book_data.get("notes", "No description available") if "notes" in book_data else "No description available",
            "Availability": "Available",
            "Quantity": 1
        }
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OpenLibrary: {e}")
        return None

# Function to get book information from Google Books API as fallback
def get_book_info_googlebooks(isbn):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url, timeout=10)  # Adding a timeout
        data = response.json()
        if 'items' in data:
            book_data = data['items'][0]['volumeInfo']
            return {
                "ISBN": isbn,
                "Title": book_data.get("title", "No title available"),
                "Author": ", ".join(book_data.get("authors", ["No authors available"])),
                "Description": book_data.get("description", "No description available"),
                "Availability": "Available",
                "Quantity": 1
            }
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Google Books: {e}")
    return {
        "ISBN": isbn,
        "Title": "No title available",
        "Author": "No authors available",
        "Description": "No description available",
        "Availability": "Unavailable",
        "Quantity": 1
    }

# Function to get book information from Wikipedia
def get_book_info_wikipedia(book_title):
    try:
        url = f"https://en.wikipedia.org/wiki/{book_title.replace(' ', '_')}"
        response = requests.get(url, timeout=10)  # Adding a timeout
        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('table', class_='infobox')
        if infobox:
            rows = infobox.find_all('tr')
            book_info = {}
            for row in rows:
                header = row.find('th')
                if header:
                    key = header.get_text().strip()
                    if key == 'Author' or key == 'Authors':
                        value = row.find('td').get_text().strip()
                        book_info[key] = value
                    elif key == 'Description':
                        value = row.find_next_sibling('tr').find('td').get_text().strip()
                        book_info[key] = value
            return {
                "ISBN": None,
                "Title": book_title,
                "Author": book_info.get("Author", "No authors available"),
                "Description": book_info.get("Description", "No description available"),
                "Availability": "Unavailable",
                "Quantity": 1
            }
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Wikipedia: {e}")
    return {
        "ISBN": None,
        "Title": book_title,
        "Author": "No authors available",
        "Description": "No description available",
        "Availability": "Unavailable",
        "Quantity": 1
    }

# Function to get book information from Google Search
def get_book_info_google_search(book_title):
    try:
        query = f"{book_title} book"
        url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)  # Adding a timeout
        soup = BeautifulSoup(response.content, 'html.parser')
        snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd').get_text()
        return {
            "ISBN": None,
            "Title": book_title,
            "Description": snippet,
            "Availability": "Unavailable",
            "Quantity": 1
        }
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Google Search: {e}")
    return {
        "ISBN": None,
        "Title": book_title,
        "Description": "No description available",
        "Availability": "Unavailable",
        "Quantity": 1
    }

# Function to get book information using multiple sources
def get_book_info(isbn, excel_path):
    # First, check if the book exists in the Excel file
    book_info = get_book_info_from_excel(isbn, excel_path)
    if book_info:
        return book_info

    # If not found, fetch book information from external sources
    book_info = get_book_info_openlibrary(isbn)
    if book_info is None or not book_info["Title"] or book_info["Title"] == "No title available" or book_info["Description"] == "No description available":
        print("OpenLibrary did not return sufficient data, trying Google Books API...")
        book_info = get_book_info_googlebooks(isbn)
    if not book_info["Title"] or book_info["Title"] == "No title available" or book_info["Description"] == "No description available":
        print("Google Books API did not return sufficient data, trying Wikipedia...")
        book_info = get_book_info_wikipedia(book_info["Title"])  # Use the title from previous attempt
    if not book_info["Title"] or book_info["Title"] == "No title available" or book_info["Description"] == "No description available":
        print("Wikipedia did not return sufficient data, trying Google search...")
        book_info = get_book_info_google_search(book_info["Title"])  # Use the title from previous attempt

    # Include default values for Category and Location if not available
    if 'Category' not in book_info:
        book_info['Category'] = ""
    if 'Location' not in book_info:
        book_info['Location'] = ""

    return book_info

def get_book_info_from_excel(isbn, excel_path):
    try:
        existing_df = pd.read_excel(excel_path, dtype={'ISBN': str})
        if 'ISBN' in existing_df.columns and isbn in existing_df['ISBN'].values:
            book_info = existing_df.loc[existing_df['ISBN'] == isbn].iloc[0].to_dict()
            book_info['Availability'] = 'Available'  # Ensure availability is set correctly
            return book_info
    except FileNotFoundError:
        pass
    return None

# Function to add book information to an Excel sheet
def add_book_to_excel(book_info, excel_path):
    df = pd.DataFrame([book_info])
    print(f"Data to write to Excel: {df}")
    try:
        existing_df = pd.read_excel(excel_path, dtype={'ISBN': str})
        if 'Quantity' not in existing_df.columns:
            existing_df['Quantity'] = 1
        existing_df['ISBN'] = existing_df['ISBN'].astype(str)
        book_info['ISBN'] = str(book_info['ISBN'])
        if book_info["ISBN"] in existing_df['ISBN'].values:
            print("This book already exists in the database. Incrementing quantity.")
            existing_df.loc[existing_df['ISBN'] == book_info['ISBN'], 'Quantity'] += 1
            existing_df.to_excel(excel_path, index=False)
            return
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        df['Quantity'] = 1  # Initialize quantity column if creating new file
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
    columns_order = ['ISBN', 'Title', 'Author', 'Description', 'Availability', 'Quantity']
    df = df.reindex(columns=columns_order)
    df.to_excel(excel_path, index=False)
    print(f"Data has been written to {excel_path}")

# Main function to add books
def add_books():
    excel_path = 'rasa_bot/actions/Books.xlsx'
    cap = cv2.VideoCapture(0)  # 0 is the default camera

    start_time = time.time()
    isbn = capture_isbn_from_camera()

    if isbn:
        display_start_time = time.time()
        display_duration = 2  # seconds
        
        # Display ISBN Scanned
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            elapsed_time = time.time() - display_start_time
            if elapsed_time < display_duration:
                cv2.putText(frame, f"ISBN Scanned: {isbn}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                display_start_time = time.time()  # Reset for processing display
                break
            
            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Start processing
        processing_start_time = time.time()
        processing_duration = 3  # seconds
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            elapsed_time = time.time() - processing_start_time
            if elapsed_time < processing_duration:
                cv2.putText(frame, "Processing...", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                processing_start_time = time.time()  # Reset for success display
                book_info = get_book_info(isbn, excel_path)
                if book_info:
                    print("Book information retrieved:")
                    for key, value in book_info.items():
                        print(f"{key}: {value}")
                    add_book_to_excel(book_info, excel_path)
                    print(f"Book with ISBN {isbn} has been added to the database.")
                else:
                    print(f"Unable to retrieve information for ISBN {isbn}.")
                break
            
            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Show success message
        success_start_time = time.time()
        success_duration = 2  # seconds
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            elapsed_time = time.time() - success_start_time
            if elapsed_time < success_duration:
                cv2.putText(frame, "Book Added Successfully", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                break
            
            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    add_books()
