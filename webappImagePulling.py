import tkinter as tk
from tkinter import messagebox
import requests


# NASA API base URL
API_BASE_URL = 'http://images-api.nasa.gov/'

# Function to handle the search button click event
def search():
    query = search_entry.get()
    if query:
        search_images(query)
    else:
        messagebox.showinfo('Error', 'Please enter a search query')

# Function to fetch and display the search results
def search_images(query):
    url = f'{API_BASE_URL}search?q={query}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data['collection']['items']
        display_results(items)
    else:
        messagebox.showinfo('Error', 'An error occurred while fetching the search results')

# Function to display the search results
def display_results(items):
    result_list.delete(0, tk.END)
    for item in items:
        data = item['data'][0]
        title = data['title']
        image_url = data['media_type']
        result_list.insert(tk.END, title)
    result_list.bind('<<ListboxSelect>>', show_details)

# Function to fetch and display the details of a selected item
def show_details(event):
    selection = result_list.curselection()
    if selection:
        index = selection[0]
        item = result_list.get(index)
        query = search_entry.get()
        url = f'{API_BASE_URL}search?q={query}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data['collection']['items']
            details = items[index]['data'][0]
            messagebox.showinfo('Details', f'Title: {details["title"]}\nDescription: {details["description"]}\nDate: {details["date_created"]}')
        else:
            messagebox.showinfo('Error', 'An error occurred while fetching the item details')

# Create the main application window
root = tk.Tk()
root.title('NASA Image Search')

# Create search bar
search_entry = tk.Entry(root)
search_entry.pack(pady=10)

# Create search button
search_button = tk.Button(root, text='Search', command=search)
search_button.pack()

# Create result listbox
result_list = tk.Listbox(root, width=50, height=10)
result_list.pack(pady=10)

# Run the main application loop
root.mainloop()