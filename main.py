import os
import stat
import sys

from flask import Flask, jsonify, request
from jinja2 import Environment, FileSystemLoader

from .allowaxios import crossdomain

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
@crossdomain(origin='*')
def home():
    plat = sys.platform
    return 'Hello world. You\'re on ' + plat


@app.route('/browser')
@crossdomain(origin='*')
def browse():
    itemList = os.listdir(FILE_SYSTEM_ROOT)
    itemListDetailed = []
    for item in itemList:
        itemOriginal = item
        item = os.path.join(FILE_SYSTEM_ROOT, item)
        if os.path.isfile(item):
            print('isdir')
            itemD = (item, 'F', itemOriginal)  # file
        elif os.path.isdir(item):
            print('isfile')
            itemD = (item, 'D', itemOriginal)  # directory
        else:
            print('isnone')
            itemD = (item, None, itemOriginal)  # unknown
        itemListDetailed.append(itemD)
    print(itemListDetailed)
    return {'list': itemListDetailed}


@app.route('/browser/<path:urlFilePath>')
@crossdomain(origin='*')
def browser(urlFilePath):
    nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, urlFilePath)
    if os.path.isdir(nestedFilePath):
        itemList = os.listdir(nestedFilePath)
        fileProperties = {'filepath': nestedFilePath}
        if not urlFilePath.startswith('/'):
            urlFilePath = '/' + urlFilePath
        itemListDetailed = []
        for item in itemList:
            itemOriginal = item
            item = os.path.join(urlFilePath, item)
            if os.path.isfile(item):
                itemD = (item, 'F', itemOriginal)  # file
            elif os.path.isdir(item):
                itemD = (item, 'D', itemOriginal)  # directory
            else:
                itemD = (item, None, itemOriginal)  # unknown
            itemListDetailed.append(itemD)
        print(itemListDetailed)
        return {'list': itemListDetailed}
    if os.path.isfile(nestedFilePath):
        fileProperties = {"filepath": nestedFilePath}
        # Opening the file and getting metadata
        sbuf = os.fstat(os.open(nestedFilePath, os.O_RDONLY))
        fileProperties['type'] = stat.S_IFMT(sbuf.st_mode)
        fileProperties['mode'] = stat.S_IMODE(sbuf.st_mode)
        fileProperties['mtime'] = sbuf.st_mtime
        fileProperties['size'] = sbuf.st_size
        if not urlFilePath.startswith('/'):
            urlFilePath = '/' + urlFilePath
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
    print(templateData)
    print(templateData['projectPath'])


def handle_nodejs(resp):
    templateData = get_default_template_data(resp)
    templateData['volumeMap'] = '.:/src'
    templateData['includeComposeForDebug'] = True
    templateData['debugPortNumber'] = "5858"

    # print(templateData)
    nodeDockerfilePath = os.path.abspath('.') + '/templates/node/Dockerfile'
    projectDockerfilePath = templateData['projectPath'] + '/Dockerfile'
    env = Environment(loader=FileSystemLoader('./templates/node'))
    template = env.get_template('Dockerfile')
    output_from_parsed_template = template.render(
        # environment='debug',
        isWebProject=templateData['isWebProject'],
        portNumber=templateData['portNumber'],
        debugPortNumber=templateData['debugPortNumber']
    )
    # print(output_from_parsed_template)
    with open(projectDockerfilePath, 'w') as df:
        df.write(output_from_parsed_template)

    handle_common(templateData)


def handle_golang(resp):
    templateData = get_default_template_data(resp)
    # templateData['volume']

    goDockerfilePath = os.path.abspath('.') + '/templates/go/Dockerfile'
    projectDockerfilePath = templateData['projectPath'] + '/Dockerfile'
    env = Environment(loader=FileSystemLoader('./templates/go'))
    template = env.get_template('Dockerfile')
    output_from_parsed_template = template.render(
        # environment='debug',
        isWebProject=templateData['isWebProject'],
        portNumber=templateData['portNumber']
    )
    # print(output_from_parsed_template)
    with open(projectDockerfilePath, 'w') as df:
        df.write(output_from_parsed_template)

    handle_common(templateData)


def handle_python(resp):
    pass


def do_stuff(resp):
    print(resp)
    nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, resp['projectPath'])
    if os.path.isdir(nestedFilePath):
        itemList = os.listdir(nestedFilePath)
        fileProperties = {'filepath': nestedFilePath}
        if not resp['projectPath'].startswith('/'):
            resp['projectPath'] = '/' + resp['projectPath']
        d = {'list': itemList}
        for i in itemList:
            # print(i)
            if i == 'requirements.txt' or i == 'Pipfile':
                print('python/flask/django')
                lang = 'py'
            elif i == 'package.json':
                print('nodejs')
                lang = 'nodejs'
            elif i == 'Cargo.toml':
                print('rust')
                lang = 'rust'
        for i in itemList:
            if i == 'main.py':
                entry = 'main.py'
            elif i == 'app.py':
                entry = 'app.py'
        # print(d)
    if resp['lang'] == 'nodejs':
        handle_nodejs(resp)


@app.route('/collectdata', methods=['GET', 'POST'])
@crossdomain(origin='*')
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

        allowed_langs = ['python', 'nodejs', 'flask', 'go']
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
