from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from sqlalchemy_utils import database_exists, create_database

database_name = 'sql_demo'
connection_string = f"postgresql://postgres:admin@192.168.1.106:5432/{database_name}"

engine = create_engine(connection_string, echo=True, future=True)

if not database_exists(engine.url):
        create_database(engine.url)
        
metadata_obj = MetaData()

# create city SQL table
table_name = "city_stats"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("country", String(20), nullable=False),
)

# Create the table in the PostgreSQL database
metadata_obj.create_all(engine)
