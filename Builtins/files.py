from Modules.commands import Command, Parameter
from Modules.data_types import DataType

import Builtins.Executives._files as exe

Command('find', exe.find_files, [Parameter('query', DataType.Text, 'Search query. Can contain "*" as all.'), Parameter('location', DataType.Text, 'Search location as path.', required=False)], 'Find files with given query.')
Command('deltmp', exe.delete_temp_files, [], 'Delete temporary files from all disks')
Command('dsp', exe.show_file_content, [Parameter('file', DataType.Text, 'File path')], 'Display colored file content.', True)
Command('bigf', exe.find_big_files, [Parameter('bottom_limit', DataType.Number, 'Minimum size of file to be treated as "big"', required=False)], "Show all files with greater size than limit.")
Command('ld', exe.list_directory, [Parameter('path', DataType.Text, 'Path of directory', required=False)], "Show list of files in current directory.", True)
Command('cd', exe.change_working_directory, [Parameter('directory', DataType.Text, 'New directory, use ".." to get into previous directory')], "Move current working directory into other directory", True)
Command('mkd', exe.make_directory, [Parameter('name', DataType.Text, 'Name of new directory')], 'Create new directory in current path.', True)
Command('mkf', exe.make_file, [Parameter('name', DataType.Text, 'Name of new file (with .ext)')], 'Create file with given name in current path.', True)
Command('rm', exe.delete_object, [Parameter('name', DataType.Text, 'Name of file or directory to delete')], 'Delete object named as parameter value, can be dir or file.', True)
Command('ren', exe.rename_object, [Parameter('obj', DataType.Text, 'Target object current name'), Parameter('new_name', DataType.Text, 'New object\'s name.')], 'Rename object.', True)
