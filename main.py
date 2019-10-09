import os
import sys
import json
import stat
import shutil

from flask import Flask, session, jsonify, request, redirect
from jinja2 import Environment, FileSystemLoader

# from templates import nodejshelper

app = Flask(__name__)

wsgi_app = app.wsgi_app

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Docker variables
portNumber = 3000
imageName = ''
serviceName = ''
composeProjectName = ''
DOCKERIGNORE_NAME = '.dockerignore'
DEBUG_DOCKERFILE_NAME = 'Dockerfile.debug'
DEBUG_DOCKERCOMPOSE_NAME = 'docker-compose.debug.yml'
RELEASE_DOCKERFILE_NAME = 'Dockerfile'
RELEASE_DOCKERCOMPOSE_NAME = 'docker-compose.yml'

FILE_SYSTEM_ROOT = '/'


@app.route('/')
def home():
    plat = sys.platform
    return 'Hello world. You\'re on ' + plat


@app.route('/browser')
def browse():
    itemList = os.listdir(FILE_SYSTEM_ROOT)
    return {'list': itemList}


@app.route('/browser/<path:urlFilePath>')
def browser(urlFilePath):
    nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, urlFilePath)
    if os.path.isdir(nestedFilePath):
        itemList = os.listdir(nestedFilePath)
        fileProperties = {'filepath': nestedFilePath}
        if not urlFilePath.startswith("/"):
            urlFilePath = '/' + urlFilePath
        return {'list': itemList}
    if os.path.isfile(nestedFilePath):
        fileProperties = {"filepath": nestedFilePath}
        # Opening the file and getting metadata
        sbuf = os.fstat(os.open(nestedFilePath, os.O_RDONLY))
        fileProperties['type'] = stat.S_IFMT(sbuf.st_mode)
        fileProperties['mode'] = stat.S_IMODE(sbuf.st_mode)
        fileProperties['mtime'] = sbuf.st_mtime
        fileProperties['size'] = sbuf.st_size
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return {'properties': fileProperties}
    return 'something bad happened'


def get_default_template_data(resp):
    return {
        'projectPath': resp['projectPath'],
        'lang': resp['lang'],
        'composeProjectName': resp['composeProjectName'],
        'imageName': resp['imageName'],
        'serviceName': resp['serviceName'],
        'portNumber': resp['portNumber'],
        'debugPortNumber': None,
        'isWebProject': resp['isWebProject'],
        'volumeMap': None,
        'includeComposeForDebug': False,
        'includeStartDebugging': False
    }


def handle_common(templateData):
    pass


def handle_nodejs(resp):
    templateData = get_default_template_data(resp)
    templateData['volumeMap'] = '.:/src'
    templateData['includeComposeForDebug'] = True
    templateData['debugPortNumber'] = "5858"

    print(templateData)
    nodeDockerfilePath = os.path.abspath('.') + '/templates/node/Dockerfile'
    projectDockerfilePath = templateData['projectPath'] + '/Dockerfile'
    env = Environment(loader=FileSystemLoader('./templates/node'))
    template = env.get_template('Dockerfile')
    output_from_parsed_template = template.render(
        # environment='debug',
        isWebProject=templateData['isWebProject'],
        portNumber=templateData['portNumber']
    )
    print(output_from_parsed_template)
    with open(projectDockerfilePath, 'w') as df:
        df.write(output_from_parsed_template)

    handle_common(templateData)


def handle_python(resp):
    pass


def do_stuff(resp):
    if resp['lang'] == 'nodejs':
        handle_nodejs(resp)


@app.route('/collectdata', methods=['GET', 'POST'])
def get_data():
    try:
        # absolute path of project root directory
        projectPath = request.json['projectPath']
        lang = request.json['lang']  # lang or framework
        isWebProject = request.json['isWebProject']
        if isWebProject:
            portNumber = request.json['portNumber']
        else:
            portNumber = 3000
        imageName = request.json['imageName']
        serviceName = request.json['serviceName']
        composeProjectName = request.json['composeProjectName']

        allowed_langs = ['python', 'nodejs', 'flask']
        if lang not in allowed_langs:
            return 'not possible'
        resp = {
            'projectPath': projectPath,
            'lang': lang,
            'isWebProject': isWebProject,
            'portNumber': portNumber,
            'imageName': imageName,
            'serviceName': serviceName,
            'composeProjectName': composeProjectName
        }
        do_stuff(resp)
        return jsonify(resp)
    except:
        return 'error'


# @app.route('/selectlang', methods=['GET', 'POST'])
# def select_language():
#     """Lang (?lang) can be nodejs/python(flask)"""
#     if not request.json or not 'lang' in request.json:
#         print('not found')
#         return redirect('/')
#     lang = request.json['lang']
#     allowed_langs = ['python', 'nodejs', 'flask']
#     if lang in allowed_langs:
#         return redirect('/ws', Response={'lang': lang})
#         # return jsonify({'lang': lang})
#     else:
#         print('not found')
#         return redirect('/')


# @app.route('/ws', methods=['GET', 'POST'])
# def web_server():
#     """Does ur app use web server? Can be 0 (false) or 1 (true).
#     Default: 1"""
#     if not request.json or not 'lang' in request.json:
#         print('not found')
#         return redirect('/')
#     try:
#         ws = request.json['ws']
#     except:
#         ws = 1
#     lang = request.json['lang']
#     return jsonify({'lang': lang, 'ws': ws})
