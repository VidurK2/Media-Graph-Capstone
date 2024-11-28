# import pandas as pd
# import ast  # To safely evaluate string representations of Python literals
# from itertools import combinations

# # Load your DataFrame
# df = pd.read_csv('output_final.csv')

# # Function to parse entities from the string representation of a list of tuples
# def parse_entities(entities_str):
#     try:
#         # Safely evaluate the string to a Python list
#         entities = ast.literal_eval(entities_str)
#         # Ensure that the entities are tuples and properly structured
#         if isinstance(entities, list):
#             return [tuple(entity) for entity in entities if isinstance(entity, tuple) and len(entity) == 2]
#     except (ValueError, SyntaxError):
#         pass
#     return []

# # Sets to hold unique entities and relationships
# entities_set = set()
# relationships_dict = {}

# # Process each article
# for entities_str in df['Resolved Entities']:
#     entities = parse_entities(entities_str)
#     entities = list(set(entities))  # Remove duplicates in the same article
#     entities_set.update(entities)
    
#     # Generate all pairs of entities in the article
#     for (entity1, type1), (entity2, type2) in combinations(entities, 2):
#         key = tuple(sorted([(entity1, type1), (entity2, type2)]))
#         relationships_dict[key] = relationships_dict.get(key, 0) + 1

# # Create DataFrame for entities
# entities_df = pd.DataFrame(list(entities_set), columns=['entity', 'type'])
# entities_df.to_csv('entities.csv', index=False)

# # Create DataFrame for relationships
# relationships_list = []
# for ((entity1, type1), (entity2, type2)), weight in relationships_dict.items():
#     relationships_list.append({
#         'entity1': entity1,
#         'entity2': entity2,
#         'weight': weight,
#         'date': date
#     })

# relationships_df = pd.DataFrame(relationships_list)
# relationships_df.to_csv('cooccurrences.csv', index=False)


import pandas as pd
import ast  # To safely evaluate string representations of Python literals
from itertools import combinations
from datetime import datetime

# Load your DataFrame
df = pd.read_csv('output_final.csv')

# Function to parse entities from the string representation of a list of tuples
def parse_entities(entities_str):
    try:
        # Safely evaluate the string to a Python list
        entities = ast.literal_eval(entities_str)
        # Ensure that the entities are tuples and properly structured
        if isinstance(entities, list):
            return [tuple(entity) for entity in entities if isinstance(entity, tuple) and len(entity) == 2]
    except (ValueError, SyntaxError):
        pass
    return []

# Dictionary to hold relationships with added date information
relationships_dict = {}

# Process each article
for index, row in df.iterrows():
    entities_str = row['Resolved Entities']
    date = row['Date']  # Ensure the 'Date' column exists in your DataFrame
    entities = parse_entities(entities_str)
    entities = list(set(entities))  # Remove duplicates in the same article
    
    # Generate all pairs of entities in the article and record their co-occurrence on that date
    for (entity1, type1), (entity2, type2) in combinations(entities, 2):
        key = tuple(sorted([(entity1, type1), (entity2, type2)]))
        month_year = datetime.strptime(date, '%d-%m-%Y').strftime('%m-%Y')  # Convert date to 'MM-YYYY' format
        if key in relationships_dict:
            relationships_dict[key]['weight'] += 1
            relationships_dict[key]['dates'].add(month_year)
        else:
            relationships_dict[key] = {'weight': 1, 'dates': {month_year}}

# Prepare the list for the DataFrame conversion
relationships_list = []
for ((entity1, type1), (entity2, type2)), info in relationships_dict.items():
    dates = ', '.join(sorted(info['dates']))  # Sort dates and join them into a single string
    relationships_list.append({
        'entity1': entity1,
        'entity2': entity2,
        'weight': info['weight'],
        'dates': dates  # List of all month-year combinations
    })

# Create DataFrame for relationships
relationships_df = pd.DataFrame(relationships_list)
relationships_df.to_csv('cooccurrences_with_dates.csv', index=False)
