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
echo "Hello World!"; BashVariable="This will not get passed"
# each line is of a saperated run, and so "$BashVariable" is empty
uptime; echo "BashVariable: $BashVariable"
'@
# get files from a remote Unix host. This will probably not work on your system
python main.py --host "10.10.10.10" --port 22 `
--user root --password password `
--get "/path/to/remote/dir" --to "./relative/local/path" `
--unix --recursive
# using --su to invoke command with 'su'
python main.py --host 10.10.10.10 --user ssh_user `
--password ssh_user_password --su root_password `
--cmd "cat /etc/shadow"
```

# build
```PowerShell
pip install pyinstaller
pyinstaller --onefile main.py --name "SshBot"
```

# license
MIT
