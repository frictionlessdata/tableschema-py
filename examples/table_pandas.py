# pip install jsontableschema-pandas
from pprint import pprint
from jsontableschema import Table

# Data source
SOURCE = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/data/data_infer.csv'

# Data processor
def skip_under_30(erows):
    for number, headers, row in erows:
        krow = dict(zip(headers, row))
        if krow['age'] >= 30:
            yield (number, headers, row)

# Export to pandas
table = Table(SOURCE, post_convert=[skip_under_30])
storage = table.save('persons', backend='pandas')
pprint(storage['persons'])
# Will print (if use skip_under_30 filter)
# id age name
# 1  39  Paul
# 3  36  Jane
