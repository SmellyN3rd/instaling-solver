from distutils.core import setup
setup(
  name = 'instaling-solver',         # How you named your package folder (MyLib)
  packages = ['instaling-solver'],   # Chose the same as "name"
  version = '0.01',      # Start with a small number and increase it with every change you make
  license='	gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'instaling-solver is a small project that automates the process of answering instaling.pl questions.',   # Give a short description about your library
  author = 'SmellyN3rd',                   # Type in your name
  author_email = 'milosz.kusz@onet.pl',      # Type in your E-Mail
  url = 'https://github.com/SmellyN3rd/instaling-solver',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/SmellyN3rd/instaling-solver/archive/0.01.tar.gz',    # I explain this later on
  keywords = ['selenium', 'instaling', 'automation', 'bot'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium',
          'geckodriver-autoinstaller'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
