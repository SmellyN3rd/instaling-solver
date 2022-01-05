from distutils.core import setup

setup(
  name = 'instaling-solver',
  packages = ['instaling-solver'],
  version = '0.05',
  license='	gpl-3.0',
  description = 'instaling-solver is a small project that automates the process of answering instaling.pl questions.',
  author = 'SmellyN3rd',
  author_email = 'milosz@miloszkusz.pl',
  url = 'https://github.com/SmellyN3rd/instaling-solver',
  download_url = 'https://github.com/SmellyN3rd/instaling-solver/archive/0.05.tar.gz',
  keywords = ['selenium', 'instaling', 'automation', 'bot'],
  install_requires=[
          'selenium',
          'geckodriver-autoinstaller'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
  ],
)
