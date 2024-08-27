# Spotify Translator

Display translated lyrics of the currently playing Spotify track in real-time, extremely simple to use! It is 2024 but for some reason Spotify still doesn't provide a native solution to translate lyrics of non-English songs, so I had to come up with this solution.

## Installation

To get started, install the required Python packages:

```bash
pip3 install syrics
pip install deep-translator
pip install sv-ttk
```

Now download `app.py`. You only need to edit this part in the code (the 12th line):

```python
sp = Spotify("your_sp_dc")
```

Follow the instructions here to find your Spotify `sp_dc` key:   [Finding sp_dc](https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc)

## Usage

Run the app.py, that's it! You should see the GUI application, which will stay open until closed and will show translated lyrics of each song in real-time. Yes it is as simple as running a single .py file, weren't you supposed to clone 5 Github repos and launch 3 Docker containers? 😂

<table>
  <tr>
    <td style="text-align: center;">
      <p>Spotify's Native Lyrics Display</p>
      <img src="https://i.imgur.com/7PoYKzL.png" alt="Native lyrics display of Spotify" style="width: 100%;" />
    </td>
    <td style="text-align: center;">
      <p>Translated Lyrics Display on the App</p>
      <img src="https://i.imgur.com/IY6v5y8.png" alt="The app with translation" style="width: 91%;" />
    </td>
  </tr>
</table>



The program uses the Google Translate API to translate lyrics from any language to English, which often takes 2-3 seconds. It builds a cache of lyrics of the last played 1000 songs to prevent translating the same songs repeatedly. You can change the cache size to any value (or 0 to disable it altogether). The cache will be written/read to the `lyrics_cache.pkl` file.

Video Demo: https://youtu.be/OBQi-sNb3Ss

## Thanks

Thanks to @akashrchandran for his Spotify Lyrics Api which made my app possible: https://github.com/akashrchandran/syrics <br>
And thanks to Melisa [@melisahingl ](https://github.com/melisahingl) for her wonderful Russian music playlist :)

## Contact

You can write to me at atahanuz23@gmail.com for anything at any time.  
However if it is about this program, it will be better if you raise an issue in the repo or submit a PR so everyone can see and contribute to the discussion.
