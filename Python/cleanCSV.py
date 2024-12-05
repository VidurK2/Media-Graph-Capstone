import pandas as pd

def clean_csv_automatically(input_file, output_file):
    # Load the CSV into a DataFrame
    df = pd.read_csv(input_file)
    
    # Normalize the 'entity' column for case-insensitive duplicate checking
    df['entity_normalized'] = df['entity'].str.lower()
    
    # Drop duplicates based on the normalized entity column, keeping the first occurrence
    cleaned_df = df.drop_duplicates(subset='entity_normalized').drop(columns=['entity_normalized'])
    
    # Report results
    total_duplicates = len(df) - len(cleaned_df)
    print(f"Total rows removed: {total_duplicates}")
    print(f"Remaining rows: {len(cleaned_df)}")
    
    # Save the cleaned data to a new CSV
    cleaned_df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

# Usage example
input_csv = "/home/vidur/mediagraph/data/entities2020.csv"  # Replace with your input CSV file path
output_csv = "/home/vidur/mediagraph/data/cleaned_entities2020.csv"  # Replace with your desired output CSV file path

clean_csv_automatically(input_csv, output_csv)

#---

import pandas as pd

def clean_cooccurrence(cooccurrence_file, cleaned_entities_file, output_file):
    # Load the cleaned entities and co-occurrence files
    cleaned_entities_df = pd.read_csv(cleaned_entities_file)
    cooccurrence_df = pd.read_csv(cooccurrence_file)
    
    # Create a set of valid entities from the cleaned entities file
    valid_entities = set(cleaned_entities_df['entity'].str.lower())  # Normalize to lowercase for case-insensitive comparison
    
    # Filter the co-occurrence data
    filtered_cooccurrence_df = cooccurrence_df[
        cooccurrence_df['entity1'].str.lower().isin(valid_entities) &  # Check entity1 exists
        cooccurrence_df['entity2'].str.lower().isin(valid_entities)   # Check entity2 exists
    ]
    
    # Save the cleaned co-occurrence data
    filtered_cooccurrence_df.to_csv(output_file, index=False)
    print(f"Cleaned co-occurrence data saved to {output_file}")

# Usage example
cooccurrence_csv = "/home/vidur/mediagraph/data/cooccurrences_with_dates2020.csv"  # Replace with your co-occurrence CSV file path
cleaned_entities_csv = "/home/vidur/mediagraph/data/cleaned_entities2020.csv"  # Replace with your cleaned entities CSV file path
output_csv = "/home/vidur/mediagraph/data/cleaned_co_occurrence2020.csv"  # Replace with your desired output CSV file path

clean_cooccurrence(cooccurrence_csv, cleaned_entities_csv, output_csv)

