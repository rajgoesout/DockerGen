def numbers_with_zero(file_, lang):
    import re
    # Note:current regex will convert floats and ints to 0
    # if one wants to just convert ints, and convert them to 1
    # do line = re.sub(r'[-+]?\d+',r'1',line)

    file_contents = []

    # read file, change lines
    with open(file_, 'r') as f:
        for line in f:
            # this regex should take care of ints, floats, and sings, if any
            line = re.sub(r'[-+]?\d*\.\d+|\d+',r'0',line)
            file_contents.append(line)

    # reopen file and write changed lines back
    with open('./database/'+lang+'/filesThatExist.txt', 'w') as f:
        for line in file_contents:
            f.write(line)

lang='rust'

numbers_with_zero('./database/'+lang+'/specialFiles.txt', lang)
