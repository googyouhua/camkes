#!/usr/bin/env python
#
# Copyright 2016, NICTA
#
# This software may be distributed and modified according to the terms of
# the BSD 2-Clause license. Note that NO WARRANTY is provided.
# See "LICENSE_BSD2.txt" for details.
#
# @TAG(NICTA_BSD)
#

import argparse, multiprocessing, os, stat, subprocess, sys, string

MY_DIR = os.path.abspath(os.path.dirname(__file__))

def escape_xml(string):
    return string.replace('<', '&lt;').replace('>', '&gt;')

def main(argv):
    parser = argparse.ArgumentParser(
        description='run CAmkES integration tests')
    parser.add_argument('--jobs', '-j', type=int,
        default=multiprocessing.cpu_count(), help='number of parallel jobs')
    parser.add_argument('--verbose', '-v', action='store_true',
        help='be verbose with output')
    opts = parser.parse_args(argv[1:])

    printable = set(string.printable)

    sys.stdout.write("<testsuite>\n")

    for t in sorted(os.listdir(MY_DIR)):
        path = os.path.join(MY_DIR, t)
        mode = os.stat(path).st_mode
        if t.endswith(".tcl") and not stat.S_ISDIR(mode) and \
                os.access(path, os.X_OK):

            sys.stdout.write("<testcase classname='camkesnexttest' name='%s'>\n" % t)

            sys.stdout.write('Running %s ... ' % t)
            sys.stdout.flush()

            # Subprocess for running the test_process
            # It is assumed that this script will be located in projects/camkes/tests relative
            # to the project's top level directory. The working directory from which to run
            # the build commands is determined relative to this script's location, so this script
            # can be run from any location.
            test_process = subprocess.Popen([path, str(opts.jobs)], cwd=os.path.join(MY_DIR, '../../..'),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            lines = []

            for line in iter(test_process.stdout.readline, b''):
                sys.stdout.write(escape_xml(line))
                lines.append(line)

            test_process.wait()

            if test_process.returncode == 0:
                sys.stdout.write('-- Passed --\n')
            else:

                sys.stdout.write("<failure type='failure'>\n")

                sys.stdout.write('-- Failed --\n')

                # Print the output within the <failed> tag
                output = filter(lambda x: x in printable, "\n".join(lines))
                sys.stdout.write(' -- output %s --\n%s' % (t, escape_xml(output)))

                sys.stdout.flush()
                sys.stderr.flush()

                sys.stdout.write("</failure>\n")

            sys.stdout.write("</testcase>\n")

    sys.stdout.write("</testsuite>\n")

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)