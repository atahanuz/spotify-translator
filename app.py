import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
from syrics.api import Spotify
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import pickle
import os
import sv_ttk

# Initialize Spotify API
sp = Spotify("your_sp_dc")

# Cache to store the translated lyrics
CACHE_FILE = 'lyrics_cache.pkl'
MAX_CACHE_SIZE = 1000


current_song_id = None
translation_complete = False
translated_lyrics_cache = None
language=""
# Load cache from file if it exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        lyrics_cache = pickle.load(f)
else:
    lyrics_cache = {}

# Function to save cache to file
def save_cache():
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(lyrics_cache, f)

# Function to get the current song and playback position
def get_current_playback_position():
    try:
        current_song = sp.get_current_song()
        position_ms = current_song['progress_ms']
        return current_song, position_ms
    except Exception as e:
        print(f"Error fetching current song playback position: {e}")
        return None, 0

# Function to update the Treeview and the current time label
def update_display():
    global current_song_id
    current_song, current_position = get_current_playback_position()
    if current_song:
        song_id = current_song['item']['id']
        if song_id != current_song_id:
            current_song_id = song_id
            update_lyrics()

        current_time_label.config(text=f"Current Time: {ms_to_min_sec(current_position)}")
        last_index = None
        for item in tree.get_children():
            item_data = tree.item(item)
            start_time = int(item_data['values'][0].split(":")[0]) * 60000 + int(item_data['values'][0].split(":")[1]) * 1000
            if start_time <= current_position:
                last_index = item
            else:
                break
        if last_index:
            tree.selection_set(last_index)
            tree.see(last_index)

    root.after(500, update_display)  # Reduced the update frequency

# Function to convert milliseconds to minutes:seconds format
def ms_to_min_sec(ms):
    ms = int(ms)
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02}"

# Function to translate a single lyric line
def translate_line(translator, line):
    original_text = line['words']
    try:
        translated_text = translator.translate(original_text)
    except Exception as e:
        print(f"Error translating '{original_text}': {e}")
        translated_text = original_text
    return {'startTimeMs': line['startTimeMs'], 'words': original_text, 'translated': translated_text}

# Function to translate lyrics using multithreading
def translate_words(lyrics, song_name, song_id, callback):
    global translation_complete, translated_lyrics_cache
    translator = GoogleTranslator(source='auto', target='en')
    translated_song_name = translator.translate(song_name)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(translate_line, translator, line) for line in lyrics]
        translated_lyrics = [future.result() for future in as_completed(futures)]
    lyrics_cache[song_id] = translated_lyrics  # Store the result in the cache

    # Ensure the cache size does not exceed the limit
    if len(lyrics_cache) > MAX_CACHE_SIZE:
        lyrics_cache.pop(next(iter(lyrics_cache)))

    save_cache()
    callback(translated_lyrics)
    translation_complete = True

# Function to update the lyrics in the Treeview
def update_lyrics():
    global current_song_id, translation_complete

    current_song = sp.get_current_song()
    song_id = current_song['item']['id']
    song_name = current_song['item']['name']
    lyrics = sp.get_lyrics(song_id)
    lyrics_data = lyrics['lyrics']['lines'] if lyrics and 'lyrics' in lyrics and 'lines' in lyrics['lyrics'] else None

    root.title(f"{song_name}")

    tree.delete(*tree.get_children())

    if lyrics_data:
        # Detect the language of the first line of lyrics
        detected_lang= lyrics['lyrics']['language']
        global language
        language=detected_lang
        tree.heading("Original Lyrics", text=f"Original Lyrics ({detected_lang})")

        for index, lyric in enumerate(lyrics_data):
            tree.insert("", "end", values=(ms_to_min_sec(lyric['startTimeMs']), lyric['words'], ""))
        translation_complete = False
        if song_id in lyrics_cache:
            update_translations(lyrics_cache[song_id])
        else:
            threading.Thread(target=translate_words, args=(lyrics_data, song_name, song_id, update_translations)).start()
    else:
        tree.insert("", "end", values=("0:00", "(No lyrics)", ""))
    adjust_column_widths()

# Function to update the Treeview with translated lyrics
def update_translations(translated_lyrics):
    for item in tree.get_children():
        item_data = tree.item(item)
        start_time = item_data['values'][0]
        original_lyrics = item_data['values'][1]
        for lyric in translated_lyrics:
            if ms_to_min_sec(lyric['startTimeMs']) == start_time and lyric['words'] == original_lyrics:
                tree.set(item, column="Translated Lyrics", value=lyric['translated'])
                break
    if tree.get_children():
        first_item = tree.get_children()[0]
        tree.set(first_item, column="Translated Lyrics", value=translated_lyrics[0]['translated'])
    adjust_column_widths()

# Function to find the longest line length in original and translated lyrics
def find_longest_line_lengths():
    max_original_length = 0
    max_translated_length = 0
    line_count = 0

    for item in tree.get_children():
        line_count += 1
        original_length = len(tree.item(item)['values'][1])
        translated_length = len(tree.item(item)['values'][2])
        if original_length > max_original_length:
            max_original_length = original_length
        if translated_length > max_translated_length:
            max_translated_length = translated_length

    return max_original_length, max_translated_length, line_count

# Function to adjust the column widths based on the content
def adjust_column_widths():
    min_time_width = 60  # Minimum width for the "Time" column
    max_original_length, max_translated_length, line_count = find_longest_line_lengths()

    root.update_idletasks()
    width = tree.winfo_reqwidth()

    orig_length=max_original_length*15
    trans_length = max_translated_length * 15

    if language=="ja":
        orig_length=max_original_length*23
    if language=="ru":
        orig_length=max_original_length*18
        trans_length=max_translated_length*19







    width = min_time_width + orig_length + trans_length

    # Get the required height for the treeview
    tree_height = tree.winfo_reqheight()

    # Add the height of the current time label and some padding
    height = line_count * 17 + 100

    #print(f"Width: {width}, Height: {height}")
    #print(f"Max Original Length: {max_original_length}, Max Translated Length: {max_translated_length}")

    # Update the window size
    # get current width
    current_width = root.winfo_width()

    tree.column("Time", width=min_time_width, minwidth=min_time_width)
    tree.column("Original Lyrics", width=orig_length)
    tree.column("Translated Lyrics", width=trans_length)
    root.geometry(f"{current_width}x{height}")

# Create main application window

root = tk.Tk()

root.title("Spotify Lyrics Translator")

# Apply a theme to the Tkinter application
style = ttk.Style(root)
style.theme_use("default")  # Use a base theme that can be customized

# Customize Treeview styles with green theme
style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background='#4CAF50', foreground='white')
style.configure("Treeview", font=('Arial', 14), rowheight=40, background='#E8F5E9', foreground='black', fieldbackground='#E8F5E9')
sv_ttk.set_theme("dark")
style.configure("Treeview",rowheight=25)

style.map('Treeview', background=[('selected', '#81C784')], foreground=[('selected', 'white')])

# Force update of the Treeview style
root.update_idletasks()

# Current time label
current_time_label = tk.Label(root, text="Current Time: 00:00", font=('Helvetica', 12, 'bold'), bg='#388E3C', fg='#fff', padx=10, pady=5)
current_time_label.pack(side=tk.TOP, fill=tk.X)

# Create a frame to hold the Treeview and Scrollbar
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)

# Create and pack the treeview widget
style.configure("Treeview.Heading", foreground="lightgreen", font=('Helvetica', 14, 'bold'))

tree = ttk.Treeview(frame, columns=("Time", "Original Lyrics", "Translated Lyrics"), show="headings", style="Treeview")
tree.heading("Time", text="  Time", anchor='w')
tree.heading(f"Original Lyrics", text=f"  Original Lyrics", anchor='w')
tree.heading("Translated Lyrics", text="  Translated Lyrics", anchor='w')
tree.column("Time", width=200, minwidth=200, anchor='w')
tree.column(f"Original Lyrics", width=250, anchor='w')
tree.column("Translated Lyrics", width=250, anchor='w')

# Update the column heading style to green
tree.tag_configure('heading', foreground='#4CAF50')

# Create the Scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side='left', fill=tk.BOTH, expand=True)
scrollbar.pack(side='right', fill='y')

# Start the update in a non-blocking manner
root.after(500, update_display)  # Initial call to start the loop with reduced frequency

# Start the application

root.mainloop()
