import sqlite3
import json
import os
from src.params.globals import opts_db


def init_db(db_name=opts_db):
    if os.path.exists(db_name):
        os.remove(db_name)
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the necessary tables
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabs (
            tab_id TEXT PRIMARY KEY,
            tab_name TEXT,
            app_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS components (
            component_id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_type TEXT,
            component_type TEXT,
            attributes TEXT,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES components (component_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS component_values (
            value_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tab_id TEXT,
            component_id INTEGER,
            value TEXT,
            FOREIGN KEY (tab_id) REFERENCES tabs (tab_id),
            FOREIGN KEY (component_id) REFERENCES components (component_id),
            UNIQUE (tab_id, component_id)
        )
    ''')

    conn.commit()
    conn.close()



# Connect to SQLite database
#init_db()
#conn = sqlite3.connect(opts_db)
#cursor = conn.cursor()

# Function to insert a new tab into the `tabs` table
def insert_tab(tab_id, tab_name, app_type):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO tabs (tab_id, tab_name, app_type) 
        VALUES (?, ?, ?)
    ''', (tab_id, tab_name, app_type))
    conn.commit()
    conn.close() 

# Function to insert a new component into the `components` table
def insert_component(app_type, component_type, attributes, parent_id=None):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO components (app_type, component_type, attributes, parent_id)
        VALUES (?, ?, ?, ?)
    ''', (app_type, component_type, json.dumps(attributes), parent_id))
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Function to insert or update a tab's component value in the `component_values` table
def insert_component_value(tab_id, component_id, value):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO component_values (tab_id, component_id, value)
        VALUES (?, ?, ?)
        ON CONFLICT(tab_id, component_id) DO UPDATE SET value=excluded.value
    ''', (tab_id, component_id, value))
    conn.commit()
    conn.close()

# Recursively parse `left_content` and insert into the database
def parse_and_insert_content(tab_id, content, app_type='synteny', parent_id=None):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()
    if isinstance(content, list):
        for item in content:
            parse_and_insert_content(tab_id, item, app_type, parent_id)
    elif isinstance(content, dict):
        component_type = content.get('type', None)
        props = content.get('props', {})
        children = props.get('children', None)

        # Extract the value (if applicable)
        value = props.get('value') or props.get('filename') or props.get('n_clicks')

        # Prepare attributes for storing (without children)
        attributes = {k: v for k, v in props.items() if k != 'children'}

        # Insert the component and get its ID
        component_id = insert_component(app_type, component_type, attributes, parent_id)

        # Insert the value (if applicable) into the `component_values` table
        if value is not None:
            insert_component_value(tab_id, component_id, value)

        # Recursively parse children components
        if children:
            parse_and_insert_content(tab_id, children, app_type, component_id)
    conn.close()

# Function to update or add attributes to a component
def update_or_add_attribute(tab_id, component_id_key, component_id_value, attribute_name, attribute_value):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()

    # Dynamic query to handle both cases: when `id` is a string or a dictionary
    if component_id_key == 'id':
        if isinstance(component_id_value, str):
            # Handle string 'id'
            cursor.execute('''
                SELECT component_id, attributes
                FROM components
                WHERE json_extract(attributes, '$.id') = ? AND json_extract(attributes, '$.tab') = ?
            ''', (component_id_value, tab_id))
        elif isinstance(component_id_value, dict):
            # Handle dictionary 'id'
            query_conditions = ' AND '.join(
                f"json_extract(attributes, '$.id.{k}') = ?" for k in component_id_value.keys()
            )
            query_values = list(component_id_value.values())
            cursor.execute(f'''
                SELECT component_id, attributes
                FROM components
                WHERE {query_conditions}
            ''', query_values)
    
    record = cursor.fetchone()

    if record is None:
        print(f"No component found with id: {component_id_value} in tab: {tab_id}")
        return

    component_id, attributes_json = record
    attributes = json.loads(attributes_json)

    # Debug: Print the current attributes before updating
#    print(f"Current attributes before updating for {component_id_value}: {attributes}")

    # Update or add the attribute
    attributes[attribute_name] = attribute_value

    # Update the attributes in the database
    cursor.execute('''
        UPDATE components
        SET attributes = ?
        WHERE component_id = ?
    ''', (json.dumps(attributes), component_id))

    conn.commit()
    conn.close()

    # Debug: Print a message confirming the update
#    print(f"Attribute '{attribute_name}' updated/added successfully in component '{component_id_value}'")


def retrieve_component_attributes(tab_id, component_id_key, component_id_value):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()

    # Dynamic query to handle both cases: when `id` is a string or a dictionary
    if component_id_key == 'id':
        if isinstance(component_id_value, str):
            # Handle string 'id'
            cursor.execute('''
                SELECT component_id, attributes
                FROM components
                WHERE json_extract(attributes, '$.id') = ? AND json_extract(attributes, '$.tab') = ?
            ''', (component_id_value, tab_id))
        elif isinstance(component_id_value, dict):
            # Handle dictionary 'id'
            query_conditions = ' AND '.join(
                f"json_extract(attributes, '$.id.{k}') = ?" for k in component_id_value.keys()
            )
            query_values = list(component_id_value.values())
            cursor.execute(f'''
                SELECT component_id, attributes
                FROM components
                WHERE {query_conditions}
            ''', query_values)
    
    record = cursor.fetchone()

    conn.close()

    if record is None:
        print(f"No component found with id: {component_id_value} in tab: {tab_id}")
        return {}

    component_id, attributes_json = record
    attributes = json.loads(attributes_json)

#    # Debug: Print the retrieved attributes
#    print(f"Retrieved attributes for {component_id_value}: {attributes}")

    return attributes


def update_template_with_attributes(template_json, tab_id):
    conn = sqlite3.connect(opts_db)
    cursor = conn.cursor()
    # Recursively update the template based on the component's id and attributes in the database
    def update_component_attributes(component, tab_id):
        # Check if the component has an 'id' in its props
        if 'props' in component and 'id' in component['props']:
            component_id = component['props']['id']
            
            # Check if the component's id is a dictionary (e.g., {'id': 'synteny-inputs', 'tab': 'synteny_1'})
            if isinstance(component_id, dict) and 'id' in component_id and 'tab' in component_id:
                # Retrieve attributes from the database
                retrieved_attributes = retrieve_component_attributes(tab_id, 'id', component_id)

                # If we found attributes, update the component's props
                if retrieved_attributes:
                    component['props'].update(retrieved_attributes)

        # Recursively update children if they exist
        if 'props' in component and 'children' in component['props']:
            children = component['props']['children']
            if isinstance(children, list):
                # Update each child component
                for child in children:
                    update_component_attributes(child, tab_id)
            elif isinstance(children, dict):
                # Update the single child component
                update_component_attributes(children, tab_id)

    # Iterate through the top-level components in the template JSON
    for component in template_json:
        update_component_attributes(component, tab_id)

    conn.close()
    return template_json



##### USAGE EXAMPLE ######


# Example: Sample opts_content
#with open('synteny.opts', 'r') as file:
#    opts_content = json.load(file)

# Example: Insert the tab and the components into the database
#insert_tab('synteny_1', 'Synteny Tab 1', 'synteny')
#parse_and_insert_content('synteny_1', opts_content)

# Example: Update the component's 'options' attribute
#update_or_add_attribute(
#    tab_id='synteny_1', 
#    component_id_key='id', 
#    component_id_value={'id': 'synteny-inputs', 'tab': 'synteny_1'}, 
#    attribute_name='options', 
#    attribute_value=['one', 'two', 'three']
#)

# Example: Update the component's 'value' attribute
#update_or_add_attribute(
#    tab_id='synteny_1', 
#    component_id_key='id', 
#    component_id_value={'id': 'synteny-inputs', 'tab': 'synteny_1'}, 
#    attribute_name='value', 
#    attribute_value='one'
#)

# Example: Print all componnets (separated)
#cursor.execute("SELECT attributes FROM components")
#records = cursor.fetchall()
#for record in records:
#    print(record)


# Example: Retrive attributes for a given component
#component_data = retrieve_component_attributes(
#    tab_id='synteny_1', 
#    component_id_key='id', 
#    component_id_value={'id': 'synteny-inputs', 'tab': 'synteny_1'}
#)
#print("Component Data:", json.dumps(component_data, indent=2))



# Example: Retrieve the JSON structure for 'synteny_1'
#json_structure = update_template_with_attributes(opts_content, 'synteny_1')
#print(json_structure)

# Close the connection
#conn.close()