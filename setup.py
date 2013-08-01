from distutils.core import setup

import arc.version

setup(name='arc',
      version=arc.version.VERSION,
      description='Autotest RPC Client',
      author='Cleber Rosa',
      author_email='cleber@redhat.com',
      url='http://autotest.github.com',
      packages=['arc',
                'arc.cli',
                'arc.cli.args',
                'arc.cli.actions'],
      data_files=[('/etc/', ['data/arc.conf'])],
      scripts=['scripts/arcli'])
