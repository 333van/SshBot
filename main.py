import argparse
from fabric import Connection, Config
from invoke import Responder

def main():
  userInputs = _parse_arguments()
  # https://docs.fabfile.org/en/stable/api/connection.html
  if userInputs.key:
    con = Connection(
      host=userInputs.host, port=userInputs.port, user=userInputs.user,
      connect_kwargs={ "key_filename": userInputs.key }
    )
  elif userInputs.password:
    con = Connection(
      host=userInputs.host, port=userInputs.port, user=userInputs.user,
      connect_kwargs={ "password": userInputs.password, 'look_for_keys': False }
    )
  else:
    con = Connection(
      host=userInputs.host, port=userInputs.port, user=userInputs.user,
      connect_kwargs={ 'look_for_keys': True }
    )

  suWatcher = None
  if userInputs.su:
    suWatcher = Responder(
      pattern=r'Password:',
      response=f"{userInputs.su}\n"
    )

  CommandsArray = userInputs.cmd.splitlines()
  for command in CommandsArray:
    if command:
      # https://docs.pyinvoke.org/en/latest/api/runners.html#invoke.runners.Runner.run
      if suWatcher:
        con.run(f'su root -c "{command}"', warn=userInputs.warn, watchers=[suWatcher])
      else:
        con.run(command, warn=userInputs.warn)

  if userInputs.put and userInputs.to:
    con.put(userInputs.put, remote=userInputs.to, preserve_mode=userInputs.preserve)
  elif userInputs.get and userInputs.to:
    # workarond for bug of Fabric version 3.0.0 on Windows for Unix system
    if userInputs.recursive and userInputs.unix:
      findOut = con.run(f"find {userInputs.get} -print")
      fileLines = findOut.stdout.split('\n').pop() # poping the last empty line from "find" command
      for fileLine in fileLines:
        con.get(fileLine, local=f"{userInputs.to}/{fileLine}")
    else: 
      con.get(userInputs.get, local=userInputs.to, preserve_mode=userInputs.preserve)

def _parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', type=str, required=True)
  parser.add_argument('--port', type=str, required=False, default=22)
  parser.add_argument('--user', type=str, required=False, default="root")
  parser.add_argument('--password', type=str, required=False)
  parser.add_argument('--su', type=str, required=False)
  parser.add_argument('--key', type=str, required=False)
  parser.add_argument('--cmd', type=str, required=False)
  parser.add_argument('--warn', type=bool, required=False, default=True)
  parser.add_argument('--put', type=str, required=False)
  parser.add_argument('--get', type=str, required=False)
  parser.add_argument('--to', type=str, required=False)
  parser.add_argument('--preserve', type=bool, required=False, default=False)
  parser.add_argument('--recursive', type=bool, required=False, default=True)
  parser.add_argument('--unix', type=bool, required=False, default=True)
  # parser.add_argument('--pty', type=bool, required=False, default=False)
  return parser.parse_args()

main()
