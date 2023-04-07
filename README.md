It's a commandline utility to help automate SSH tasks, based on Fabric in Python.
I build this because plink.exe from PuTTY don't have everything that I need.
It's only tested on Python 3.10. 

# use
```PowerShell
pip install fabric argparse
python main.py `
--host 192.168.0.1 --port 22 `
--user root --password password `
--cmd @'
echo "Hello World!"
uptime
echo "Bye!"
'@
```

# build
```PowerShell
pip install pyinstaller
pyinstaller --onefile main.py --name "SshBot"
```

# license
MIT
