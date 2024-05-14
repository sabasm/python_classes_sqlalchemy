from collections import namedtuple

# Use namedtuple for organizing database table names, making them accessible via attribute-style access
TableNames = namedtuple('TableNames', ['toy', 'owner', 'animal'])
DATABASE_TABLES = TableNames(toy='toys', owner='owners', animal='animals')

# Use namedtuple for organizing foreign key references, improving clarity and maintainability
ForeignKeys = namedtuple('ForeignKeys', ['favorite_toy_id', 'owner_id'])
FOREIGN_KEYS = ForeignKeys(
    favorite_toy_id=f"{DATABASE_TABLES.toy}.id",
    owner_id=f"{DATABASE_TABLES.owner}.id"
)

# Use namedtuple for organizing class names used in relationships, providing clear reference points
ClassNames = namedtuple('ClassNames', ['toy', 'owner', 'animal'])
CLASSES = ClassNames(toy='Toy', owner='Owner', animal='Animal')
