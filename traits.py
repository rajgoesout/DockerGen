import os


def get_data_from_file(language, filename):
    """
    :param language:
        The programming language or framework of the given project,
        as specified by the user.
    :param filename:
        The files inside database/<language>/ directory.
        Currently there is just one file (specialFiles.txt).
    """
    fileExists = False
    data = {}
    # IOError if file does not exist already
    try:
        textfile = open('./database/' + str(language) +
                        '/' + str(filename), 'r')
        fileExists = True
    except:
        pass

    # read database into memory
    if fileExists:
        temp = textfile.readline().strip()
        while temp != '':
            data[temp.split(' ')[0]] = int(temp.split(' ')[1])
            temp = textfile.readline().strip()
        textfile.close()
    return data


def add_special_files(language: str, source: str):
    """
    Writes frequency of special files present in a project.
    :param language:
        The programming language or framework of the given project,
        as specified by the user.
    :param source:
        Source directory absolute path of the project root.
    """
    special_files = get_data_from_file(language, 'specialFiles.txt')

    for special_file in special_files:
        sfs = os.popen(
            'find ' + source + ' -print | grep -w "' +
            special_file + '"').read().split('\n')[:-1]
        sf_count = len(sfs)
        special_files[special_file] += sf_count
    sfsl = []
    for sf in special_files.items():
        sfsl.append(sf)
    sfsl.sort(key=lambda x: x[1])
    sfsl.reverse()

    writefile = open('./database/' + language + '/specialFiles.txt', 'w')
    for i in sfsl:
        writefile.write(i[0] + ' ' + str(i[1]) + '\n')
    writefile.close()

    trainsetcount = open('./database/' + language +
                         '/projectsParsed.txt', 'r+')
    count = trainsetcount.read()
    if count[-1] == '\n':
        count = int(count[:-1])
    else:
        count = int(count)
    count += 1
    trainsetcount.seek(0)
    trainsetcount.truncate()
    trainsetcount.write(str(count))
    trainsetcount.close()


def add_if_file_exists(language: str, source: str):
    special_files = get_data_from_file(language, 'filesThatExist.txt')

    for special_file in special_files:
        sfs = os.popen(
            'find ' + source + ' -print | grep -w "' +
            special_file + '"').read().split('\n')[:-1]

        if len(sfs):
            # write True if file exists in a project
            special_files[special_file] += 1
    sfsl = []
    for sf in special_files.items():
        sfsl.append(sf)
    sfsl.sort(key=lambda x: x[1])
    sfsl.reverse()

    writefile = open('./database/' + language + '/filesThatExist.txt', 'w')
    for i in sfsl:
        writefile.write(i[0] + ' ' + str(i[1]) + '\n')
    writefile.close()

    trainsetcount = open('./database/' + language +
                         '/projectsParsed.txt', 'r+')
    count = trainsetcount.read()
    if count[-1] == '\n':
        count = int(count[:-1])
    else:
        count = int(count)
    count += 1
    trainsetcount.seek(0)
    trainsetcount.truncate()
    trainsetcount.write(str(count))
    trainsetcount.close()


# def add_all_files(language: str, source: str):
#     """
#     Meant for the unsupervised learning algorithm.
#     """
