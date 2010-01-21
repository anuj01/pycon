#!/usr/bin/python

# Copyright (C) 2010 Anuj Aggarwal<anuj01@gmail.com>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA."""
#
# Net4India Broadband Connector Ver 0.1
#

from distutils.core import setup
import os, glob

icon_path = os.path.join("share", "icons")
pixmaps_path = os.path.join("share", "pixmaps", "pycon")
menu_path = os.path.join("share", "applications")
doc_path = os.path.join("share", "doc", "pycon")

setup(
    name = "Connector",
    version = "0.1",
    description = "Net4India Broadband Connector",
    long_description = """Net4India Broadband Connector lets you to connect to Net4India \
Broadband server. It has very simple GUI and shows you the session information etc.""",
    author = "Anuj Aggarwal",
    author_email = "anuj01@gmail.com",
    maintainer = "Anuj Aggarwal",
    maintainer_email = "anuj01@gmail.com",
    keywords = ['net4india', 'dialer', 'connector', 'python', 'pygtk'],
    url = "http://anuj01.limewebs.com",
    license = "GPL",
    platforms = "Linux",
    scripts = ['bin/pycon'],
    data_files=[(icon_path, [os.path.join(pixmaps_path, 'pycon.xpm')]),
	    (menu_path, ['data/pycon.desktop']),
            (doc_path, ['README']),
            (pixmaps_path, glob.glob(os.path.join(pixmaps_path, '*.png')))
    ],
    classifiers = [
	    'Development Status :: 5 - Production/Stable',
            'Environment :: X11 Applications :: GTK',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.4',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Topic :: System :: Networking',
            ]

)
