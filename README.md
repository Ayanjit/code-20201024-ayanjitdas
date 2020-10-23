# code-20201024-ayanjitdas

Steps to run the code:
1. Pull the source
2. Install the python modules from requirements.txt
3. Run the server with -> python manage.py runserver

To fetch data from server:
Base api link: http://127.0.0.1:8000/api/bmicalculator
url parameter = personJSON, values = persondata.json and persondata2.json

example api url:
1. For 4 person data: http://127.0.0.1:8000/api/bmicalculator?personJSON=persondata.json
2. For 1lac person data: http://127.0.0.1:8000/api/bmicalculator?personJSON=persondata2.json