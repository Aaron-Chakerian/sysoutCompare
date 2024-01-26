'''
This program is designed to compile, run and compare output to a 
supplied answer.txt file

'''
import os
import subprocess
import logging

java_project_name:str = ""
java_files = []
bin_folder_dir:str = ""

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
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"{e.stderr}")
        return False
    
def run_one(bin_path:str, class_file_path: str):
    print(bin_path)
    cmd = "java -classpath {} {}".format(bin_path, bin_path + "/" + class_file_path)
    try:
        subprocess.run(cmd, shell=True, capture_output=True, check=True, text=True).stdout
        logging.info("Successfully Run " + class_file_path)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"{e.stderr}")
        return False

def find_java_files():
    global java_project_name
    global java_files
    global bin_folder_dir

    all_files = os.walk(os.curdir)
    flag = False
    for dirpath, dirname, filenames in all_files:
        for f in filenames:
            if ".java" in f:
                java_files.append(dirpath + "/" + f)
        for d in dirname:
            if "bin" in d:
                bin_folder_dir = (dirpath + "/" + d)
            if not flag and "." not in d and not java_project_name:
                java_project_name = d
    logging.basicConfig(filename='diagnostics.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("\n    Project Name: " + java_project_name)
    logging.info("bin folder: " + bin_folder_dir)
    for j in java_files:
        logging.info("java file path: " + j)
        
def retrieve_class_filename(path:str) -> str:
    pathname = path.split("/")
    pathname = pathname[-1].split(".java")[0]
    return pathname + ".class"

if __name__ == "__main__":
    remove_class_files(os.curdir)
    find_java_files()
    compile_one(bin_folder_dir, java_files[0])
    s = retrieve_class_filename(java_files[0])
    run_one(bin_folder_dir, s)
