""" Builtins/Executives/_files.py """

import threading
import fnmatch
import pathlib
import os

import Modules.exceptions as Exceptions
import Modules.display as Display
import Modules.files as Files


def find_files(args):
    """ Find all files or directories with given query in name."""
    query = args['query']
    location = args['location']
    exact_search = args['exact']

    if location == "?":
        location = None
    if not location is None:
        if not os.path.exists(location):
            raise Exceptions.NotExists

    if exact_search is None:
        exact_search = False

    if not exact_search:
        if "*" not in query:
            query = f"*{query}*"

    class _Counter:
        directories = 0
        files = 0

    def search(_location):
        """ Iterate thru all directories in given _location and search for files and dirs. """


        for root, dirs, files in os.walk(_location):
            for file in files:
                if fnmatch.fnmatch(file, query):
                    _Counter.files += 1
                    print(f"FILE: {os.path.join(root, file)}")

            for directory in dirs:
                if fnmatch.fnmatch(directory, query):
                    _Counter.directories += 1
                    print(f"DIR:  {os.path.join(root, directory)}")


    Display.Message.info("Searching started...")

    # Check if location is provided. If no, search all disks.
    if location is None:

        all_disks = Files.get_all_disks()

        # Create threaded task for every disk.
        threads_list = list(
            map(
                lambda _disk: threading.Thread(target=search, args=[_disk]), all_disks
            )
        )

        # Search all disks at the same time.
        [ thread.start() for thread in threads_list ]

        # Join all threads after done job.
        [ thread.join() for thread in threads_list ]

    # Search only in provided location.
    else:
        search(location)

    Display.Message.success(f"Search ended. ({_Counter.files} files, {_Counter.directories} dirs)")

def delete_temp_files(_):
    """ Delete all files that ends with .tmp/.temp
    and content of directories with temp word in it's names. """

    def _remove(path):
        try:
            os.remove(path)
            return True

        except (PermissionError, OSError):
            return False

    deleted_files = 0
    deleted_dirs = 0
    errors_count = 0

    all_disks = Files.get_all_disks()

    Display.Message.info("Deleting process started. This may take a while...")

    for disk in all_disks:

        # Walk thru all files in given disk.
        for root, dirs, files in os.walk(disk):

            # Remove all found .tmp or .temp files.
            for file in files:
                if file.endswith((".tmp", '.temp')):
                    if _remove(root + "\\" + file): deleted_files += 1
                    else: errors_count += 1

            # Clear directories named temp.
            for directory in dirs:
                if "temp" in directory.lower():
                    deleted_dirs += 1

                    try:
                        for _file in os.listdir(root + "\\" + directory):
                            if _remove(root + "\\" + _file): deleted_files += 1
                            else: errors_count += 1 

                    except (PermissionError, OSError):
                        errors_count += 1

    Display.Message.success(
        f"Process ended. ({deleted_files} files, {deleted_dirs} dirs, {errors_count} errors)"
    )

def show_file_content(args, session):
    """ Show colorized content of file. """
    file_path = os.path.join(session.cwd, args['file'])

    if not os.path.exists(file_path):
        raise Exceptions.NotExists
    if not os.path.isfile(file_path):
        raise Exceptions.NotFile
    if not Files.has_permissions(file_path):
        raise Exceptions.NoPermissions

    with open(file_path, "r", errors='ignore') as opened_file:

        lines = opened_file.readlines()
        line_number_space_prefix = len(str(len(lines)))
        formatted_content = ""

        # Format file content.
        for index, line in enumerate(lines):

            for char in ['(', ')', '{', '}', '<', '>', ":", ";"]:
                line = line.replace(char, f"\033[35m{char}\033[37m")

            for char in ['"', "'"]:
                line = line.replace(char, f'\033[32m{char}\033[37m')

            for char in ['=']:
                line = line.replace(char, f'\033[34m{char}\033[37m')

            for char in ["+", "-", "*", "/", "%", ":", "?", "|", "!",
                         ".", "@", "#", "$", "&", "*", "~", ","]:
                line = line.replace(char, f'\033[33m{char}\033[37m')

            s_count = int(line_number_space_prefix-len(str(index+1)))
            ready_line = f"\033[1;36m{' ' * s_count}{index+1} \033[2;37m| \033[0;37m{line}\033[37m"
            formatted_content += ready_line

    print(formatted_content)

def find_big_files(args):

    bottom_limit_gb = args['bottom_limit']
    if bottom_limit_gb is None:
        bottom_limit_gb = 8

    all_disks = Files.get_all_disks()

    class _Counter:
        hits = 0
        size_gb = 0

    def search(disk):

        for root, dirs, files in os.walk(disk):
            for file in os.listdir(root):
                try:
                    size = os.path.getsize(os.path.join(root+"\\"+file))

                except:
                    size = 0

                finally:

                    # Round size to GB and check with bottom limit.
                    if size:
                        size = round(size/1024/1024/1024, 2) # Gb

                        if size > bottom_limit_gb:
                            _Counter.hits+= 1
                            _Counter.size_gb += size
                            path = os.path.join(root+"\\"+file)
                            print(f'({size} gb) {path}')

    Display.Message.info("Searching process started.")

    # Create threaded task for every disk.
    threads_list = list(map(lambda _disk: threading.Thread(target=search, args=[_disk]), all_disks))

    # Search all disks at the same time.
    [ thread.start() for thread in threads_list ]

    # Join all threads after done job.
    [ thread.join() for thread in threads_list ]

    Display.Message.success(
        f"Process ended. ({_Counter.hits} found, {round(_Counter.size_gb, 2)} Gb total)"
    )

def list_directory(args, session):
    """ Show all files and subdirectories in given path."""
    path = args['path']
    if path is None:
        path = session.cwd
    else:
        if not os.path.exists(path):
            raise Exceptions.NotExists
        path = pathlib.Path(path)

    print(f"\npath: {path.absolute()}")

    try:
        dirs, files = Files.list_dir(path.absolute())
    except:
        raise Exceptions.OsError

    Display.Message.bullet_list("directories", dirs)
    Display.Message.bullet_list("files", files)

def change_working_directory(args, session):
    """ Change CWD in session instance. """

    directory = args['directory']
    current = session.cwd

    new_path = pathlib.Path(
        os.path.abspath(
            os.path.join(
                str(current.absolute()),
                directory
            )
        )
    )

    if not new_path.exists():
        raise Exceptions.NotExists
    if not new_path.is_dir():
        raise Exceptions.NotDirectory

    session.cwd = new_path

def make_directory(args, session):
    """ Create directory. """

    name = args['name']
    working_path = session.cwd
    new_dir_path = os.path.join(working_path, name)

    if os.path.exists(new_dir_path):
        raise Exceptions.NameAlreadyTaken

    try:
        os.mkdir(new_dir_path)
    except PermissionError:
        raise Exceptions.NoPermissions
    except:
        raise Exceptions.OsError

def make_file(args, session):
    """ Create file. """

    name = args['name']
    working_path = session.cwd
    new_file_path = os.path.join(working_path, name)

    if os.path.exists(new_file_path):
        raise Exceptions.NameAlreadyTaken

    try:
        open(new_file_path, 'a+').close()
    except PermissionError:
        raise Exceptions.NoPermissions
    except:
        raise Exceptions.OsError

def delete_object(args, session):
    """ Delete file or directory. """

    name = args['name']
    working_path = session.cwd
    object_path = pathlib.Path(os.path.join(working_path, name))

    if not os.path.exists(object_path):
        raise Exceptions.NotExists

    try:
        object_path.unlink()
    except PermissionError:
        raise Exceptions.NoPermissions
    except:
        raise Exceptions.OsError

def rename_object(args, session):
    """ Rename file or directory. """

    obj = args['obj']
    working_directory = session.cwd
    name = args['new_name']

    path = pathlib.Path(os.path.join(working_directory, obj))
    if not path.exists():
        raise Exceptions.NotExists

    if os.path.exists(os.path.join(working_directory, name)):
        raise Exceptions.NameAlreadyTaken

    try:
        path.rename(os.path.join(working_directory, name))
    except PermissionError:
        raise Exceptions.NoPermissions
    except:
        raise Exceptions.OsError
