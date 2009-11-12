#! /usr/bin/env python
#
# Copyright (c) 2009 Okoye Chuka D.<okoye9@gmail.com> 
#                    All rights reserved.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  US

from os import system 
import halib.Logger as logger
import halib.chaif.DatabaseDriver as ddriver
import halib.chaif.SanityCheck as scheck
import halib.Exit as exit

#@des:	The sanityCheck method ensure the build environment is sane
#			It checks, operating sys, user as root, sshd root login.		

def sanityCheck():
	logger.subsection("checking to make sure system environment is sane")
	err = scheck.initialize()
	if(len(err) > 0):
		logger.subsection("the following errors resulted from sanity check:")
		for message in err:
			logger.subsection(message)
		logger.subsection("installation cannot continue")
		return 1
	else:
		logger.subsection("yup, system is sane")
		return 0

def databaseSetup():
	logger.subsection("starting mysql services")
	system("/etc/init.d/mysqld restart")
	logger.subsection("initializing database")
	#Create database
	ddriver.create_db()
	logger.subsection("database setup completed sucessfully")
