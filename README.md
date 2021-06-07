# website-fruits-classification

Our website for Bangkit Capstone Project that can predict the level of ripeness of fruits and how much the cost would be.

## Run locally

Go to the project folder
or
use this command.

```bash
cd PATH_TO/fruit-freshness-detector-web
```
Use [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```
Create python virtual environment.

```bash
pip install virtualenv
virtualenv venv
```
initialize virtual environment
```bash
source venv/bin/activate
```
or in windows
```
.\venv\bin\activate
```
run flask app
```bash
flask run
```
Type http://127.0.0.1:5000/ on your browser.

## Deploy to cloud

Heroku Deployment
```bash
heroku login
heroku git:clone -a fruit-freshness-detector-web
cd fruit-freshness-detector-web
git add .
git commit -am "make it better"
git push heroku master
```
App Engine Google Cloud Platform Deployment
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/fruit-freshness-detector-web
gcloud run deploy --image gcr.io/PROJECT-ID/fruit-freshness-detector-web  
```

## API

### Recognize Image

----

  Return recognize result as JSON.

* **URL**

  /api/recognize

* **Method:**

  `POST`

* **Content-Type**

  `multipart/form-data`

* **Data Params**

   `image=[file]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ freshness_level : 100, price : 10000 }`

## Run Test
```
python -m unittest discover tests
``` 

## License
[MIT](https://choosealicense.com/licenses/mit/)
