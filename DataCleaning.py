#Data Cleaning
import pandas as pd
import re
# Load the CSV file
file_path = 'kdrama_dataset_with_ratings_plots_and_images.csv'
df = pd.read_csv(file_path)

# Replace placeholder values with NaN
df.replace({"N/A": None, "No rating": None, "No plot": None , "Add a plot in your language   ": None, "['N/A']":None , "No IMDb link":None}, inplace=True)
df.dropna(subset=['Title', 'Actors', 'Directors', 'Plot', 'Genre'], inplace=True)
df['IMDb_Rating'] = df['IMDb_Rating'].replace(r'^\s*$', None, regex=True)  # Replace blanks with NaN
df.replace({"N/A": None, "No rating": None, "No plot": None}, inplace=True)

# Drop rows with NaN in critical columns including 'IMDb_Rating'
df.dropna(subset=['Title', 'Actors', 'Directors', 'Plot', 'Genre', 'IMDb_Rating'], inplace=True)
def remove_references(entry):
    if isinstance(entry, str):
        return re.sub(r'\[\d+\]', '', entry).strip()
    elif isinstance(entry, list):
        return [re.sub(r'\[\d+\]', '', str(item)).strip() for item in entry]
    return entry

df['Genre'] = df['Genre'].apply(remove_references)
df['Actors'] = df['Actors'].apply(remove_references)
df['Directors'] = df['Directors'].apply(remove_references)
df['Plot'] = df['Plot'].fillna("This drama features a captivating storyline, engaging characters, and memorable moments.")
output_file = 'kdrama_cleaned_dataset.csv'
df.to_csv(output_file, index=False)
print("Cleaned Dataset:")
print(df.head())


