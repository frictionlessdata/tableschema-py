from jsontableschema import Table

# Data from WEB, schema from MEMORY
SOURCE = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/data/data_infer.csv'
SCHEMA = {'fields': [{'name': 'id', 'type': 'integer'}, {'name': 'age', 'type': 'integer'}, {'name': 'name', 'type': 'string'}] }

# If schema is not passed it will be inferred
table = Table(SOURCE, schema=SCHEMA)
rows = table.iter()
while True:
    try:
        print(next(rows))
    except StopIteration:
        break
    except Exception as exception:
        print(exception)
