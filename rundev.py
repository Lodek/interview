from pathlib import Path
import subprocess
import sys, os
import venv

if not (Path('.') / '.venv').exists():
    print('venv not found, creating venv')
    venv.create('.venv', with_pip=True)
    print('venv created')

print('Installing poetry')
run = lambda cmd : subprocess.run(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)
run('pip install poetry')
run('poetry install')
print('Starting app')
run('python manage.py runserver 0.0.0.0:8000')
