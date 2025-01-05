import pandas as pd
import matplotlib.pyplot as plt
import zipfile

# Path to the ZIP file
zip_file_path = "C:\\Users\\Lanoi\\Data-analysis\\my_spotify_data.zip"

# Target file inside the ZIP (update this with the correct file name if needed)
target_file = "Spotify Account Data/StreamingHistory_music_0.json"  # Change to the file you want to process

try:
    # Open the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        # List all files in the ZIP archive
        file_list = z.namelist()
        print("Files in the ZIP archive:", file_list)

        # Check if the target file exists
        if target_file in file_list:
            # Read the target file
            with z.open(target_file) as f:
                # Update this to match the file format (JSON assumed here)
                data = pd.read_json(f)
                print("File loaded successfully.")
        else:
            print(f"Error: Target file '{target_file}' not found in the ZIP.")
            exit()
except FileNotFoundError:
    print("Error: ZIP file not found. Please check the file path.")
    exit()

# Display the first few rows of the data
print("\nFirst 5 rows of the dataset:")
print(data.head())

# Basic data information
print("\nDataset Information:")
print(data.info())

# Analyze data: most popular tracks
if "Popularity" in data.columns:
    print("\nTop 5 most popular tracks:")
    most_popular = data.sort_values(by="Popularity", ascending=False).head(5)
    print(most_popular[["Track", "Artist", "Popularity"]])
else:
    print("\nPopularity column missing. Skipping popularity analysis.")

# Analyze data: average duration by genre
if "Genre" in data.columns and "Duration" in data.columns:
    avg_duration_by_genre = data.groupby("Genre")["Duration"].mean()
    print("\nAverage Duration by Genre:")
    print(avg_duration_by_genre)

    # Plot average duration by genre
    avg_duration_by_genre.plot(kind='bar', figsize=(10, 6), title='Average Track Duration by Genre')
    plt.ylabel('Duration (ms)')
    plt.xlabel('Genre')
    plt.show()
else:
    print("\nGenre or Duration columns missing. Skipping duration analysis.")

# Analyze data: most represented genres
if "Genre" in data.columns:
    genre_counts = data["Genre"].value_counts()
    print("\nMost represented genres:")
    print(genre_counts.head(10))

    # Plot genre distribution
    genre_counts.head(10).plot(kind='pie', figsize=(8, 8), autopct='%1.1f%%', title='Top 10 Genres Distribution')
    plt.ylabel('')
    plt.show()
else:
    print("\nGenre column missing. Skipping genre distribution analysis.")

# Analyze data: popularity distribution
if "Popularity" in data.columns:
    plt.figure(figsize=(10, 6))
    plt.hist(data["Popularity"], bins=20, color='skyblue', edgecolor='black')
    plt.title('Popularity Distribution')
    plt.xlabel('Popularity')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("\nPopularity column missing. Skipping popularity distribution analysis.")
