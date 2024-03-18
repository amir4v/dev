def where():
    until = open('until', 'r').read()
    until = int(until)
    return until


def write_where(index):
    index = str(index)
    open('until', 'w').write(index)
