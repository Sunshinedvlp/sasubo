import PyInstaller.__main__


PyInstaller.__main__.run([
    'app.py',
    '--icon=icon.ico',
    '--onefile',
], )
