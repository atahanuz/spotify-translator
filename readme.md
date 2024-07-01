# spotify-translator

Display translated lyrics of the currently playing Spotify track in real time, extremely simple to use! It is 2024 but Spotify still doesn't provide a native solution to translate lyrics of the non-English songs so I had to come with this solution.

## Installation

To get started, install the required Python packages:

```bash
pip3 install syrics
pip install deep-translator
pip install sv-ttk
```


Now download app.py.
You only need to edit this part
```python
sp = Spotify("your_sp_dc")
```
Follow the instructions here to find your Spotfiy sp_dc key <br>
https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc

## Usage
<div style="display: flex; justify-content: space-between;">
    <img src="https://i.imgur.com/7PoYKzL.png" alt="Native lyrics display of Spotify" style="width: 40%;" />
    <img src="https://i.imgur.com/IY6v5y8.png" alt="App with translation" style="width: 40%;" />
</div>



That's it, run the application. You should see the GUI application which will stay open until closed and will show translated lyrics of each song in real time.

The program uses Google Translate API to translate lyrics from any language to English, it often takes 2-3 seconds. It builds a cache of lyrics of the last played 1000 songs to prevent translating the same songs over and over. You can change the cache size to any value (or 0 to disable it altogether). The cache will be written/read to lyrics_cache.pkl file.


