# generate all command to test out the sample maps
# usage in linux: python3 command_gen.py

import glob, os
import subprocess

os.chdir("./")
documents = dict()

for fn in glob.glob("*.txt"):
    if not any(prefix in fn for prefix in ["out", "my", "exclude_"]):
        documents[fn] = os.path.getsize(fn)

documents = {k: v for k, v in sorted(documents.items(), key=lambda item: item[1])}

buffer_types = ['q', 's']
output_types = ['list', 'map']

for fn in documents:
    for buffer_type in buffer_types:
        args = f"./puzzle -{buffer_type} -o list < {fn}"
        print(args)
        res = subprocess.run(args, shell=True, stdout=subprocess.PIPE).stdout
        res = str(res)
        print(res)
        should_have_res = not "no" in fn
        if not str(int(should_have_res)) in res:
            print("\n\n???\n\n")