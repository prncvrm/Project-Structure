# @author : Prince Verma
# @version : 1.0.0
# @date : 18-02-2019
# @email : prince.verma@innovaccer.com
# -*- encoding=UTF-8 -*-
import os
import sys
import argparse


class ProjectStructure:
    def __init__(self, args=None):
        parser = argparse.ArgumentParser()
        self.args = self.add_arguments(parser)
        self.horizontal = []
        self.vertical = []
        self.main()

    def add_arguments(self, parser):
        parser.add_argument('-s', '--source', type=str, const=True, nargs='?', default='/',
                            help='Enter Absolute Path to Project Folder')
        parser.add_argument('-o', '--output', type=str, const=True, nargs='?', default='project_structure',
                            help='Enter (Absolute Path)? to file name for output/project structure markdown')
        parser.add_argument('-id', '--i_directory', type=str, const=True, nargs='?', default='',
                            help='Enter directories to be ignored comma delimited')
        parser.add_argument('-ie', '--i_extension', type=str, const=True, nargs='?', default='',
                            help='Enter extensions to be ignored, comma delimited as .svg')
        return parser.parse_args()

    def explore_first_directory(self, _dir):
        folders = os.listdir(_dir)
        folders = self.remove_git_ignore(folders)

        folders.sort()

        files = []

        for folder in folders:
            # check if its a folder
            if os.path.isdir(os.path.join(_dir, folder)):
                self.vertical.append(['-', '-', folder])
                self.explore_nth_directory(os.path.join(_dir, folder), 2)
            else:
                files.append(folder)

        for file in files:
            self.vertical.append(['-', '-', file])

        return

    def explore_nth_directory(self, _dir, nth_level):
        folders = os.listdir(_dir)
        folders = self.remove_git_ignore(folders)

        folders.sort()

        files = []
        for folder in folders:
            # check if its a folder
            if os.path.isdir(os.path.join(_dir, folder)):
                self.create_horizontal(nth_level)
                self.horizontal.append(folder)
                self.vertical.append(self.horizontal)
                self.explore_nth_directory(
                    os.path.join(_dir, folder), nth_level+1)
            else:
                files.append(folder)

        for file in files:
            self.create_horizontal(nth_level)
            self.horizontal.append(file)
            self.vertical.append(self.horizontal)

        return

    def create_horizontal(self, nth_level):
        self.horizontal = ['-' for x in range(nth_level+1)]

    def remove_git_ignore(self, folders):
        # @re-tune this piece if you need to as per your requirement
        folders = [
            elts for elts in folders if elts not in self.git_ignore and not elts.startswith(".")]
        _folders = []
        for elts in folders:
            flag = 0
            for ends in self.git_ignore_astrik:
                if elts.endswith(ends):
                    flag = 1
                    break
            if flag == 0:
                _folders.append(elts)
        return _folders

    def git_ignore_parser(self):
        # check if git ignore file exists
        if not os.path.exists('.gitignore'):
            print("No Git Ignore File Exists.. Moving Ahead")
            return []
        with open('.gitignore') as fp:
            git_ignore = fp.readlines()
        # removing comments and new line and stirping
        self.git_ignore = [elt.strip().strip('\n').strip(
            '\t').strip("/") for elt in git_ignore if not elt.startswith("#") and not elt.startswith("\n")]
        self.git_ignore += [elt.strip()
                            for elt in self.args.i_directory.split(",")]
        self.git_ignore_astrik = [elt[1:].strip().strip("\n").strip("/")
                                  for elt in git_ignore if elt.startswith("*")]
        if not self.args.i_extension == '':
            self.git_ignore_astrik += [elt.strip()
                                       for elt in self.args.i_extension.split(",")]
        return

    def main(self):
        # checking if path exists
        if not os.path.exists(self.args.source):
            print(
                "Path Doesn't Exist")
            sys.exit(1)
        os.chdir(self.args.source)
        self.vertical.append(self.args.source.split("/")[-1:])

        folders = os.listdir(self.args.source)

        # removing the git ignore files/folders from folders and remove all dot files
        print("Getting Git Ignore Folders and Files")
        self.git_ignore_parser()
        print("Done, Parsing the Folders and subdirectory")

        folders = self.remove_git_ignore(folders)

        folders.sort()

        files = []

        for folder in folders:
            # check if its a folder
            if os.path.isdir(folder):
                self.vertical.append(['-', folder])
                self.explore_first_directory(
                    os.path.join(self.args.source, folder))
            else:
                files.append(folder)
        for file in files:
            self.vertical.append(['-', file])

        # writing to file
        f = open(self.args.output, 'w')
        f.write(self.vertical[0][0]+"\n")
        for idx in range(len(self.vertical[1:])):
            for elt in self.vertical[idx+1][:-2]:
                f.write("|")
                f.write("   ")
            try:
                if len(self.vertical[idx+1]) > len(self.vertical[idx+2]):
                    f.write("└──")
                else:
                    f.write("├──")
            except:
                f.write("└──")
            f.write(self.vertical[idx+1][-1:][0]+"\n")


if __name__ == '__main__':
    ProjectStructure()
