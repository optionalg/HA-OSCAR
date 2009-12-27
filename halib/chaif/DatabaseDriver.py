#! /usr/bin/env python
#
# Copyright (c) 2009 Himanshu Chhetri <himanshuchhetri@gmail.com> 
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


from os import path, unlink
from sys import exit
import sqlite3
import halib.Logger as logger

class DbDriver:

  def __init__(self, default_db_path = "/usr/share/haoscar/hadb", default_schema_path="/usr/share/haoscar/schema.sql"):
    self.db_path = default_db_path
    self.schema_path = default_schema_path

  def create_database(self):
    # Delete sqlite database file if it already exists
    try:
      unlink(self.db_path)
    except OSError:
      pass

    if not path.exists(self.schema_path):
      logger.subsection("Cannot access database schema file")
      exit(2)

    # Create database creation query from schema file
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = ""
    f = open(self.schema_path)
    for line in f:
      query += line
    try:
      c.executescript(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :") 
      logger.subsection(query)
      exit(2)
    conn.commit()
    c.close()

# Returns list of tables in database as a list
  def get_tables(self):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database file at "+ self.db_path)
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = "select name from sqlite_master where type='table'"

    try:
      c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :")
      logger.subsection(query)
      exit(2)
    result = []
    for row in c:
      result.append(row[0])  
    c.close()
    return result


# Returns table in the form of a dictionary
# TODO : Fix select_db bug
  def select_db(self, table):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database file at "+ self.db_path)
      exit(2)
    
    existing_tables = []
    existing_tables = self.get_tables()
    if table not in existing_tables:
      logger.subsection(table + " does not exist in database")
      exit(2)

    if type(table)!=str:
      logger.subsection(table + " must of type String")
      exit(2)

    conn = sqlite3.connect(self.db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = "SELECT * from "
    query += table

    try:
      c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :") 
      logger.subsection(query)
      exit(2)

    r = c.fetchone()
    columns = r.keys()
    result = {}
    n = 0
    for row in c:
      result[columns[n]] = row[1]
      #result[row[0]] = row[1]
      n += 1
    c.close()
    #return result
    return row

   
  # Insert given list into given table of database
  def insert_db(self, table, get_dict):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database")
      exit(2)

    existing_tables = []
    existing_tables = self.get_tables()
    if table not in existing_tables:
      logger.subsection(table+ " does not exist in database")
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    
    query = "INSERT INTO "+table+" ("
    for key in get_dict.keys():
       query += key            
       query += ","
    query = query.rstrip(',')
    query += ") VALUES ("
    for key in get_dict.keys():
      query += "'"
      query += get_dict[key]
      query += "'"
      query += ","
    query = query.rstrip(',')
    query += ")"

    try:
       c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :") 
      logger.subsection(query)
      exit(2)
    conn.commit()
    c.close()
