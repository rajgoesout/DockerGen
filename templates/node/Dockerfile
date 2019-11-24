FROM node
{% if environment == 'debug' %}
RUN npm install nodemon -g
{% endif %}
WORKDIR /src
{% if isWebProject %}
EXPOSE {{ portNumber }}
{% endif %}
{% if environment == 'debug' %}
EXPOSE {{ debugPortNumber }}
ENTRYPOINT ["/bin/bash", "-c", "if [ -z \"$REMOTE_DEBUGGING\" ]; then nodemon -L --debug; else nodemon -L --debug-brk; fi"]
{% else %}
ENTRYPOINT ["npm", "start"]
{% endif %}
COPY . /src
RUN npm install
