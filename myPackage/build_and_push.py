import os 

def build_and_push_c7(logger, exe_path, project_path, bin_name):
    logger.run_cmd("build_and_push.bat {} {} {}".format(exe_path, project_path, bin_name))

def build_and_push_c6(logger, exe_path, project_path, bin_name):
    origin_dir = os.getcwd()
    print('cd ', project_path)
    os.chdir(project_path)
    logger.run_cmd("CMax.bat")
    print('cd ', origin_dir)
    os.chdir(origin_dir)
