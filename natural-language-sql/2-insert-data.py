from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, insert
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
        Column("country", String(20), nullable=False),
)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert some data
rows = [
            {"city_name": "Paris", "population": 2148000, "country": "France"},
            {"city_name": "Sydney", "population": 5312000, "country": "Australia"},
            {"city_name": "Mumbai", "population": 12480000, "country": "India"},
            {"city_name": "Berlin", "population": 3769000, "country": "Germany"},
            {"city_name": "Rio de Janeiro", "population": 6748000, "country": "Brazil"},
            {"city_name": "Moscow", "population": 12615000, "country": "Russia"},
            {"city_name": "Cairo", "population": 20080000, "country": "Egypt"},
            {"city_name": "Johannesburg", "population": 5070000, "country": "South Africa"},
            {"city_name": "Dubai", "population": 3137000, "country": "United Arab Emirates"},
            {"city_name": "Mexico City", "population": 8919000, "country": "Mexico"},
            {"city_name": "Bangkok", "population": 10530000, "country": "Thailand"},
            {"city_name": "Oslo", "population": 1557000, "country": "Norway"},
            {"city_name": "Istanbul", "population": 15460000, "country": "Turkey"},
            {"city_name": "Lima", "population": 9748000, "country": "Peru"},
            {"city_name": "Auckland", "population": 1730000, "country": "New Zealand"},
            {"city_name": "Stockholm", "population": 975900, "country": "Sweden"},
            {"city_name": "Buenos Aires", "population": 3054000, "country": "Argentina"},
            {"city_name": "Shanghai", "population": 27440000, "country": "China"},
            {"city_name": "Toronto", "population": 2930000, "country": "Canada"},
            {"city_name": "Tokyo", "population": 13960000, "country": "Japan"},
        ]

for row in rows:
        stmt = insert(city_stats_table).values(**row)
        session.execute(stmt)
        session.commit()
