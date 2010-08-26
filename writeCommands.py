# netfilterManager
#Copyright (C) 2010  Antoine Benkemoun
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configuration
import sqlite3 as sqlite

def writeIptablesRule(hostname,line,rule):

    # If line number not specified (=0), default to last line (200)
    if line == 0:
        line = 200

    # Connecting to SQLite DB
    connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
    cursor = connection.cursor()

    # Get the ID of the host
    cursor.execute("SELECT id FROM host WHERE name=?;", [hostname])
    id = str(cursor.fetchone()[0])

    substitution = [ line, id, rule]

    # Writing to DB
    cursor.execute("INSERT INTO rules (line, host_id, rule) VALUES (?,?,?);",substitution)

    # Commit and close
    connection.commit()
    cursor.close()
