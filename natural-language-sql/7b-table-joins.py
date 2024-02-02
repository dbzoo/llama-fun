from sqlalchemy import create_engine
from llama_index.indices.struct_store.sql_query import (
        SQLTableRetrieverQueryEngine,
    )
from llama_index import (
    set_global_tokenizer,
    SQLDatabase,
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context,
    MockEmbedding
    )
from llama_index.llms import Ollama
from llama_index.objects import (
        SQLTableNodeMapping,
        ObjectIndex,
        SQLTableSchema,
    )
from transformers import AutoTokenizer

EMBED_DIM=384
ollama = Ollama(model="starling-lm", request_timeout=30.0)
set_global_tokenizer(AutoTokenizer.from_pretrained("openchat/openchat_3.5").encode)

service_context = ServiceContext.from_defaults(llm=ollama, embed_model=MockEmbedding(embed_dim=EMBED_DIM))
# Instead of providing a service context when loading the index from storage use a global.
set_global_service_context( service_context )

database_name = 'scott'
connection_string = f"postgresql://postgres:admin@192.168.1.106:5432/{database_name}"

engine = create_engine(connection_string)
sql_database = SQLDatabase(engine, include_tables=["emp","dept"])

emp_description = """The emp table stores information about employees in an
organization. Each record in this table represents an individual
employee, and the columns provide details about their employment,
roles, and relationships within the organization.

Columns:
- empno: Employee number, a unique identifier for each employee.
- ename: Employee name, specifying the name of the employee.
- job: Job role, indicating the position or title of the employee.
- mgr: Manager's employee number, showing the identification of the employee's manager.
- hiredate: Hire date, specifying the date when the employee was hired.
- sal: Salary, denoting the monetary compensation received by the employee.
- comm: Commission, representing any additional commission received by the employee.
- deptno: Department number, indicating the department to which the employee belongs.
"""

dept_description = """The dept table represents information about different
departments within an organization. Each row contains details about a
specific department, including the department number, department name,
and the location of the department.

Columns:
- deptno: Department number, a unique identifier for each department.
- dname: Department name, specifying the name of the department.
- loc: Location, indicating the physical location or city where the department is situated.
"""

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
        (SQLTableSchema(table_name="emp", context_str=emp_description)),
        (SQLTableSchema(table_name="dept", context_str=dept_description))
    ]
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
query_engine = SQLTableRetrieverQueryEngine(
        sql_database, obj_index.as_retriever(similarity_top_k=1)
    )

query_str = "How many employees work in the New York location"
print(query_str)
response = query_engine.query(query_str)
sql = response.metadata["sql_query"]
print(f"\nExecuted {sql}\n")
print(response)
