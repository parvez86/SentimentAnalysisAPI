# SentimentAnalysisAPI
A Django web backend server that has a single API for collecting sentiment text in JSON format, analysing it with an optimisation of a pretrained BERT model and returning the sentiment of the text as a JSON response.

#### Files Format
Column Title | Description
------------ | -------------
Data | [Sp1786/multiclass-sentiment-analysis-dataset](https://huggingface.co/datasets/Sp1786/multiclass-sentiment-analysis-dataset/viewer/Sp1786--multilabel-sentiment-dataset/validation)
Pretrained Model | [bert-base-uncased](https://huggingface.co/bert-base-uncased)
Label | 0, 1 or 2 . '0' for neutral, '1' for positive and '2' for negative
# Installation
Requires the following packages:
  - Python 3.9.7 or higher
  - Django 4.0 or higher
  - pip 22.3.1 or higher

It is recommended to use virtual environment packages such as virtualenv. Follow the steps below to set up the project:
  - Clone this repository via `git clone https://github.com/parvez86/SentimentAnalysisAPI.git`
  - Create and Activate a Virtual Environment (Recommended):
      ```
      Bash
      python -m venv venv
      # On Windows
      .\venv\Scripts\activate
      # On macOS/Linux
      source venv/bin/activate
      ```
  - Use this command to install required packages: `pip install -r requirements.txt`
  - Crate database and change database settings in `settings.py` according to your database.
    - **Mysql**:
       ```
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql', 
                'NAME': 'DB_NAME',
                'USER': 'DB_USER',
                'PASSWORD': 'DB_PASSWORD',
                'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
                'PORT': '3306',
            }
        }
        ```
    - **SQLite**:
      ```
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'mydatabase', # This is where you put the name of the db file. 
                         # If one doesn't exist, it will be created at migration time.
            }
        }
      ```
    - **Others**: See documentation, add appropriate database settings and install the connector.
  - Check Migrations of the project via terminal: `python manage.py makemigrations`
  - Migrate the project from terminal: `python manage.py migrate`
  - Create admin user for admin panel from terminal: `python manage.py createsuperuser`. Then enter the username, email and password. 
  - Run the project from terminal: `python manage.py runserver`

# Usage
- Run the model
- At endpoind `/analyze`:
    - add request payload:
      ```
        {
          "text": "write your sentences"
        }
      ```
    - response will return:
      ```
        {
          "sentiment": "negative/neutral/positive"
        }
      ```


