# coding:utf-8

"""
    Info print
    ~~~~~~~~~~
    
    Insert in every stdout.write() a info line from witch code line this print comes.
    Usefull to find debug print statements ;)
    
    WARNING: This is very slow and should only be used with the developer server ;)
    
    Simply put this two lines in your settings:
        ---------------------------------------------------------------------- 
        from django_tools.utils import info_print
        info_print.redirect_stdout()
        ----------------------------------------------------------------------
    
    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate$
    $Rev$
    $Author:$

    :copyleft: 2009 by the django-tools team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import sys
import inspect
import warnings

MAX_FILEPATH_LEN = 66



class InfoStdout(object):
    """ Insert in every stdout.write() a info line from witch code line this print comes."""
    def __init__(self, orig_stdout):
        self.orig_stdout = orig_stdout

    def write(self, txt):
        self.orig_stdout.write("\n%s:\n%s" % (self._get_fileinfo(), txt))

    def _get_fileinfo(self):
        """ return fileinfo: Where from the announcement comes? """
        try:
            self_basename = os.path.basename(__file__)
            if self_basename.endswith(".pyc"):
                # cut: ".pyc" -> ".py"
                self_basename = self_basename[:-1]

            for stack_frame in inspect.stack():
                # go forward in the stack, to outside of this file.
                filename = stack_frame[1]
                lineno = stack_frame[2]
                if os.path.basename(filename) != self_basename:
                    break

            if len(filename) >= MAX_FILEPATH_LEN:
                filename = "...%s" % filename[-MAX_FILEPATH_LEN:]
            fileinfo = "%s line %s" % (filename, lineno)
        except Exception, e:
            fileinfo = "(inspect Error: %s)" % e

        return fileinfo



__redirected = False

def redirect_stdout():
    global __redirected

    if not __redirected:
        __redirected = True
        try:
            warnings.warn("Redirect stdout/stderr for info print!")
            orig_stdout = sys.stdout
            sys.stdout = InfoStdout(orig_stdout)
            orig_stderr = sys.stderr
            sys.stderr = InfoStdout(orig_stdout)
        except Exception, err:
            print "Error:", err
