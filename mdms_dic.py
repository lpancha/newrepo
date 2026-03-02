import json
import os

# File to save/load movie data
DATA_FILE = "movies_data.json"

# Initialize movie database
movies = {
    "The Dark Knight": {
        "year": 2008,
        "genre": "Action",
        "director": "Christopher Nolan",
        "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"]
    },
    "Inception": {
        "year": 2010,
        "genre": "Sci-Fi",
        "director": "Christopher Nolan",
        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"]
    },
    "Pulp Fiction": {
        "year": 1994,
        "genre": "Crime",
        "director": "Quentin Tarantino",
        "actors": ["John Travolta", "Samuel L. Jackson", "Uma Thurman"]
    }
}


# ── Save / Load ──────────────────────────────────────────────────────────────

def save_data():
    """Save movie database to a JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(movies, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data():
    """Load movie database from a JSON file (if it exists)."""
    global movies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                movies = json.load(f)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
    else:
        print("No saved data found. Starting with default database.")


# ── Display ──────────────────────────────────────────────────────────────────

def view_all_movies():
    """Print all movies and their information."""
    if not movies:
        print("The movie database is empty.")
        return
    print("\n===== Movie Database =====")
    for movie in movies:
        print(f"\nMovie: {movie}")
        for key, value in movies[movie].items():
            print(f"  {key}: {value}")
    print("==========================\n")


# ── Add ──────────────────────────────────────────────────────────────────────

def add_movie():
    """Add a new movie to the database."""
    print("\n--- Add a New Movie ---")
    title = input("Enter movie title: ").strip()
    if not title:
        print("Error: Movie title cannot be empty.")
        return
    if title in movies:
        print(f"Error: '{title}' already exists in the database.")
        return

    # Year
    year_input = input("Enter release year: ").strip()
    if not year_input.isdigit():
        print("Error: Year must be a valid number.")
        return
    year = int(year_input)

    genre = input("Enter genre: ").strip()
    if not genre:
        print("Error: Genre cannot be empty.")
        return

    director = input("Enter director: ").strip()
    if not director:
        print("Error: Director cannot be empty.")
        return

    actors_input = input("Enter actors (comma-separated): ").strip()
    actors = [a.strip() for a in actors_input.split(",") if a.strip()]
    if not actors:
        print("Error: At least one actor is required.")
        return

    movies[title] = {
        "year": year,
        "genre": genre,
        "director": director,
        "actors": actors
    }
    print(f"'{title}' has been added to the database.")


# ── Edit ─────────────────────────────────────────────────────────────────────

def edit_movie():
    """Edit an existing movie's information."""
    print("\n--- Edit a Movie ---")
    title = input("Enter the title of the movie to edit: ").strip()
    if title not in movies:
        print(f"Error: '{title}' not found in the database.")
        return

    print(f"Editing '{title}'. Press Enter to keep the current value.")
    movie = movies[title]

    # Year
    current_year = movie["year"]
    year_input = input(f"Enter new year [{current_year}]: ").strip()
    if year_input:
        if not year_input.isdigit():
            print("Error: Year must be a valid number. Keeping original.")
        else:
            movie["year"] = int(year_input)

    # Genre
    current_genre = movie["genre"]
    genre_input = input(f"Enter new genre [{current_genre}]: ").strip()
    if genre_input:
        movie["genre"] = genre_input

    # Director
    current_director = movie["director"]
    director_input = input(f"Enter new director [{current_director}]: ").strip()
    if director_input:
        movie["director"] = director_input

    # Actors
    current_actors = ", ".join(movie["actors"])
    actors_input = input(f"Enter new actors (comma-separated) [{current_actors}]: ").strip()
    if actors_input:
        new_actors = [a.strip() for a in actors_input.split(",") if a.strip()]
        if new_actors:
            movie["actors"] = new_actors

    print(f"'{title}' has been updated.")


# ── Delete ───────────────────────────────────────────────────────────────────

def delete_movie():
    """Delete a movie from the database."""
    print("\n--- Delete a Movie ---")
    title = input("Enter the title of the movie to delete: ").strip()
    if title not in movies:
        print(f"Error: '{title}' not found in the database.")
        return
    confirm = input(f"Are you sure you want to delete '{title}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        del movies[title]
        print(f"'{title}' has been deleted.")
    else:
        print("Deletion cancelled.")


# ── Search ───────────────────────────────────────────────────────────────────

def search_movies():
    """Search for movies by title, genre, director, year, or actor."""
    print("\n--- Search Movies ---")
    print("Search by: 1) Title  2) Genre  3) Director  4) Year  5) Actor")
    choice = input("Enter choice (1-5): ").strip()

    criteria_map = {
        "1": "title",
        "2": "genre",
        "3": "director",
        "4": "year",
        "5": "actor"
    }

    if choice not in criteria_map:
        print("Error: Invalid choice.")
        return

    criteria = criteria_map[choice]
    query = input(f"Enter {criteria} to search for: ").strip().lower()
    if not query:
        print("Error: Search query cannot be empty.")
        return

    results = {}
    for title, info in movies.items():
        if criteria == "title" and query in title.lower():
            results[title] = info
        elif criteria == "genre" and query in info.get("genre", "").lower():
            results[title] = info
        elif criteria == "director" and query in info.get("director", "").lower():
            results[title] = info
        elif criteria == "year" and query == str(info.get("year", "")):
            results[title] = info
        elif criteria == "actor":
            for actor in info.get("actors", []):
                if query in actor.lower():
                    results[title] = info
                    break

    if results:
        print(f"\nFound {len(results)} result(s):")
        for title, info in results.items():
            print(f"\nMovie: {title}")
            for key, value in info.items():
                print(f"  {key}: {value}")
    else:
        print("No movies found matching your search.")


# ── Main Menu ────────────────────────────────────────────────────────────────

def main():
    load_data()
    while True:
        print("\n====== Movie Database Management System ======")
        print("1. View all movies")
        print("2. Add a movie")
        print("3. Edit a movie")
        print("4. Delete a movie")
        print("5. Search movies")
        print("6. Save data")
        print("7. Exit")
        print("===============================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            view_all_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            edit_movie()
        elif choice == "4":
            delete_movie()
        elif choice == "5":
            search_movies()
        elif choice == "6":
            save_data()
        elif choice == "7":
            save_choice = input("Save data before exiting? (yes/no): ").strip().lower()
            if save_choice == "yes":
                save_data()
            print("Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
