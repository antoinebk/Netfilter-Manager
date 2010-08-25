#! /usr/bin/python

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
