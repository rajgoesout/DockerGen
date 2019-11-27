# DockerGen

DockerGen is a GUI app that automagically dockerizes 🐳 your software project. 😉

## Getting Started

- Make sure you have python3, nodejs and yarn installed.

- Clone this repo:

```sh
$ git clone https://github.com/rajdeepbharati/DockerGen
```

- Create a virtualenv and set up backend:

```sh
$ cd DockerGen
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=main.py
$ export FLASK_ENV=dev # for dev server
$ flask run
```

- On a different terminal window, set up the frontend:

```sh
$ cd frontend
$ yarn install
$ yarn run build # for production build
$ yarn run serve # for hot reload dev server
```

Head over to http://localhost:8080 to browse your computer for projects!
