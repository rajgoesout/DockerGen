import os


def getTemplateDockerComposeFileName():
    return 'docker-compose.yml'


def getTemplateDockerFileName():
    return os.path.join(__file__, 'node', 'Dockerfile')
