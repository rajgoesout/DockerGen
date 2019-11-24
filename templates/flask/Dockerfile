FROM python:3
WORKDIR /src
RUN pip install requirements.txt
EXPOSE {{ portNumber }}
RUN export FLASK_APP=main.py
{% if environment == 'debug' %}
RUN export FLASK_ENV=development
EXPOSE {{ debugPortNumber }}
{% endif %}
ENTRYPOINT [ "/bin/bash", "-c", "flask run" ]
COPY . /src
