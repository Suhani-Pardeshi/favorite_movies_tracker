import random
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# -------------------- Configuration --------------------
st.set_page_config(
    page_title="Favorite Movies Tracker",
    page_icon="🎬",
    layout="wide",
)

DB_PATH = Path(__file__).with_name("movies.db")


# -------------------- Database --------------------
def get_connection():
    """Create a SQLite connection and return rows as dictionary-like objects."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the movies table if it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5)
            )
            """
        )


def add_movie(title, genre, rating):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO movies (title, genre, rating) VALUES (?, ?, ?)",
            (title.strip(), genre.strip(), int(rating)),
        )


def get_movies(search_text=""):
    with get_connection() as connection:
        if search_text.strip():
            rows = connection.execute(
                """
                SELECT id, title, genre, rating
                FROM movies
                WHERE title LIKE ?
                ORDER BY id DESC
                """,
                (f"%{search_text.strip()}%",),
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT id, title, genre, rating
                FROM movies
                ORDER BY id DESC
                """
            ).fetchall()

    return [dict(row) for row in rows]


def update_movie(movie_id, title, genre, rating):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE movies
            SET title = ?, genre = ?, rating = ?
            WHERE id = ?
            """,
            (title.strip(), genre.strip(), int(rating), int(movie_id)),
        )


def delete_movie(movie_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM movies WHERE id = ?", (int(movie_id),))


# -------------------- UI Helpers --------------------
def rating_stars(rating):
    return "★" * int(rating) + "☆" * (5 - int(rating))


def show_movie_card(movie):
    top_pick = " 🏆 **Top Pick!**" if movie["rating"] == 5 else ""
    st.markdown(
        f"**{movie['title']}**{top_pick}  \n"
        f"Genre: {movie['genre']}  \n"
        f"Rating: {rating_stars(movie['rating'])} ({movie['rating']}/5)"
    )


# -------------------- Main Application --------------------
initialize_database()

st.title("🎬 Favorite Movies Tracker")
st.caption("Save, search, update and organize your favorite movies.")

movies = get_movies()
total_movies = len(movies)
top_picks = sum(1 for movie in movies if movie["rating"] == 5)
average_rating = (
    round(sum(movie["rating"] for movie in movies) / total_movies, 1)
    if total_movies
    else 0
)

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Total Movies", total_movies)
metric2.metric("Top Picks", top_picks)
metric3.metric("Average Rating", f"{average_rating}/5")

st.divider()

# Sidebar: Add movie form
with st.sidebar:
    st.header("➕ Add a Movie")

    with st.form("add_movie_form", clear_on_submit=True):
        new_title = st.text_input("Movie title", placeholder="e.g. Inception")
        new_genre = st.text_input("Genre", placeholder="e.g. Sci-Fi")
        new_rating = st.slider("Rating", min_value=1, max_value=5, value=3)
        add_submitted = st.form_submit_button(
            "Add Movie", type="primary", use_container_width=True
        )

        if add_submitted:
            if not new_title.strip() or not new_genre.strip():
                st.error("Title and genre are required.")
            else:
                add_movie(new_title, new_genre, new_rating)
                st.success(f'"{new_title.strip()}" was added.')
                st.rerun()

    st.divider()
    st.subheader("🎲 Movie Suggestion")

    if st.button("Suggest a random movie", use_container_width=True):
        current_movies = get_movies()
        if current_movies:
            suggestion = random.choice(current_movies)
            st.session_state["random_movie_id"] = suggestion["id"]
        else:
            st.session_state.pop("random_movie_id", None)
            st.info("Add a movie first.")

    random_movie_id = st.session_state.get("random_movie_id")
    if random_movie_id:
        random_movie = next(
            (movie for movie in get_movies() if movie["id"] == random_movie_id),
            None,
        )
        if random_movie:
            st.markdown("**Your suggestion:**")
            show_movie_card(random_movie)

# Main content
st.subheader("📚 Your Movie Collection")

search_col, sort_col = st.columns([2, 1])
with search_col:
    search_text = st.text_input(
        "Search by movie title",
        placeholder="Type a title to search...",
    )
with sort_col:
    sort_option = st.selectbox(
        "Sort movies",
        ["Newest first", "Highest rating", "Lowest rating", "Title A–Z"],
    )

display_movies = get_movies(search_text)

if sort_option == "Highest rating":
    display_movies.sort(key=lambda movie: (-movie["rating"], movie["title"].lower()))
elif sort_option == "Lowest rating":
    display_movies.sort(key=lambda movie: (movie["rating"], movie["title"].lower()))
elif sort_option == "Title A–Z":
    display_movies.sort(key=lambda movie: movie["title"].lower())

if not display_movies:
    if search_text.strip():
        st.info("No movies found. Try another title.")
    else:
        st.info("Your collection is empty. Add your first movie using the sidebar.")
else:
    # Table view
    table_data = []
    for movie in display_movies:
        table_data.append(
            {
                "ID": movie["id"],
                "Title": ("🏆 " if movie["rating"] == 5 else "") + movie["title"],
                "Genre": movie["genre"],
                "Rating": f"{movie['rating']}/5",
            }
        )

    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Manage a movie")
    movie_options = {
        f"{movie['title']} (ID: {movie['id']})": movie for movie in display_movies
    }
    selected_label = st.selectbox("Select a movie", list(movie_options.keys()))
    selected_movie = movie_options[selected_label]

    edit_col, delete_col = st.columns(2)

    with edit_col:
        with st.expander("✏️ Edit selected movie"):
            with st.form(f"edit_movie_{selected_movie['id']}"):
                edited_title = st.text_input(
                    "Title",
                    value=selected_movie["title"],
                    key=f"edit_title_{selected_movie['id']}",
                )
                edited_genre = st.text_input(
                    "Genre",
                    value=selected_movie["genre"],
                    key=f"edit_genre_{selected_movie['id']}",
                )
                edited_rating = st.slider(
                    "Rating",
                    min_value=1,
                    max_value=5,
                    value=int(selected_movie["rating"]),
                    key=f"edit_rating_{selected_movie['id']}",
                )
                update_submitted = st.form_submit_button(
                    "Save Changes", type="primary"
                )

                if update_submitted:
                    if not edited_title.strip() or not edited_genre.strip():
                        st.error("Title and genre are required.")
                    else:
                        update_movie(
                            selected_movie["id"],
                            edited_title,
                            edited_genre,
                            edited_rating,
                        )
                        st.success("Movie updated successfully.")
                        st.rerun()

    with delete_col:
        with st.expander("🗑️ Delete selected movie"):
            st.warning(
                f"You are about to delete **{selected_movie['title']}**. "
                "This action cannot be undone."
            )
            confirm_delete = st.checkbox(
                "I confirm that I want to delete this movie.",
                key=f"confirm_delete_{selected_movie['id']}",
            )
            if st.button(
                "Delete Movie",
                type="secondary",
                disabled=not confirm_delete,
                key=f"delete_button_{selected_movie['id']}",
            ):
                delete_movie(selected_movie["id"])
                st.success("Movie deleted successfully.")
                st.rerun()

    st.markdown("### Movie Details")
    detail_cols = st.columns(3)
    for index, movie in enumerate(display_movies):
        with detail_cols[index % 3]:
            with st.container(border=True):
                show_movie_card(movie)
                st.caption(f"Movie ID: {movie['id']}")

st.divider()
st.caption("Favorite Movies Tracker | Built with Python, Streamlit and SQLite")
