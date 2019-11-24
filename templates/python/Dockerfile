FROM python:3
WORKDIR /src
RUN pip install requirements.txt
ENTRYPOINT [ "/bin/bash", "-c", "python app.py" ]
COPY . /src
