import os, mimetypes, re, functools


def list_type(top, mimes: [str] or None):
    for file in list_file(top):
        mime, encoding = mimetypes.guess_type(file)
        if mimes is None or mime in mimes:
            yield mime, file


def list_file(top):
    for path, dirs, files in os.walk(top=top):
        for file in files:
            yield os.path.join(path, file)


def main():
    for mime, file in list_type('.', ['image/svg+xml', 'text/css']):
        if not file.endswith(('close.svg', 'close-active.svg', 'close-hover.svg')):
            with open(file, 'r') as f:
                s = substitute_color(f.read())
            with open(file, 'w') as f:
                f.write(s)

    # with open('./gnome-shell.css', 'r') as f:
    #     s = substitute_color(f.read())
    # with open('./gnome-shell.css', 'w') as f:
    #     f.write(s)

    # substitute_color('asd #ABC, #aabbcc, rgba(100, 110, 120, 0.5)')


def substitute_color(s, re3=re.compile(r'#([\da-fA-F])([\da-fA-F])([\da-fA-F])($|[^\da-fA-F])'),
                     re6=re.compile(r'#([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})($|[^\da-fA-F])'),
                     re_rgba=re.compile(r'rgba\((\d+)\s?,\s?(\d+)\s?,\s?(\d+)\s?,\s([\d\.]+)\)')):
    s = substitute_pattern(s, re6, lambda m: '#' + 3 * '{:02X}'.format(
        int(round(sum([int(i, 16) for i in m.groups()[:3]]) / 3))) + m.group(4))
    s = substitute_pattern(s, re3, lambda m: '#' + 3 * '{:02X}'.format(
        int(round(sum([int(i, 16) * 17 for i in m.groups()[:3]]) / 3))) + m.group(4))
    s = substitute_pattern(s, re_rgba, lambda m: 'rgba({0}, {0}, {0}, {1})'.format(
        int(round(sum([int(i) for i in m.groups()[:3]]) / 3)), m.group(4)))
    return s


def substitute_pattern(s, pattern, func):
    ret = ""
    m = pattern.search(s)
    while m:
        ret += s[:m.start()] + func(m)
        s = s[m.end():]
        m = pattern.search(s)
    ret += s
    return ret


main()
