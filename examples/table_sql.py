# pip install sqlalchemy tableschema-sql
import sqlalchemy as sa
from tableschema import Table

# Create SQL database
db = sa.create_engine('sqlite://')

# Data from WEB, schema from MEMORY
SOURCE = 'https://raw.githubusercontent.com/frictionlessdata/tableschema-py/master/data/data_infer.csv'
SCHEMA = {'fields': [{'name': 'id', 'type': 'integer'}, {'name': 'age', 'type': 'integer'}, {'name': 'name', 'type': 'string'}] }

# Open from WEB save to SQL database
table = Table(SOURCE, schema=SCHEMA)
table.save('articles', backend='sql', engine=db)

# Open from SQL save to DRIVE
table = Table('articles', backend='sql', engine=db)
table.schema.save('tmp/articles.json')
table.save('tmp/articles.csv')

# Open from DRIVE print to CONSOLE
table = Table('tmp/articles.csv', schema='tmp/articles.json')
print(table.read(keyed=True))
# Will print
# [{'id': 1, 'age': 39, 'name': 'Paul'}, {'id': 2, 'age': 23, 'name': 'Jimmy'}, {'id': 3, 'age': 36, 'name': 'Jane'}, {'id': 4, 'age': 28, 'name': 'Judy'}]
