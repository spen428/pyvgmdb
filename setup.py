from setuptools import setup
from pyvgmdb.pyvgmdb import NAME, VERSION

setup(name=NAME,
      version=VERSION,
      description='Python interface for the VGMdb API.',
      url='https://github.com/spen428/pyvgmdb',
      keywords='vgmdb api anime video game music',
      author='spen428',
      author_email='spen428@users.noreply.github.com',
      packages=['pyvgmdb'],
      install_requires=['requests'])
