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
                'arc.cli.actions'],
      data_files=[('/etc/', ['data/arc.conf'])],
      cmdclass={'build_doc': BuildDoc},
      command_options={'build_doc': {'source_dir':
                                     ('setup.py', 'docs/source')}},
      scripts=['scripts/arcli'])
