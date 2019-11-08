

import sys
import os
from os.path import isfile, join
​
def read_arg():
    if len(sys.argv) < 2:
        print("Incorrect arguement count. Please specify zip file name.")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Too many arguements provided. Only specify zip file name.")
        sys.exit(1)
    else:
        return sys.argv[1]
​
zip_file = read_arg()
dependency_file = "requirements.txt"
bot_code_dir = "bot-code"
path = os.path.abspath(".")
bot_code_path = path + "/" + bot_code_dir
​
# Run pipenv commands
os.system("pipenv lock -r > " + dependency_file)
os.system("cat " + dependency_file)
os.system("pipenv run pip download -d ./" + bot_code_dir + "/ -r " + dependency_file)
​
# Create a string list of names of files downloaded from pipenv command
files = [f for f in os.listdir(bot_code_path) if isfile(join(bot_code_path, f))]
​
# Unzip .whl and .tar files
for file in files:
    ext_split = file[-4:]
    ext = ext_split.split('.')
    # if ext[-1] == 'whl' or ext[-1] == 'gz':
    #     print(file)
​
    if ext[-1] == 'whl':
        os.system("unzip -o " + bot_code_path + "/" + file + " -d ./" + bot_code_dir)
        os.system("rm " + bot_code_path + "/" + file)
​
    if ext[-1] == 'gz':
        os.system("tar xvfz " + bot_code_path + "/" + file + " -C ./" + bot_code_dir)
        os.system("rm " + bot_code_path + "/" + file )
    # print(file)
​
# Remove requirements.txt file
os.system("rm " + dependency_file)
​
# Create zip file to be uploaded to Artifactory
os.system("zip -r " + zip_file + " ./" + bot_code_dir)
