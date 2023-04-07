import argparse
from fabric import Connection

def main():
  userInputs = _parse_arguments()
  # https://docs.fabfile.org/en/stable/api/connection.html
  if(userInputs.key):
    con = Connection(
      host=userInputs.host, port=userInputs.port, user=userInputs.user,
      connect_kwargs={ "key_filename": userInputs.key }
    )
  else:
    con = Connection(
      host=userInputs.host, port=userInputs.port, user=userInputs.user,
      connect_kwargs={ "password": userInputs.password }
    )
    
  CommandsArray = userInputs.cmd.splitlines()
  for command in CommandsArray:
    if(command):
      # https://docs.pyinvoke.org/en/latest/api/runners.html#invoke.runners.Runner.run
      con.run(command, warn=userInputs.warn)

def _parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', type=str, required=True)
  parser.add_argument('--port', type=str, required=False, default=22)
  parser.add_argument('--user', type=str, required=False, default="root")
  parser.add_argument('--password', type=str, required=False)
  parser.add_argument('--key', type=str, required=False)
  parser.add_argument('--cmd', type=str, required=False, default="uptime")
  parser.add_argument('--warn', type=bool, required=False, default=True)
  return parser.parse_args()

main()
