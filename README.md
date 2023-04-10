It's a commandline utility to help automate SSH tasks, based on Fabric in Python.
I build this because plink.exe from PuTTY don't have everything that I need.
It's only tested on Python 3.10.

# use
```PowerShell
# install its requirements
pip install fabric argparse
# run a script with password stored in clear text. What a security disater!
python main.py `
--host "10.10.10.10" --port 22 `
--user root --password password `
--cmd @'
echo "Hello World!"
uptime
echo "Bye!"
'@
python main.py --host "10.10.10.10" --port 22 `
--user root --password password `
--get "/path/to/remote/dir" --to "./relative/local/path" `
--unix --recursive
```

# build
```PowerShell
pip install pyinstaller
pyinstaller --onefile main.py --name "SshBot"
```

# license
MIT
