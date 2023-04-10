import argparse
from fabric import Connection

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
      connect_kwargs={ "password": userInputs.password }
    )
  else:
    con = Connection(
      host=userInputs.host, port=userInputs.port, user=userInputs.user
    )
    
  CommandsArray = userInputs.cmd.splitlines()
  for command in CommandsArray:
    if(command):
      # https://docs.pyinvoke.org/en/latest/api/runners.html#invoke.runners.Runner.run
      con.run(command, warn=userInputs.warn)

  if userInputs.put and userInputs.to:
    con.put(userInputs.put, remote=userInputs.to, preserve_mode=userInputs.preserve)
  if userInputs.get and userInputs.to:
    # workarond for bug of Fabric version 3.0.0 on Windows
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
  parser.add_argument('--key', type=str, required=False)
  parser.add_argument('--cmd', type=str, required=False)
  parser.add_argument('--warn', type=bool, required=False, default=True)
  parser.add_argument('--put', type=str, required=False)
  parser.add_argument('--get', type=str, required=False)
  parser.add_argument('--to', type=str, required=False)
  parser.add_argument('--preserve', type=bool, required=False, default=False) # isPreserve
  parser.add_argument('--recursive', type=bool, required=False, default=True) # isRecursive
  parser.add_argument('--unix', type=bool, required=False, default=True)      # isUnix
  return parser.parse_args()

main()
