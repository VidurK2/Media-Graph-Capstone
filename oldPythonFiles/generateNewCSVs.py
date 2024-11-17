import pandas as pd
from itertools import combinations

# Load your DataFrame
df = pd.read_csv('output.csv')

# Function to parse entities
def parse_entities(entities_str):
    entities = []
    if isinstance(entities_str, str):
        for item in entities_str.split(';'):
            item = item.strip()
            if item:
                if '(' in item and ')' in item:
                    entity_name, entity_type = item.rsplit('(', 1)
                    entity_name = entity_name.strip()
                    entity_type = entity_type.strip(')')
                    entities.append((entity_name, entity_type))
    return entities

# Sets to hold unique entities and relationships
entities_set = set()
relationships_dict = {}

# Process each article
for entities_str in df['Entities']:
    entities = parse_entities(entities_str)
    entities = list(set(entities))  # Remove duplicates in the same article
    entities_set.update(entities)
    
    # Generate all pairs of entities in the article
    for (entity1, type1), (entity2, type2) in combinations(entities, 2):
        key = tuple(sorted([(entity1, type1), (entity2, type2)]))
        relationships_dict[key] = relationships_dict.get(key, 0) + 1

# Create DataFrame for entities
entities_df = pd.DataFrame(list(entities_set), columns=['name', 'type'])
entities_df.to_csv('entities.csv', index=False)

# Create DataFrame for relationships
relationships_list = []
for ((entity1, type1), (entity2, type2)), weight in relationships_dict.items():
    relationships_list.append({
        'entity1': entity1,
        'entity2': entity2,
        'weight': weight
    })

relationships_df = pd.DataFrame(relationships_list)
relationships_df.to_csv('cooccurrences.csv', index=False)
