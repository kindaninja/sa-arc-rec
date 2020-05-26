from pathlib import Path
import re
import networkx as nx
import matplotlib.pyplot as plt

CODE_ROOT_FOLDER = '/Users/egh/Zeeguu-Core/zeeguu_core/'


def extract_import_from_line(line):
    x = re.search("^import zeeguu_core\.([a-z_]+)", line)
    x = re.search("^from zeeguu_core\.([a-z_]+)", line)

    if x:
        print(str(x))

    return x.group(1)


def imports(file):
    # extracts all the imported modules from a file
    lines = [line for line in open(file)]

    all_imports = []
    for line in lines:
        try:
            all_imports.append(extract_import_from_line(line))
        except:
            continue

    return all_imports


def module_from_file_path(folder_prefix, full_path):
    # extracting a module from a file name
    # e.g. /Users/mircea/Zeeguu-Core/zeeguu_core/model/user.py -> zeeguu_core.model.user

    file_name = full_path[len(folder_prefix):]
    file_name = file_name.replace("/", ".")
    file_name = file_name.replace(".py", "")
    return file_name


def module(full_path):
    return module_from_file_path(CODE_ROOT_FOLDER, full_path)


def dependencies_graph():
    files = Path(CODE_ROOT_FOLDER).rglob("*.py")

    G = nx.Graph()

    for file in files:
        m = module(str(file))
        if m not in G.nodes:
            G.add_node(m)

        for each in imports(str(file)):
            G.add_edge(m, each)

    return G


def top_level_module(module_name, depth=1):
    # extracts the parent of depth X
    # e.g. top_level_module(zeeguu_core.model.util, 1) -> zeeguu_core
    components = module_name.split(".")
    return ".".join(components[:depth])


def abstracted_to_top_level(G):
    dG = nx.DiGraph()
    for each in G.edges():
        source = top_level_module(each[0])
        destination = top_level_module(each[1])
        # print(source + " " + destination)
        dG.add_edge(source, destination)

    return dG

def draw_graph_with_labels(G, figsize=(10,10)):
    plt.figure(figsize=figsize)
    nx.draw(aG, with_labels=True, font_size=20, arrowsize=20)
    plt.show()


G = dependencies_graph()
aG = abstracted_to_top_level(G)
draw_graph_with_labels(aG, (30,30))