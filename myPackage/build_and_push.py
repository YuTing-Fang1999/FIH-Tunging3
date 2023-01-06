import os 

def build_and_push_c7(exe_path, project_path, bin_name):
    os.system("build_and_push.bat {} {} {}".format(exe_path, project_path, bin_name))