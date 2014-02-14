#!/usr/bin/env python

import os
import string
import subprocess
import sys


execname = sys.argv.pop(0)
topdir = os.path.normpath(os.path.join(os.path.abspath(execname),
                                       os.pardir, os.pardir))


def execute(*cmd, **kwargs):
    cmd = map(str, cmd)
    attempts = kwargs.pop('attempts', 1)

    while attempts > 0:
        attempts -= 1
        try:
            obj = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            if not attempts:
                raise
        except Exception as e:
            command = ' '.join(cmd)
            raise Exception('%s failed due to: %s' % (
                command, str(e)))


def update_diagrams_by_dir(source_dir, target_dir):
    dirs = []
    files = []

    for name in os.listdir(source_dir):
        path = os.path.join(source_dir, name)
        if (os.path.isfile(path)
           and not path.startswith('.')
           and path.endswith('.wsd')):
            files.append(name)
        elif os.path.isdir(path):
            dirs.append(name)

    for source_file in files:
        source_path = os.path.join(source_dir, source_file)
        target_file = os.path.splitext(source_file)[0]
        output = string.join([target_file , 'png'], sep='.')
        target_path = os.path.join(target_dir, output)

        getmtime = os.path.getmtime
        if (not os.path.exists(target_path)
            or getmtime(source_path) > getmtime(target_path)):
            try:
                print "updating %s" % source_path
                command = ['mkdir', '-p', target_dir]
                execute(*command, attempts=2)
                tools_dir = os.path.join(topdir, 'tools')
                generate_script = os.path.join(tools_dir, 'gendiagram.py')
                command = ['python', generate_script,
                           '-i', source_path,
                           '-o', target_path]
                execute(*command, attempts=2)
            except Exception as e:
                print "%s failed to generate diagram due to: %s" % (
                    source_path, str(e))

    for directory in dirs:
        source_path = os.path.join(source_dir, directory)
        target_path = os.path.join(target_dir, directory)
        update_diagrams_by_dir(source_path, target_path)


if __name__ == '__main__':

    source_dir = os.path.join(topdir, 'crystal', 'source')
    target_dir = os.path.join(topdir, 'crystal', 'target')

    update_diagrams_by_dir(source_dir, target_dir)
