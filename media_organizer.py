import os
import time
import sys

ext = {
        'videos':[".mp4", ".avi", ".3gp", ".mpeg", ".mkv", ".wmv", ".mov"],
        'photos':[".jpg", ".jpeg", ".png"]
        }


def get_time(path):
    modified = os.path.getmtime(path)
    return str(time.ctime(modified).split(" ")[-1])


def get_filename(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            file_ext = os.path.splitext(filename)[-1].lower()
            if ext in ext['videos'] or file_ext in ext['photos']:
                return filename


def locate_files(src_path):
    paths = []
    for root, dirs, files in os.walk(src_path):
        for filename in files:
            file_ext = os.path.splitext(filename)[-1].lower()
            if file_ext in ext['videos']:
                file_path = os.path.join(root, filename)
                paths.append((file_path, get_time(file_path), "videos"))
            elif file_ext in ext['photos']:
                file_path = os.path.join(root, filename)
                paths.append((file_path, get_time(file_path), "photos"))
    return paths


def is_dir(dir_name):
    if os.path.exists(dir_name):
        return True
    else:
        return False


def make_main_dir(dst_path, path):
    f_time = ""

    f_time = path[1]
    f_name = os.path.join(dst_path, f_time)
    if is_dir(f_name):
        pass
    else:
        os.mkdir(f_name)

    return f_name


def make_sub_dir(main_dir, paths):
    typee = paths[2]
    type_dir = os.path.join(main_dir, typee)
    if is_dir(type_dir):
        pass
    else:
        os.mkdir(type_dir)
    return type_dir


def move_files(src_path, dst_path):
    paths = locate_files(src_path)
    if is_dir(dst_path):
        for pth in paths:
            dst_path1 = make_sub_dir(make_main_dir(dst_path, pth), pth)
            os.link(pth[0], os.path.join(dst_path1, os.path.basename(pth[0])))
            dst_path1 = ""
    else:
        os.mkdir(dst_path)
        for pth in paths:
            dst_path1 = make_sub_dir(make_main_dir(dst_path, pth), pth)
            os.link(pth[0], os.path.join(dst_path1, os.path.basename(pth[0])))
            dst_path1 = ""


move_files(sys.argv[1], sys.argv[2])
