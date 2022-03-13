from distutils.core import setup

setup(
  name = 'instaling-solver',
  packages = ['instaling-solver'],
  version = '1.00',
  license='	gpl-3.0',
  description = 'instaling-solver is a small project that automates the process of answering instaling.pl questions.',
  author = 'SmellyN3rd',
  author_email = 'milosz@miloszkusz.pl',
  url = 'https://github.com/SmellyN3rd/instaling-solver',
  download_url = 'https://github.com/SmellyN3rd/instaling-solver/archive/1.00.tar.gz',
  keywords = ['selenium', 'instaling', 'automation', 'bot'],
  install_requires=[
          'selenium'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
  ],
)
