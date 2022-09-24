## How to Run Locally

Use Python 3.9 or later (this project was developed using Python 3.10.2).

Create and activate a virtual environment. Then run `pip install -r requirements.txt` to install all required packages.

In `project_one_bulletin/settings.py`, set `DEBUG = True`. Uncomment the `SECRET_KEY` used for testing.

Now, run `python manage.py makemigrations && python manage.py migrate` to initialize a local database.

Install the `git` and `heroku` CLIs.

Run `heroku local --port=8000` to test. Go to `0.0.0.0:8000` (or `0.0.0.0:8100`) in a browser.
