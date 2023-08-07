import tkinter as tk
from tkinter import ttk
import requests
import re
import clipboard

def scrape_emails(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_content = response.text

        # Regular expression pattern to match email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        emails = re.findall(email_pattern, page_content)
        return emails
    except Exception as e:
        print("Error:", e)
        return []

def main():
    root = tk.Tk()
    root.title("Email Scraper")

    width = 400
    height = 400
    
    # Set the geometry of the window
    root.geometry(f"{width}x{height}")
    
    # Create a frame to hold widgets
    frame = ttk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Entry field for URL
    url_label = ttk.Label(frame, text="Enter URL:")
    url_label.pack(padx=10, pady=5)
    
    url_entry = ttk.Entry(frame)
    url_entry.pack(padx=10, pady=5, fill=tk.X)
    
    # Button to start scraping
    scrape_button = ttk.Button(frame, text="Scrape Emails", command=lambda: display_emails())
    scrape_button.pack(padx=10, pady=5)
    
    # Listbox to display scraped emails
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Button to copy emails to clipboard
    copy_button = ttk.Button(frame, text="Copy", command=lambda: copy_emails())
    copy_button.pack(padx=10, pady=5)
    
    def display_emails():
        url = url_entry.get()
        scraped_emails = scrape_emails(url)
        
        listbox.delete(0, tk.END)  # Clear existing list
        
        if scraped_emails:
            for email in scraped_emails:
                listbox.insert(tk.END, email)
        else:
            listbox.insert(tk.END, "No emails found.")
    
    def copy_emails():
        selected_emails = listbox.get(0, tk.END)
        clipboard.copy("\n".join(selected_emails))
    
    root.mainloop()

if __name__ == "__main__":
    main()

