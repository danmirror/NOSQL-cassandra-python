
import logging
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
from cassandra.query import SimpleStatement


class PythonCassandraExample:

    def __init__(self):
        self.cluster = None
        self.session = None
        self.keyspace = None
        self.log = None

    def __del__(self):
        self.cluster.shutdown()

    def createsession(self):
        self.cluster = Cluster(['localhost'])
        self.session = self.cluster.connect(self.keyspace)

    def getsession(self):
        return self.session

    # How about Adding some log info to see what went wrong
    def setlogger(self):
        log = logging.getLogger()
        log.setLevel('INFO')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        log.addHandler(handler)
        self.log = log

    # Create Keyspace based on Given Name
    def createkeyspace(self, keyspace):
        """
        :param keyspace:  The Name of Keyspace to be created
        :return:
        """
        # Before we create new lets check if exiting keyspace; we will drop that and create new
        rows = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if keyspace in [row[0] for row in rows]:
            self.log.info("dropping existing keyspace...")
            self.session.execute("DROP KEYSPACE " + keyspace)

        self.log.info("creating keyspace...")
        self.session.execute("""
                CREATE KEYSPACE %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % keyspace)

        self.log.info("setting keyspace...")
        self.session.set_keyspace(keyspace)

    def create_table(self):
        c_sql = """
                CREATE TABLE IF NOT EXISTS employee (emp_id int PRIMARY KEY,
                                              ename varchar,
                                              sal double,
                                              city varchar);
                 """
        self.session.execute(c_sql)
        self.log.info("Employee Table Created !!!")

    # lets do some batch insert
    def insert_data(self):
        insert_sql = self.session.prepare("INSERT INTO  employee (emp_id, ename , sal,city) VALUES (?,?,?,?)")
        batch = BatchStatement()
        batch.add(insert_sql, (1, 'LyubovK', 2555, 'Dubai'))
        batch.add(insert_sql, (2, 'JiriK', 5660, 'Toronto'))
        batch.add(insert_sql, (3, 'IvanH', 2547, 'Mumbai'))
        batch.add(insert_sql, (4, 'YuliaT', 2547, 'Seattle'))
        self.session.execute(batch)
        self.log.info('Batch Insert Completed')

    def select_data(self):
        rows = self.session.execute('select * from employee limit 5;')
        for row in rows:
            print(row.ename, row.sal)

    def update_data(self):
        pass

    def delete_data(self):
        pass


if __name__ == '__main__':
    example1 = PythonCassandraExample()
    example1.createsession()
    example1.setlogger()
    example1.createkeyspace('castes2')
    example1.create_table()
    example1.insert_data()
    example1.select_data()