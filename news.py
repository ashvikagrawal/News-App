import requests
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# Replace with your API key
API_KEY = "440e264ae142438cbea8ecb0b63c7173"
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Function to fetch news
def get_news(category, country="us"):
    params = {
        "apiKey": API_KEY,
        "category": category,
        "country": country,
        "pageSize": 5,  # Fetch top 5 news articles
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        messagebox.showerror("Error", "Failed to fetch news!")
        return []

# Function to display news
def display_news():
    category = category_var.get()
    articles = get_news(category)
    
    news_list.delete(*news_list.get_children())  # Clear previous entries
    for article in articles:
        news_list.insert("", "end", values=(article['title'], article['source']['name'], article['url']))

# Function to open article URL
def open_url(event):
    selected_item = news_list.selection()
    if selected_item:
        url = news_list.item(selected_item[0])['values'][2]
        webbrowser.open(url)

# Creating GUI window
root = tk.Tk()
root.title("Personalized News Aggregator")
root.geometry("700x400")

# Dropdown for category selection
category_var = tk.StringVar()
categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
ttk.Label(root, text="Select Category:").pack(pady=5)
category_menu = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly")
category_menu.pack(pady=5)
category_menu.current(0)

# Button to fetch news
ttk.Button(root, text="Get News", command=display_news).pack(pady=10)

# Table to display news
columns = ("Title", "Source", "URL")
news_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    news_list.heading(col, text=col)
    news_list.column(col, width=200)
news_list.pack(fill="both", expand=True)
news_list.bind("<Double-1>", open_url)  # Double-click to open URL

root.mainloop()