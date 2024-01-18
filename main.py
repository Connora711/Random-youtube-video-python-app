import tkinter as tk
from googleapiclient.discovery import build
import webbrowser
from PIL import ImageTk, Image
import io
import requests
import random


# Function to search for youtube videos based on user input
def search_youtube(keyword):
    api_key = "your api key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Call the search.list method to retrieve results
    search_response = youtube.search().list(
        q=keyword,
        part='id, snippet',
        type='video',
        maxResults=3 # Limit the number of results
    ).execute()

    # Get a random video from the search results
    if search_response.get('items'):
        video = random.choice(search_response['items']) # Get a random video from the search results
        video_title = video['snippet']['title']
        video_id = video['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Get the video thumbnail
        thumbnail_url = video['snippet']['thumbnails']['medium']['url']
        thumbnail_data = requests.get(thumbnail_url).content
        thumbnail_image = Image.open(io.BytesIO(thumbnail_data))

        return video_title, video_url, thumbnail_image

    return None


# Function to open the video in a web browser
def open_video(event):
    webbrowser.open(window.video_url)


# Function to handle button click
def button_click():
    keyword = entry.get()
    if keyword:
        result = search_youtube(keyword)
        if result:
            video_title, video_url, thumbnail_image = result

            # Display the video title
            title_label.config(text=video_title)

            # Display the video thumbnail
            thumbnail_image.thumbnail((300, 300))
            thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
            thumbnail_label.config(image=thumbnail_photo)
            thumbnail_label.image = thumbnail_photo

            # Display the link
            link_label.config(text="Watch Video", fg="blue", cursor="hand2")
            link_label.bind("<Button-1>", open_video)

            # Set the video URL in the window object
            window.video_url = video_url
        else:
            title_label.config(text="No video found")
            link_label.config(text="")
    else:
        title_label.config(text="Please enter a keyword")
        link_label.config(text="")


# Create main window
window = tk.Tk()
window.title("YouTube Video Search")

# Initialize video_url attribute
window.video_url = ""

# Create widgets
label = tk.Label(window, text="What type of video are you feeling: ")
label.pack(pady=10)

entry = tk.Entry(window)
entry.pack(pady=10)

button = tk.Button(window, text="Find Video", command=button_click)
button.pack(pady=10)

title_label = tk.Label(window, text="")
title_label.pack(pady=10)

thumbnail_label = tk.Label(window)
thumbnail_label.pack(pady=10)

link_label = tk.Label(window, text="")
link_label.pack(pady=10)

# Start the GUI
window.mainloop()
