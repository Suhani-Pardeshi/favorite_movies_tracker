# 🎬 Favorite Movies Tracker

<img width="1920" height="1020" alt="Suhani-Pardeshi_favorite_movies_tracker - Google Chrome 19-11-2026 11_56_25" src="https://github.com/user-attachments/assets/68ab21f5-2122-49ae-8a8f-53c703f6a41e" />
<img width="1920" height="1020" alt="Favorite Movies Tracker - Personal - Microsoft​ Edge 19-11-2026 11_56_33" src="https://github.com/user-attachments/assets/65fc45cd-3fe5-4b8e-b733-162d3b5c2ad1" />

A simple and interactive web application built using **Python, Streamlit, and SQLite** to manage and organize your favorite movies.

Users can add, view, search, update, and delete movies while tracking their ratings.

## ✨ Features

- **Add Movies:** Add a movie with its title, genre, and rating.
- **View Movies:** Display all saved movies in a table.
- **Edit Movies:** Update movie details and ratings.
- **Delete Movies:** Remove movies from your collection.
- **Search Movies:** Search for movies by title.
- **Rating System:** Rate movies from 1 to 5 stars.
- **Top Pick:** Movies with a 5-star rating are highlighted as "Top Pick!"
- **Sort Movies:** Sort by highest rating, lowest rating, title, or newest first.
- **Random Movie Suggestion:** Get a random movie recommendation from your collection.
- **Dashboard:** View total movies, top picks, and average rating.

## 🛠️ Technologies Used

- **Python** – Application logic
- **Streamlit** – User interface
- **SQLite** – Database
- **Pandas** – Displaying movie data

## 📁 Project Structure

```text
favorite_movies_tracker/
│
├── app.py
├── database.sql
├── requirements.txt
├── .gitignore
└── README.md
```

The `movies.db` database file is created automatically when the application runs for the first time.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Suhani-Pardeshi/favorite_movies_tracker.git
```

### 2. Open the project folder

```bash
cd favorite_movies_tracker
```

### 3. Create a virtual environment (optional)

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install required packages

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🗄️ Database Structure

The application uses an SQLite database with a `movies` table.

| Column | Description |
|---|---|
| id | Auto-generated Movie ID |
| title | Movie title |
| genre | Movie genre |
| rating | Movie rating (1–5) |

## 🎯 Project Objective

The objective of this project is to develop a user-friendly movie management application that demonstrates CRUD operations (Create, Read, Update, Delete), database connectivity, search functionality, and data organization.

## 👩‍💻 Author

**Suhani Pardeshi**

GitHub: [Suhani-Pardeshi](https://github.com/Suhani-Pardeshi)

---
