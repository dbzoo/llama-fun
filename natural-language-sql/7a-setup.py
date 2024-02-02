# Create the emp/dept tables in the scott database
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database

database_name = 'scott'
connection_string = f"postgresql://postgres:admin@192.168.1.106:5432/{database_name}"

engine = create_engine(connection_string, echo=True, future=True)

if not database_exists(engine.url):
        create_database(engine.url)

Base = declarative_base()

class Dept(Base):
    __tablename__ = 'dept'

    deptno = Column(Integer, primary_key=True)
    dname = Column(String(14))
    loc = Column(String(13))
    
    # Define the relationship with the 'emp' table
    employees = relationship('Emp', back_populates='dept')
    
class Emp(Base):
    __tablename__ = 'emp'
    
    empno = Column(Integer, primary_key=True)
    ename = Column(String(10))
    job = Column(String(9))
    mgr = Column(Integer, ForeignKey('emp.empno'))
    hiredate = Column(Date)
    sal = Column(Float(7, 2))
    comm = Column(Float(7, 2))
    deptno = Column(Integer, ForeignKey('dept.deptno'))
    
    # Define the relationship with the 'dept' table
    dept = relationship('Dept', back_populates='employees')

    # Define the self-referential relationship for the manager
    manager = relationship('Emp', remote_side=[empno], back_populates='subordinates')

    # Define the relationship for subordinates
    subordinates = relationship('Emp', back_populates='manager')

Base.metadata.create_all(engine)
dept_data = [
            {'deptno': 10, 'dname': 'Accounting', 'loc': 'New York'},
            {'deptno': 20, 'dname': 'Research', 'loc': 'Dallas'},
            {'deptno': 30, 'dname': 'Sales', 'loc': 'Chicago'},
            {'deptno': 40, 'dname': 'Operations', 'loc': 'Boston'}
        ]
emp_data = [
            {'empno': 7369, 'ename': 'Smith', 'job': 'Clerk', 'mgr': 7902, 'hiredate': '1993-06-13', 'sal': 800.00, 'comm': 0.00, 'deptno': 20},
            {'empno': 7499, 'ename': 'Allen', 'job': 'Salesman', 'mgr': 7698, 'hiredate': '1998-08-15', 'sal': 1600.00, 'comm': 300.00, 'deptno': 30},
            {'empno': 7521, 'ename': 'Ward', 'job': 'Salesman', 'mgr': 7698, 'hiredate': '1996-03-26', 'sal': 1250.00, 'comm': 500.00, 'deptno': 30},
            {'empno': 7566, 'ename': 'Jones', 'job': 'Manager', 'mgr': 7839, 'hiredate': '1995-10-31', 'sal': 2975.00, 'comm': None, 'deptno': 20},
            {'empno': 7698, 'ename': 'Blake', 'job': 'Manager', 'mgr': 7839, 'hiredate': '1992-06-11', 'sal': 2850.00, 'comm': None, 'deptno': 30},
            {'empno': 7782, 'ename': 'Clark', 'job': 'Manager', 'mgr': 7839, 'hiredate': '1993-05-14', 'sal': 2450.00, 'comm': None, 'deptno': 10},
            {'empno': 7788, 'ename': 'Scott', 'job': 'Analyst', 'mgr': 7566, 'hiredate': '1996-03-05', 'sal': 3000.00, 'comm': None, 'deptno': 20},
            {'empno': 7839, 'ename': 'King', 'job': 'President', 'mgr': None, 'hiredate': '1990-06-09', 'sal': 5000.00, 'comm': 0.00, 'deptno': 10},
            {'empno': 7844, 'ename': 'Turner', 'job': 'Salesman', 'mgr': 7698, 'hiredate': '1995-06-04', 'sal': 1500.00, 'comm': 0.00, 'deptno': 30},
            {'empno': 7876, 'ename': 'Adams', 'job': 'Clerk', 'mgr': 7788, 'hiredate': '1999-06-04', 'sal': 1100.00, 'comm': None, 'deptno': 20},
            {'empno': 7900, 'ename': 'James', 'job': 'Clerk', 'mgr': 7698, 'hiredate': '2000-06-23', 'sal': 950.00, 'comm': None, 'deptno': 30},
            {'empno': 7934, 'ename': 'Miller', 'job': 'Clerk', 'mgr': 7782, 'hiredate': '2000-01-21', 'sal': 1300.00, 'comm': None, 'deptno': 10},
            {'empno': 7902, 'ename': 'Ford', 'job': 'Analyst', 'mgr': 7566, 'hiredate': '1997-12-05', 'sal': 3000.00, 'comm': None, 'deptno': 20},
            {'empno': 7654, 'ename': 'Martin', 'job': 'Salesman', 'mgr': 7698, 'hiredate': '1998-12-05', 'sal': 1250.00, 'comm': 1400.00, 'deptno': 30}
        ]
# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Load data into DEPT table
for data in dept_data:
    department = Dept(**data)
    session.add(department)

# Load data into EMP table
for data in emp_data:
    employee = Emp(**data)
    session.add(employee)
    
# Commit the changes
session.commit()
session.close()


