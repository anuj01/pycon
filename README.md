# Introduction

   Connector is a network dialer frontend for Net4India Broadband Internet.

   Connector is developed in the Python programming language, and its
   interface is built with the GTK Toolkit. 

# Installation
  
   The Connector's source package are provided in such a way that, if you have
   all the required software, it will run 'out-of-the-tarball'.

   The list of required software follows:

     [1] Python 2.6 or higher

     [2] GTK+ 2.6 or higher

     [3] PyGTK 2.6 or higher


   After unpacking the source distribution do one of the following:
     * Double click the pycon file
     * Call the Python interpreter on the pycon.py file

   Unpack the source package, and get inside the extracted directory.

   * Extracting  gziped tarball

   $ tar xvzf Connector-0.1.tar.gz

   * Extracting bziped tarball

   $ tar xvjf Connector-0.1.tar.bz2

   * Extracting ziped source

   $ unzip Connector-0.1.zip

   After extracting the sources, get inside the extracted dir:
   
   $ cd Connector-0.1

   And then, run the command bellow as root:

   \# python setup.py install


   This should be enough to get Connector installed.
   To run Connector:

   $ ./bin/pycon


   If you want to define the path where Connector should be installed, do:

   $ python setup.py install --prefix /path/to/connector_dir

   After that, put the /path/to/connector_dir/bin directory created in your PATH:

   $ export PATH=$PATH:/path/to/connector_dir/bin

   Or, put line above inside your ~/.bash_profile, ~/.bashrc or ~/.profile
   (depending on your system) and this will get executed everytime you login.
   After putting the bin directory in the PATH, execute Umit:

   $ pycon

# Build 'rpm' package for your Distribution 
   
   Unpack the source package, and get inside the extracted directory.

   * Extracting  gziped tarball

   $ tar xvzf Connector-0.1.tar.gz

   * Extracting bziped tarball

   $ tar xvjf Connector-0.1.tar.bz2

   * Extracting ziped source

   $ unzip Connector-0.1.zip

   After extracting the sources, get inside the extracted dir:

   $ cd Connector-0.1

   And then, run the command below :

   $ python setup.py bdist_rpm

   Connector-0.1-1.noarch.rpm and Connector-0.1-1.src.rpm packages will be 
   created in dist/

   Now, just install the rpm package as a root :

   \# cd dist/

   \# rpm -ivh Connector-0.1-1.noarch.rpm

   
