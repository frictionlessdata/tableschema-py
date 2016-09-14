# pip install sqlalchemy jsontableschema-sql
import sqlalchemy as sa
from pprint import pprint
from jsontableschema import Table

# Data source
SOURCE = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/data/data_infer.csv'

# Create SQL database
db = sa.create_engine('sqlite://')

# Data processor
def skip_under_30(erows):
    for number, headers, row in erows:
        krow = dict(zip(headers, row))
        if krow['age'] >= 30:
            yield (number, headers, row)

# Work with table
table = Table(SOURCE, post_cast=[skip_under_30])
table.schema.save('tmp/persons.json') # Save INFERRED schema
table.save('persons', backend='sql', engine=db) # Save data to SQL
table.save('tmp/persons.csv')  # Save data to DRIVE

# Check the result
pprint(Table('persons', backend='sql', engine=db).read(keyed=True))
pprint(Table('tmp/persons.csv').read(keyed=True))
# Will print (twice)
# [{'age': 39, 'id': 1, 'name': 'Paul'},
#  {'age': 36, 'id': 3, 'name': 'Jane'}]
