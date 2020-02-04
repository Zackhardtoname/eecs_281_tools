import glob, os
import subprocess

compare = False
test = True

os.chdir("./")
documents = dict()

for fn in glob.glob("*.txt"):
    if not any(prefix in fn for prefix in ["out", "my", "exclude_"]):
        documents[fn] = os.path.getsize(fn)

documents = {k: v for k, v in sorted(documents.items(), key=lambda item: item[1])}

buffer_types = ['queue', 'stack']
output_types = ['list', 'map']

subprocess.run("cppcheck --language=c++ --enable=all --suppress=missingIncludeSystem *.c* *.h*", shell=True, stdout=subprocess.PIPE).stdout
subprocess.run("make clean", shell=True, stdout=subprocess.PIPE).stdout
subprocess.run("make", shell=True, stdout=subprocess.PIPE).stdout

for fn in documents:
    for buffer_type in buffer_types:
        for output in output_types:
            if test:
                if "test" not in fn:
                    continue

            else:
                if "test" in fn:
                    continue

                if "no" not in fn:
                    complete_name = f"{fn.split('.')[0]}-{buffer_type}-{output}.txt"
                else:
                    complete_name = f"{fn}"

            args = f"./puzzle --{buffer_type} -o {output} < {fn}"
            print(args)

            if compare:
                args += f" > my-{complete_name}"
                diff_args = f"diff -Z out-{complete_name} my-{complete_name}"
                #diff -Z -u out-big-queue-list.txt my-big-queue-list.txt |colordiff |diff-highlight                                                               
                #print(diff_args)

            res = subprocess.run(args, shell=True, stdout=subprocess.PIPE).stdout

            if compare:
                res = subprocess.run(diff_args, shell=True, stdout=subprocess.PIPE).stdout
                if len(res):
                    print(len(res))
                    
                    if (len(res) < 1000):
                        print(res)

                    print()
            else:
                res = str(res)
                #print(res)
                should_have_res = not "no" in fn
                if not str(int(should_have_res)) in res:
                    print("\n\n???\n\n")