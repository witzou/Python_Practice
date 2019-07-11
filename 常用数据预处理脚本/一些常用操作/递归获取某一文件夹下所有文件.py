import os


file_path = 'C:/Users/Administrator/Desktop/My_C_Project'


def get_file_paths_recursive(folder=None, file_ext=None):
    """ Get the absolute path of all files in given folder recursively
    :param folder:
    :param file_ext:
    :return:
    """
    file_list = []
    if folder is None:
        return file_list


    print('clw:os.walk(folder) = ', os.walk(folder))
    for dir_path, dir_names, file_names in os.walk(folder):
        print('clw:dir_path = ', dir_path)
        print('clw:dir_names = ', dir_names)
        print('clw:file_names = ', file_names)
        print('\n')
        for file_name in file_names:
            if file_ext is None:
                file_list.append(os.path.join(dir_path, file_name))
                continue
            if file_name.endswith(file_ext):
                file_list.append(os.path.join(dir_path, file_name))
    return file_list




print('clw: get_file_paths_recursive = ', get_file_paths_recursive(file_path))