# python-baySerial
BaySerial implementation for Python

## Installation
You can either use the setup.py script or a Linux binary to install the package.

### Setup.py
Do the following steps to install the package via the setup.py script:
- git clone request ```git clone git://github.com/BayCEER/python-baySerial.git```
- find the right directory ```cd python-baySerial```
- run ```python setup.py install``` as root

### Linux Binary (for Debian)
- add the following repositories to /etc/apt/sources.list ```deb http://www.bayceer.uni-bayreuth.de/repos/apt/debian squeeze main```
- install key ```wget -O - http://www.bayceer.uni-bayreuth.de/repos/apt/conf/bayceer_repo.gpg.key | apt-key add -```
- ```apt-get update```
- ```apt-get install python-baySerial```

Alternatively:
- run ```dpkg -i python-baySerial_*_all.deb``` as root

## Usage
See examples for usage.
