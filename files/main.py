from multiprocessing.connection import wait
import os
import re
__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"

# 1
cwd = os.getcwd()
cache_path = os.path.join(cwd, 'cache')


def clean_cache():

    if os.path.exists(cache_path):
        for file in os.scandir(cache_path):
            os.remove(file.path)
        print('cache geleegd')
    else:
        os.mkdir(cache_path)
        print("Folder gemaakt, genaamd: cache")
    return


print(clean_cache())

# 2

zip_path = os.path.join(cwd, 'data.zip')


def cache_zip(zip_file_path, cache_dir_path):
    import zipfile
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(cache_dir_path)
       # print(f'{zip_file_path} is unpacked in: {cache_dir_path}')
        print('Zip unpacked in ' + cache_path)
    return


cache_zip(zip_path, cache_path)


# 3


def cached_files():

    only_files = [os.path.join(cache_path, f) for f in os.listdir(
        cache_path) if os.path.isfile(os.path.join(cache_path, f))]

    return only_files


cached_file_list = cached_files()
print(cached_file_list)

# 4


def find_password(cached_file_list):
    for file in cached_file_list:
        with open(file, 'r') as f:
            text = f.readlines()
          #  print(text)
            for line in text:
                if 'password' in line:
                    # print(line)
                   # print(len(line))
                    password = line[line.find(':')+2:38]
                    return password


print(find_password(cached_files()))
