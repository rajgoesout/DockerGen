import os

from reader import get_data_from_file


def identify_special_file(languages, source):
    # TODO: Need to normalize this trait (very important)
    # I guess it is done now!
    """
    Computes scores on the basis of frequency of file/folder 
    present in a project.
    """
    scores = {}

    for language in languages:
        databasefile = open('./database/' + str(language) +
                            '/specialFiles.txt', 'r')

        special_files = databasefile.readlines()

        if len(special_files) // 2 > 10:
            topN = len(special_files) // 2
        else:
            topN = len(special_files)

        topN_special_files = special_files  # [:topN]

        projectsparsedfile = open(
            './database/' + str(language) + '/projectsParsed.txt').read()
        lang_projects_count = int(projectsparsedfile)

        _sum = 0
        lang_score = 0
        for topSF in topN_special_files:
            mc = os.popen('cd ' + source + ' && find . -print | grep -w "' +
                          topSF.split(' ')[0] + '"').read()
            mc = mc.split('\n')[:-1]
            freq_topSF_in_src = len(mc)
            freq_topSF_in_lang_db = int(topSF.split(' ')[1][:-1])
            avg_freq_topSF_in_lang_db = freq_topSF_in_lang_db / lang_projects_count
            if avg_freq_topSF_in_lang_db == 0:
                avg_freq_topSF_in_lang_db = 0.0000000000000001
            item = ((freq_topSF_in_src - avg_freq_topSF_in_lang_db) /
                    avg_freq_topSF_in_lang_db) ** 2
            if freq_topSF_in_src >= 0:
                if item == 0:
                    item = 0.0000000000000001
                lang_score += (1/item)
            else:
                lang_score += 0
            # _sum += ((freq_topSF_in_src - freq_topSF_in_lang_db) /
            #          freq_topSF_in_lang_db) ** 2

        # if _sum == 0:
        #     _sum = 0.0000000000000001
        # lang_score = 1 / _sum

        lang_score /= len(special_files)

        scores[language] = lang_score
        databasefile.close()

    summed_scores = 0
    for language in languages:
        summed_scores += scores[language]
    # print(summed_scores)
    # print('gscores', scores)
    for language in languages:
        try:
            scores[language] /= summed_scores
        except ZeroDivisionError:
            scores[language] = 0

    return scores


def identify_if_exists(languages, source):
    """
    Identify if a file exists in a project, and return a 
    score on that basis. Doesn't consider the frequency 
    (number of times a file is present in a single project).
    """
    scores = {}

    for language in languages:
        databasefile = open('./database/' + str(language) +
                            '/filesThatExist.txt', 'r')

        special_files = databasefile.readlines()

        projectsparsedfile = open(
            './database/' + str(language) + '/projectsParsed.txt').read()
        lang_projects_count = int(projectsparsedfile)

        _sum = 0
        lang_score = 0
        for SF in special_files:
            # print('splt', SF.split(' ')[0], source)
            # os.system('cd ' + source)
            mc = os.popen('cd ' + source + ' && find . -print | grep -w "' +
                          SF.split(' ')[0] + '"').read()
            mc = mc.split('\n')[:-1]
            # print(language, SF, mc, 'l', len(mc))
            # freq_SF_in_src = len(mc)
            if len(mc):
                exists_in_src = 1
            else:
                exists_in_src = 0
            freq_SF_in_lang_db = int(SF.split(' ')[1][:-1])
            SF_existence_ratio_in_lang = freq_SF_in_lang_db / lang_projects_count

            if SF_existence_ratio_in_lang == 0:
                SF_existence_ratio_in_lang = 0.0000000000000001
            # print(language, SF, freq_SF_in_lang_db, lang_projects_count,
            #       SF_existence_ratio_in_lang, 'exists', exists_in_src, 'l', len(
            #           mc), 'sumv',
            #       ((exists_in_src - SF_existence_ratio_in_lang) /
            #        SF_existence_ratio_in_lang) ** 2)
            # _sum += (SF_existence_ratio_in_lang ** 2)
            # print(language, SF, ((exists_in_src - SF_existence_ratio_in_lang) /
            #          SF_existence_ratio_in_lang)**2)
            # if exists_in_src:
            #     _sum += ((1 - SF_existence_ratio_in_lang) /
            #              SF_existence_ratio_in_lang)**2

            # _sum += ((exists_in_src - SF_existence_ratio_in_lang) /
            #          SF_existence_ratio_in_lang) ** 2
            item = ((exists_in_src - SF_existence_ratio_in_lang) /
                    SF_existence_ratio_in_lang) ** 2
            if exists_in_src:
                if item == 0:
                    item = 0.0000000000000001
                lang_score += (1/item)
            else:
                lang_score += 0

        # print(language, _sum)
        _sum /= len(special_files)
        # print(language, _sum)
        # _sum = _sum ** 2

        # if _sum == 0:
        #     _sum = 0.0000000000000001
        # lang_score = 1 / _sum

        lang_score /= len(special_files)

        scores[language] = lang_score
        databasefile.close()

    summed_scores = 0
    for language in languages:
        summed_scores += scores[language]

    for language in languages:
        try:
            scores[language] /= summed_scores
        except ZeroDivisionError:
            scores[language] = 0

    return scores
