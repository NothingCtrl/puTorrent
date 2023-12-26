# uTorrent Client Tool

Remove completed download torrent if it older than *xx day* (just remove torrent from download list, NOT delete storage). 
To using this tool, you **must** active **Web UI** in uTorrent.

This tool based on api source from this project: https://github.com/LakithaRav/uTorrent-client-python

## Usage

Call with `-h` for help.

* Test mode: call with argument `-t 1` or `--test 1`, in test mode, application just print report, it does not do anything
* The default number of days to remove seeding torrent is **7** days (when call without `-d`)
* These is a feature to request Utorrent **start** the torrent that is _error_ status, to active, call with: `-fe 1` or `--fix-error 1`

### Python

* Remove torrents seeding more than **7 days**: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx"`
* Remove torrents seeding more than **10 days**: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx" -d 10`
* Remove torrents seeding more than **14 days**, and try start torrent in error: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx" -d 14 -fe 1`
* **(Test)** Remove torrents seeding more than **3 days**, try start error torrent: `python main.py -s "http://server:port/gui" -u "admin" -p "passdxxx" -d 3 -fe 1 -t 1`

### Execute file

> Execute file build with `pyinstaller` on Windows 10 OS x64, this may not run in older Windows version (not test)

You can run this tool from pre-compile file in folder *release* without need install _python_ and package dependency.f

Example: `putorrent_win_x64.exe -s "http://server:port/gui" -u "admin" -p "passdxxx"`

### Build commands

```bat
# one file
pyinstaller --onefile main.py
# one file and no console
pyinstaller --onefile --noconsole main.py
```