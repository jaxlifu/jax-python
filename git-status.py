#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


def find_git_files(path):
    f = open('git-status-log.log', 'w')
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if name.startswith(".git"):
                #os.remove(os.path.join(root, name))
                local = os.path.join(root, name)
                print("find git root: %s and project is %s\n ===================>" % (
                    root, local))
                os.chdir(root)
                os.system('git status')
                x = os.popen('git status').read()
                if not'nothing to commit, working directory clean' in x:
                    log = "current local is :=========> \n  %s \n git status log is  :========> \n %s \n" % (
                        root, x)
                    f.write(log)
    f.close()


# test
if __name__ == "__main__":
    path = os.getcwd()
    find_git_files(path)
