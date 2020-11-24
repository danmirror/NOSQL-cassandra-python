from cassandra.cluster import Cluster
clstr=Cluster()
session=clstr.connect('castest')
rows=session.execute("select * from students;")
for row in rows:
   print ("StudentID: {} Name:{} Age:{} " .format(row[0],row[1],row[2]))