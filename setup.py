# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2013-2014 Red Hat
# Author: Cleber Rosa <cleber@redhat.com>

# pylint: disable=E0611
from distutils.core import setup
from sphinx.setup_command import BuildDoc

import arc.version

setup(name='arc',
      version=arc.version.VERSION,
      description='Autotest RPC Client',
      author='Cleber Rosa',
      author_email='cleber@redhat.com',
      url='http://autotest.github.com',
      requires=['pygments'],
      packages=['arc',
                'arc.cli',
                'arc.cli.args',
                'arc.cli.actions',
                'arc.shared',
                'arc.tko'],
      data_files=[('/etc/', ['data/arc.conf'])],
      cmdclass={'build_doc': BuildDoc},
      command_options={'build_doc': {'source_dir':
                                     ('setup.py', 'docs/source')}},
      scripts=['scripts/arcli'])
