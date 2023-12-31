# SentimentAnalysisAPI
A django web backend server that has single api for collecting sentiment text as json format, analyze them with an optimization of pretrained bert model and return the sentiment of the text as a json response.

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

It is recommended to use virtual environment packages such as virtualenv. Follow the steps below to setup the project:
  - Clone this repository via `git clone https://github.com/parvez86/SentimentAnalysisAPI.git`
  - Use this command to install required packages `pip install -r requirements.txt`
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
    - **Others**: See documentation, add put appropriate database settings and install connector.
  - Check Migrations of the project via terminal: `python manage.py makemigrations`
  - Migrate the project from terminal: `python manage.py migrate`
  - Create admin user for admin panel from terminal: `python manage.py createsuperuser`. And enter the username, email and password. 
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
    - reponse will return:
      ```
        {
          "sentiment": "negative/neutral/positive"
        }
      ```


