'''
This program is designed to compile, run and compare a java project vs a "Answer.txt" file.
Ideally to be placed alongside a java project folder, it will collect all the .java files and bin folder then
compile the 
'''

import os
import subprocess
import logging
logging.addLevelName(25, "OUTPUT")
#removes all the class files in all subdirectories
def remove_class_files(path:str):
    files = os.listdir(path)
    for f in files:
        if ".class" in f:
            os.remove(path + "/" + f)
        if "." not in f:
            remove_class_files(path + "/" + f)

def compile_one(bin_path:str, compile_file_path: str):
    cmd = "javac -d {} {}".format(bin_path, compile_file_path)
    try:
        subprocess.run(cmd, shell=True, check=True)
        logging.info("Compilation Successful: " + compile_file_path)
        return get_class_name(compile_file_path)
    except subprocess.CalledProcessError as e:
        logging.error("Compilation Error: "f"{compile_file_path}")
    
def find_java_files():
    java_project_name = ""
    java_files = []
    bin_folder_dir = ""

    all_files = os.walk(os.curdir)
    flag = False
    for dirpath, dirname, filenames in all_files:
        for f in filenames:
            if ".java" in f:
                java_files.append(dirpath + "/" + f)
                logging.info(java_files[-1])
        for d in dirname:
            if "bin" in d:
                bin_folder_dir = (dirpath + "/" + d)
                logging.info("bin folder: " + bin_folder_dir)
            if not flag and "." not in d and not java_project_name:
                java_project_name = d
                logging.info("\n    Project Name: " + java_project_name)
    return (java_project_name, bin_folder_dir, java_files)

def run_one_class(bin_path:str, class_name:str):
    cmd = ["java", "-cp", bin_path, class_name]
    try:
        sysout = subprocess.run(cmd, capture_output=True,check=True, text=True).stdout
        logging.info("Runtime on " + class_name + ".class, output = " + sysout)
        return sysout
    except subprocess.CalledProcessError as e:
        logging.error(f"{e.stderr}")

def run_all(bin_path:str, class_names: list[str]):
    stdout = []
    for c in class_names:
        temp = run_one_class(bin_path, c)
        if temp:
            stdout.append(temp)
    return stdout

def compile_all(bin_path:str, compile_list: list[str]):
    java_classes = []
    for java_file in compile_list:
        temp = compile_one(bin_path, java_file)
        if temp:
            java_classes.append(temp)
    return java_classes
    
def get_class_name(s:str):
    s = s.split("/")[-1]
    return s.split(".")[0]

if __name__ == "__main__":
    remove_class_files("./")
    logging.basicConfig(filename='diagnostics.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%D %a %H:%M')
    (project_name, bin_folder, java_files) = find_java_files()
    java_classes = compile_all(bin_folder, java_files)
    print(run_all(bin_folder, java_classes))