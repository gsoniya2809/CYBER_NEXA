"""Run the compiled CYBERNEXA app and SQLite API from one command."""
import sys
from pathlib import Path
if sys.version_info < (3,11):
    raise SystemExit('CYBERNEXA requires Python 3.11 or newer.')
sys.path.insert(0,str(Path(__file__).resolve().parent/'backend'))
from server import main
if __name__=='__main__':main()
