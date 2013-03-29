# -*- coding: utf-8 -*-
"""Recipe rsync"""

import logging
import sys
import subprocess
from pkg_resources import working_set
from sys import executable
from zc.buildout.easy_install import scripts as create_script

_LOG = logging.getLogger("rsync")
line = ('-----------------------------------' +
        '-----------------------------------')

def rsync(source=None, target=None, port=None, rsync_opt=None):
    cmd = ['rsync']
    if port:
        cmd.extend(['-e', 'ssh -p %s' % port])
        for opts in rsync_opt.split():
            cmd.append(opts)
        cmd.extend([source, target])
        print cmd
    else:
        for opts in rsync_opt.split():
            cmd.append(opts)
        cmd.extend([source, target])

    _LOG.info(line)
    _LOG.info('Running rsync with command: ')
    _LOG.info('  $ %s' % ' '.join(cmd))
    _LOG.info('  Note: depending on the source file(s) size and location, this may take a while!')
    _LOG.info(line)
    subprocess.call(cmd)
    _LOG.info('Done.')

#def rsync(source=None, target=None, port=None, rsync_opt=None):
#    cmd = ["rsync","--verbose --archive","./test_rsync


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.source = options['source']
        self.target = options['target']
        self.rsync_opt = "--verbose --archive --partial --progress"
        self.port = None
        self.script = False
        if 'rsync_opt' in options:
            self.rsync_opt = options['rsync_opt']
        if 'port' in options:
            self.port = options['port']
        if 'script' in options:
            if options['script'] == 'true':
                self.script = True


    def install(self):
        """Installer"""
        if self.script:
            bindir = self.buildout['buildout']['bin-directory']
            arguments = "source='%s', target='%s', port='%s'"
            create_script(
                [('%s' % self.name, 'collective.recipe.rsync.__init__', 'rsync')],
                working_set, executable, bindir, arguments=arguments % (
                self.source, self.target, self.port))
            return tuple((bindir + '/' + 'rsync',))
        else:
            # if we make it this far, script option is not set so we execute
            # as buildout runs
            rsync(source=self.source, rsync_opt=self.rsync_opt, target=self.target, port=self.port)
            return tuple()

    def update(self):
        """Updater"""
        self.install()
