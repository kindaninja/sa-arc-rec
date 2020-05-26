import os
from pathlib import Path

CODE_ROOT_FOLDER = '/Users/egh/git/Zeeguu-Core/zeeguu_core/'


def LOC(file):
    return sum([1 for line in open(file)])


for root, dirs, files in os.walk(CODE_ROOT_FOLDER):
        level = root.replace(CODE_ROOT_FOLDER, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)

        max_loc = 0
        max_name = 'hey.py'
        for f in files:
            if '__init__' not in f:
                loc = LOC(str(root + "/" + f))
                if max_loc < loc:
                    max_loc = loc
                    max_name = f

        if '.py' in f:
            if max_loc > 0:
                print('{}{}'.format(subindent, max_name + ' (' + str(max_loc) + ' loc)'))
        else:
            print('{}{}/'.format(subindent, max_name))