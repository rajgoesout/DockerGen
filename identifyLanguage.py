import sys

from os import path

from identifyTraits import identify_special_file, identify_if_exists


def get_languages():
    try:
        language_file = open('languagesKnown.txt', 'r+')
    except:
        language_file = open('languagesKnown.txt', 'w')
        language_file.close()
        return []

    languages = []
    s = language_file.readline()
    while s != '':
        if s.strip() != '':
            languages.append(s.strip())
        s = language_file.readline()
    language_file.close()

    return languages


def combine_scores(list_of_scores, languages):
    finalTally = []
    for lang in languages:
        finalTally.append([0, lang])
    for j in list_of_scores.items():
        for i in j[1].items():
            for k in range(len(finalTally)):
                if i[0] == finalTally[k][1]:
                    finalTally[k][0] += i[1] * 100
    finalTally.sort()

    for i in range(min(len(finalTally), 5)):
        print(
            f'{i+1}. {finalTally[len(finalTally)-i-1][1]} - {int(finalTally[len(finalTally)-i-1][0]*100)}')


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
    if not path.exists(source):
        print(f'Absolute path {source} doesn\'t exist!')
        sys.exit()
    languages = get_languages()
    list_of_scores = {}
    list_of_scores['special_files'] = identify_special_file(languages, source)
    list_of_scores['filesThatExist'] = identify_if_exists(languages, source)

    print(list_of_scores)
    combine_scores(list_of_scores, languages)
