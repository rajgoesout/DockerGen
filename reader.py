import os
import sys

from traits import add_special_files, add_if_file_exists, get_data_from_file


SPECIAL_FILE_TYPES = [
    'urls.py', 'manage.py', 'Pipfile', 'requirements.txt',
    'Pipfile.lock', 'wsgi.py', 'settings.py', '__pycache__',
    'package.json', 'package-lock.json', 'yarn.lock',
    'Cargo.toml', 'Cargo.lock'
]
SPECIAL_FILE_TYPES = [
    'urls_py', 'manage_py', 'Pipfile', 'requirements_txt',
    'Pipfile_lock', 'wsgi_py', 'settings_py', '__pycache__',
    'package_json', 'package-lock_json', 'yarn_lock',
    'Cargo_toml', 'Cargo_lock'
]


def checkDir(directory):
    d = os.path.dirname('./database/' + str(directory) + '/')
    if not os.path.exists(d):
        os.makedirs(d)


def get_language():
    try:
        language_file = open('languagesKnown.txt', 'r+')
    except:
        language_file = open('languagesKnown.txt', 'w')
        language_file.close()
        language_file = open('languagesKnown.txt', 'r+')

    languages = []
    s = language_file.readline()
    while s != '':
        if s.strip() != '':
            languages.append(s.strip())
        s = language_file.readline()

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-l':
            for j in languages:
                if sys.argv[i+1] == j:
                    language_file.close()
                    checkDir(j)
                    return str(j)
            language_file.seek(0, 2)
            language_file.write(str(sys.argv[i+1]) + '\n')
            language_file.close()
            checkDir(sys.argv[i+1])
            return str(sys.argv[i+1])

    language_file.close()
    print('Please specify -l <language>: language/framework of',
          'the project')
    sys.exit()


def add_to_db(language, source):
    # add_special_files(language, source)
    add_if_file_exists(language, source)


if __name__ == '__main__':
    source = None
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-s':
            source = sys.argv[i+1]
            break
    if source == None:
        print('Please specify -s <source> as absolute path of the',
              'project root')
        sys.exit()
    if source[-1] == '/':
        source = source[:-1]
    language = get_language()
    add_to_db(language, source)
