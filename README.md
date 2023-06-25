# SentimentAnalysisAPI
A django web backend server that has single api for collecting sentiment text as json format, analyze them with a custom machine learning model  and return the sentiment of the text as a json response. In the project gensim vectorizer is used for word embedding and Multi-layer Perceptron classifier is used for classifying sentiments type.

#### List of files

* train_df.csv
* val_df.csv
* test_df.csv
* model_state.bin

#### Files Format
Column Title | Description
------------ | -------------
Data | [Sp1786/multiclass-sentiment-analysis-dataset](https://huggingface.co/datasets/Sp1786/multiclass-sentiment-analysis-dataset/viewer/Sp1786--multilabel-sentiment-dataset/validation)
Label | 0, 1 or 2 . '0' for neutral, '1' for positive and '2' for negative
# Installation
Requires the following packages:
  - Python 3.9.7 or higher
  - Django 4.0 or higher
  - pip 22.3.1 or higher

It is recommended to use virtual environment packages such as virtualenv. Follow the steps below to setup the project:
  - Clone this repository via `git clone https://github.com/parvez86/SentimentAnalysisAPI.git`
  - Download the given optimized built model [model_state_cpu.bin](https://drive.google.com/file/d/1N60L3uA6fNyItlMvgA2Nqc-e-Wg2KZmq/view?usp=sharing) and put it to the `model` folder (beside the `data` folder). For gpu enabled model [model_state_gpu.bin](https://drive.google.com/file/d/1hbsH4Yc-ylegNjB8sJteeIK5E4QFsdth/view?usp=sharing) and rename the model file.
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
