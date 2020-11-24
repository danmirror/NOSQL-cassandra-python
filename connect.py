from cassandra.cluster import Cluster
clstr=Cluster(['localhost'])
session=clstr.connect('castest')

