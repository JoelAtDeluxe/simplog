from distutils.core import setup

with open('README.md', 'r') as fh:
  long_description=fh.read()

setup(
  name = 'simplog',
  packages = ['simplog'],
  version = '0.1.0',
  license='MIT',
  description = 'A simple, functional, opinionated logger for python',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = 'Joel Smith',
  author_email = 'joel.pypi@gmail.com',
  url = 'https://github.com/JoelAtDeluxe/simplog',
  download_url = 'https://github.com/JoelAtDeluxe/simplog/archive/v0.1.0.tar.gz', 
  keywords = ['logging', 'functional', 'splunk'],
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'Development Status :: 4 - Beta',
    "Operating System :: OS Independent",
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',    
  ],
)