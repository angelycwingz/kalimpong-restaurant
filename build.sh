
#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

npm ci
npm run build:css
npm run build:js

python manage.py check
python manage.py collectstatic --noinput --clear --ignore="*/input.css"
