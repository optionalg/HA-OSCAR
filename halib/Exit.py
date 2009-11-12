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
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import halib.Logger as logger
import sys

#@des:   This function should be called when we want to end installation
#        It might be as a result of an error or normal termination 

def open(message=None):
   if message is None:
      os.chdir(os.getenv("HAS_HOME"))
      logger.subsection("Finished installation")
      os.system("rm -rf .has_lock_file")
   else:
      logger.subsection("Your installation failed with message:")
      logger.subsection(message)
      os.chdir(os.getenv("HAS_HOME"))
      os.system("rm -rf .has_lock_file")
   sys.exit(0)


