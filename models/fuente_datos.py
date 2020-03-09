# -*- coding: utf-8 -*-

import psycopg2
from sshtunnel import SSHTunnelForwarder

# for ide
if False:
    from db import configuration

# For interactive work (on ipython) it's easier to work with explicit objects
# instead of contexts.
# Create an SSH tunnel
def test_tunel():
    tunnel = SSHTunnelForwarder(
        (configuration.get('datos.ssh_host'),
         configuration.get('datos.ssh_port')),
        ssh_username=configuration.get('datos.ssh_user'),
        ssh_password = configuration.get('datos.ssh_pass'),
        remote_bind_address=('localhost', 5432),
        local_bind_address=('localhost',6543), # could be any available port
        )
    # Start the tunnel
    tunnel.start()
    # Create a database connection
    conn = psycopg2.connect(
        database='<database>',
        user='<db_user>',
        host=tunnel.local_bind_host,
        port=tunnel.local_bind_port,
    )
    # Get a database cursor
    cur = conn.cursor()
    # Execute SQL
    cur.execute("""SQL-Statements;""")
    # Get the result
    result = cur.fetchall()
    print(result)
    # Close connections
    conn.close()
    # Stop the tunnel
    tunnel.stop()

# en appconfig.ini
# [datos]
# ssh_host = 
# ssh_port = 
# ssh_user = 
# ssh_pass = 