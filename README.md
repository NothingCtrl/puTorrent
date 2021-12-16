# uTorrent Client Tool

Remove completed download torrent if it older than *xx day* (just remove torrent from download list, NOT delete storage). 
To using this tool, you **must** active **Web UI** in uTorrent.

This tool based on api source from this project: https://github.com/LakithaRav/uTorrent-client-python

## Usage

### Python

* Remove completed torrent older than **7 days**: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx"`
* Remove completed torrent older than **10 days**: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx" -d 10`
* **Test** mode (not remove) completed torrent older than **3 days**: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx" -d 3 -t 1`

### Execute file

> Execute file build with `pyinstaller` on Windows 10 OS x64, this may not run in older Windows version (not test)

You can run this tool from pre-complite file in folder *release*, file name: `putorrent_win_x64.exe`

Example: `putorrent_win_x64.exe -s "http://server:port/gui" -u "admin" -p "passdxxx"`