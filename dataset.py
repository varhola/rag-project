import os
from helpers import data_to_vec

DATASET = {}
FILE_DATA = {}

def get_directories(dir):
    dir_list = os.listdir(dir)
    dirs = [f for f in dir_list if not os.path.isfile(dir + "/" + f)]
    return dirs

def get_filenames(dir):
    dir_list = os.listdir(dir)
    files = [f for f in dir_list if os.path.isfile(dir + "/" + f)]
    return files

def read_data(filenames):
    print(" Reading data from files...")
    data_size = 0
    for filename in filenames:
        with open(filename, 'r', encoding="utf8") as file:
            lines = file.readlines()
            FILE_DATA[lines[0][6:-1]] = "".join(lines)
            DATASET[lines[0][6:-1]] = []
            for line in lines[1:]:
                DATASET[lines[0][6:-1]].append({
                    "original": line,
                    "vector": data_to_vec(line)   
                })
            data_size += len(lines[1:])
    print(f' Ready reading files ({data_size} entries)')  

def create_dataset(dir="./data/LiHua-World"):
    print("Creating new dataset...")
    dir_names = get_directories(dir)
    filenames = []
    for d in dir_names:
        files = get_filenames(dir + "/" + d)
        for f in files:
            filenames.append(dir + "/" + d + "/" + f)
    print(len(filenames), "files to read")
    read_data(filenames)
