from cassandra.cluster import Cluster
clstr=Cluster()
session=clstr.connect('castest')
session.execute("insert into students (studentID, name, age, marks) values  (1, 'Juli',20, 200);")