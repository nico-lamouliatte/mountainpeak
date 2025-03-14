To launch the local app, install the requirements then use the command uvicorn main:app

To test the docker app, use the command docker run -p 8000:8000 $(docker build -q .)

To run the docker app and save what you've done,

* Buid the app with the command docker build -t mountain_peaks .
* Run the app with the command docker run -p 8000:8000 mountain_peaks

The documentation is available in 2 types of formats:

* Locally provided by Swagger UI at http://127.0.0.1:8000/docs
* Locally provided by ReDoc at http://127.0.0.1:8000/redoc

To run the tests on the app and get the coverage, use the commands

* coverage run -m pytest
* coverage report -m