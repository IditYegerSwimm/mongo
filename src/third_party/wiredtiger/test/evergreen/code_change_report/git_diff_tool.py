#!/usr/bin/env python
#
# Public Domain 2014-present MongoDB, Inc.
# Public Domain 2008-2014 WiredTiger, Inc.
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


#
# The code in this file is used to generate diff files that exclude any newly added 0-length files
# as loading diff files that contain newly added 0-length files does not work in pygit2.
#
# Note: 0-length means empty files with no content. Files containing only blank lines are not 0-length, and
# diffs including such files work in pygit2.
#

import argparse
import glob
import os
import subprocess
from typing import List
from pygit2 import discover_repository, Repository
from push_working_directory import PushWorkingDirectory


def run_command(directory: str, command: str) -> str:
    working_directory = PushWorkingDirectory(directory)
    completed_process = subprocess.run(command, capture_output=True, check=True, shell=True)
    output = completed_process.stdout
    working_directory.pop()
    return output.decode()


def find_zero_length_files(directory: str) -> List[str]:
    working_directory = PushWorkingDirectory(directory)
    files = glob.glob('./**/*', recursive=True)
    zero_length_files = [x for x in files if os.stat(x).st_size == 0]
    working_directory.pop()
    return zero_length_files


def create_diff_file(git_working_tree_dir: str, diff_file: str, verbose: bool) -> None:
    # Exclude files with 0-length from the diff, as pygit2 doesn't handle such diffs well
    zero_length_files = find_zero_length_files(git_working_tree_dir)
    exclude_files_param = ' '.join([f"':(exclude){file}'" for file in zero_length_files])

    repository_path = discover_repository(git_working_tree_dir)
    assert repository_path is not None
    repo = Repository(repository_path)

    head_commit = repo.head.target
    merge_base_commit = run_command(git_working_tree_dir, "git merge-base develop HEAD").strip()
    diff_command = f"git diff {merge_base_commit} -- {exclude_files_param}"

    if verbose:
        print(f"head_commit:        {head_commit}")
        print(f"merge_base_commit:  {merge_base_commit}")
        print(f"zero_length_files = {zero_length_files}")
        print(f"diff_command:       {diff_command}")

    diff_output = run_command(git_working_tree_dir, diff_command)
    diff_output += "\n"   # Ensure there is a newline on the end of the diff before writing to a file.

    file = open(diff_file, "w")
    file.write(diff_output)
    file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--git_root', required=True, help='path of the Git working directory')
    parser.add_argument('-d', '--git_diff_file', required=True, help='Path to the git diff file that will be created')
    parser.add_argument('-v', '--verbose', action="store_true", help='be verbose')
    args = parser.parse_args()

    verbose = args.verbose
    git_diff_file = args.git_diff_file
    git_working_tree_dir = args.git_root

    if verbose:
        print('Diff Generation')
        print('===============')
        print('Configuration:')
        print(f'  Git root path:              {git_working_tree_dir}')
        print(f'  Git diff output file path:  {git_diff_file}')

    create_diff_file(git_working_tree_dir=git_working_tree_dir, diff_file=git_diff_file, verbose=verbose)


if __name__ == '__main__':
    main()
