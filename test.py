import os

nodejs = ['keystone', 'pencilblue', 'apostrophe', 'cody',
          'hashbrown-cms', 'strapi', 'enduro', 'Raneto', 'uppy', 'zenbot']

flask = ['microblog', 'flaskbb', 'indico', 'open-event-server', 'securedrop', 'security_monkey', 'timesketch', 'airflow', 'skylines', 'Frozen-Flask', 'chat', 'quokka', 'redispapa', 'pypress',
         'overholt', 'newsmeme', 'motiky', 'zerqu', 'GuitarFan', 'moin-2.0', 'sync-engine', 'flask-restful', 'flask-api', 'flask-realworld-example-app', 'uploooaad', 'reco-engine', 'discover-flask']

django = ['FetchMe', 'fetchmewebapp', '3DmapsDjango', 'my-first-blog', 'groupio', 'wemake-django-template', 'django2-project-template', 'django-webpack-starter',
          'ponee', 'cookiecutter-django', 'djangox', 'drfx', 'django-project-template', 'docker-django', 'zulip', 'pythonic-news', 'django-oscar', 'Django-CRM', 'saleor']

go = ['awesome-go', 'go-app', 'istio', 'harbor', 'fabric', 'nomad', 'aws-sdk-go', 'rancher', 'chubaofs', 'sourcegraph', 'dgraph',
      'easyjson', 'jwt-go', 'act', 'origin', 'packer', 'gorm', 'dapr', 'argo', 'operator-lifecycle-manager', 'fzf', 'chat', 'operator-sdk']

rust = ['Rocket', 'RustPython', 'actix', 'actix-web', 'amethyst', 'cargo', 'citybound', 'coreutils', 'diesel', 'ffsend', 'firecracker', 'hexyl',
        'hyper', 'ktmpl', 'leaf', 'libra', 'navi', 'nushell', 'sonic', 'spotify-tui', 'starship', 'swc', 'tokio', 'xi-editor', 'xsv', 'bf-rs']

scala = ['predictionio', 'akka', 'CMAK', 'gitbucket', 'lila', 'linkerd', 'openwhisk',
         'prisma', 'polynote', 'mmlspark', 'sbt-native-packager', 'reactivemongo-demo-app']

n = len(flask)

lang = 'flask'
dataset = lang + 'Dataset'

print(n)
for i in range(n):
    # os.system('python3 reader.py -s /Users/rajdeep/' + dataset + '/' +
    #           go[i] + ' -l ' + lang)
    print(flask[i])
    os.system('python3 identifyLanguage.py -s /Users/rajdeep/' + dataset + '/' +
              flask[i])
    print()
