import codecs


def read(file_name, encoding=None):
    if encoding:
        input_file = codecs.open(file_name, 'r', encoding)
    else:
        input_file = open(file_name, 'r')

    data = []
    for input_line in input_file:
        data.append(input_line.replace("\n", ""))
    return data


def write(file_name, lines, encoding=None):
    if encoding:
        file = codecs.open(file_name, 'w', encoding)
    else:
        file = open(file_name, 'w')

    for line in lines:
        file.write(str(line) + "\n")
    file.close()
