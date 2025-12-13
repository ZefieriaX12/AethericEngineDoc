# How to Run

The project uses mostly Python 3.12 internal modules along with peewee (refer to requirements.txt)

Windows
- python.exe main.py
Linux
- python3 main.py

## Behaviour
- You will be prompted to enter the host, port and jwt token (inputs are hidden)
- A SQLite DB storage.db will be created
- Entries will be written into storage.db
- After writing 600 (binary + ascii) entries, program will end
