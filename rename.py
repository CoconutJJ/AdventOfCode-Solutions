from glob import glob
from shutil import move
from os.path import join
from re import match, compile

files = glob("**/**/*.py")

for f in files:

    year, day, file = f.split("/")

    if "puzzle" not in file:
        continue
    
    pattern = compile("puzzle(\d{1,2}).py")

    matching = match(pattern, file)

    day_no = int(matching.groups()[0])

    old_file_name = f
    new_file_name = join(year, day, "%02d.py" % day_no)
    old_path_name = join(year, day)
    new_path_name = join(year, "%02d" % day_no)
    
    print(new_file_name, new_path_name)

    # move(old_file_name, new_file_name)
    # move(old_path_name, new_path_name)

