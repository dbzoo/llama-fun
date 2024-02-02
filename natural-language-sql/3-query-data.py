from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, insert, text
from sqlalchemy.orm import sessionmaker

database_name = 'sql_demo'
connection_string = f"postgresql://postgres:admin@192.168.1.106:5432/{database_name}"

engine = create_engine(connection_string)
metadata_obj = MetaData()

# define city SQL table
table_name = "city_stats"
city_stats_table = Table(
        table_name,
        metadata_obj,
        Column("city_name", String(16), primary_key=True),
        Column("population", Integer),
        Column("country", String(16), nullable=False),
)

# view current table
stmt = select(
        city_stats_table.c.city_name,
        city_stats_table.c.population,
        city_stats_table.c.country,
        ).select_from(city_stats_table)

with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()
        print(results)

# Show how we can execute a raw SQL query, which directly executes over the table.
with engine.connect() as con:
        rows = con.execute(text("SELECT city_name from city_stats"))
        for row in rows:
                print(row)
