from sqlalchemy import create_engine, inspect

def print_all_table_schemas(database_url):
    # Create an engine
    engine = create_engine(database_url)

    # Create an inspector
    inspector = inspect(engine)

    # Get table names
    table_names = inspector.get_table_names()

    # Loop through tables and print schemas
    for table_name in table_names:
        print_table_schema(engine, table_name)

def print_table_schema(engine, table_name):
    # Create an inspector
    inspector = inspect(engine)

    # Get table columns
    columns = inspector.get_columns(table_name)

    # Print table schema
    print(f"Table: {table_name}")
    for column in columns:
        print(f"\tColumn: {column['name']}\tType: {column['type']}\tNullable: {column['nullable']}")

# Example usage
SQLALCHEMY_DATABASE_URL = "sqlite:///plugin_app.sqlite"
print_all_table_schemas(SQLALCHEMY_DATABASE_URL)
