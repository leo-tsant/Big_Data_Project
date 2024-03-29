import pandas as pd
import re

movie_df = pd.read_csv("/home/leonidastsant/Downloads/MovieLens_Dataset/movie.csv")


# Initialize empty DataFrame (Specifies that movieId is an integer)
new_df = pd.DataFrame(dict(movieId=pd.Series([], dtype=int), title=[], genre=[], year_of_release=pd.Series([], dtype=int)))

i = 0 

# While loop that adds new row to DataFrame for each genre
while i < len(movie_df):
    # print(f"ID: {i+1} Title: {movie_df.title[i]}")

    # Try except block because .csv file might be corrupted
    try:
        # RegEx to keep only the last parenthesis
        year_with_par = re.search("\(([^()]*)\)$", movie_df.title[i]).group()

        # Regex to keep only the contents of a parenthesis
        year_of_release = int(re.search("(?<=\().+?(?=\))", year_with_par).group())
        row_to_insert = {'movieId': movie_df.movieId[i], 'title': movie_df.title[i], 'genre': movie_df.genres[i], 'year_of_release': year_of_release}


        new_df = new_df.append(row_to_insert, ignore_index = True)
    except:
        i += 1
        continue
    
    i += 1

new_df.to_csv("/home/leonidastsant/Downloads/MovieLens_Dataset/movie_info.csv", index=False)

print("Done!")