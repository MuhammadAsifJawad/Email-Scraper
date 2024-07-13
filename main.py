import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import re
import clipboard
import csv
import json
import pandas as pd
import xml.etree.ElementTree as ET

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

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

def export_emails(emails, export_format):
    if not emails:
        messagebox.showerror("Export Error", "No emails to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=f".{export_format}", filetypes=[(export_format.upper(), f"*.{export_format}")])
    if not file_path:
        return

    try:
        if export_format == "csv":
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Email"])
                for email in emails:
                    writer.writerow([email])
        elif export_format == "json":
            with open(file_path, mode='w') as file:
                json.dump(emails, file)
        elif export_format == "xls":
            df = pd.DataFrame(emails, columns=["Email"])
            df.to_excel(file_path, index=False)
        elif export_format == "xml":
            root = ET.Element("emails")
            for email in emails:
                email_elem = ET.SubElement(root, "email")
                email_elem.text = email
            tree = ET.ElementTree(root)
            tree.write(file_path)
        messagebox.showinfo("Export Successful", f"Emails successfully exported as {export_format.upper()}.")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export emails: {e}")

def main():
    root = tk.Tk()
    root.title("Email Scraper")

    # Set the geometry of the window
    root.geometry("400x500")

    # Create a frame to hold widgets
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Title Label
    title_label = ttk.Label(frame, text="Email Scraper", font=("Helvetica", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Entry field for URL
    url_label = ttk.Label(frame, text="Enter URL:")
    url_label.grid(row=1, column=0, sticky=tk.W, pady=5)

    url_entry = ttk.Entry(frame, width=40)
    url_entry.grid(row=1, column=1, pady=5, padx=5)

    # Button to start scraping
    scrape_button = ttk.Button(frame, text="Scrape Emails", command=lambda: handle_scraping())
    scrape_button.grid(row=2, column=0, columnspan=2, pady=5)

    # Button to load URLs from CSV
    load_csv_button = ttk.Button(frame, text="Load URLs from CSV", command=lambda: handle_scraping(csv=True))
    load_csv_button.grid(row=3, column=0, columnspan=2, pady=5)

    # Listbox to display scraped emails
    listbox_label = ttk.Label(frame, text="Scraped Emails:")
    listbox_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

    listbox = tk.Listbox(frame, height=10, width=50)
    listbox.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Scrollbar for listbox
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))

    # Button to copy emails to clipboard
    copy_button = ttk.Button(frame, text="Copy Emails", command=lambda: copy_emails())
    copy_button.grid(row=6, column=0, pady=5, sticky=tk.W)

    # Dropdown menu for export format
    export_label = ttk.Label(frame, text="Select export format:")
    export_label.grid(row=7, column=0, sticky=tk.W, pady=5)

    export_format = tk.StringVar()
    export_format.set("csv")
    export_menu = ttk.Combobox(frame, textvariable=export_format, values=["csv", "json", "xls", "xml"])
    export_menu.grid(row=7, column=1, pady=5, padx=5)

    # Button to export emails
    export_button = ttk.Button(frame, text="Export Emails", command=lambda: export_emails(listbox.get(0, tk.END), export_format.get()))
    export_button.grid(row=8, column=0, columnspan=2, pady=5)

    def handle_scraping(csv=False):
        if csv:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            urls = read_csv(file_path)
            all_emails = []
            for url in urls:
                all_emails.extend(scrape_emails(url))
            display_emails(all_emails)
        else:
            url = url_entry.get()
            if not url:
                messagebox.showerror("Input Error", "Please enter a URL or load a CSV file.")
                return

            scraped_emails = scrape_emails(url)
            display_emails(scraped_emails)

    def display_emails(emails):
        listbox.delete(0, tk.END)  # Clear existing list

        if emails:
            for email in emails:
                listbox.insert(tk.END, email)
        else:
            listbox.insert(tk.END, "No emails found.")

    def copy_emails():
        selected_emails = listbox.get(0, tk.END)
        clipboard.copy("\n".join(selected_emails))

    root.mainloop()

if __name__ == "__main__":
    main()
