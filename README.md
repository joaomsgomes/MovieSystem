# Movie Recommendation System

## Overview

This project is a movie recommendation system built to help users discover new movies based on their preferences. The system uses collaborative filtering techniques, leveraging user ratings to make personalized recommendations. Users can log in, rate movies, and receive recommendations tailored to their interests.

## Features

- **User Registration & Login**: Users can either log in with their existing account or create a new one.
- **Personalized Recommendations**: Based on a user's ratings, the system recommends movies that other similar users have rated highly.
- **Genre-based Initial Ratings**: New users are prompted to rate movies from different genres to help the system understand their preferences.
- **View Past Ratings**: Users can view their own ratings and see what movies they've rated so far.
- **Movie Search & Rating**: Users can search for movies by title and provide their ratings for the movies they’ve watched.

## How It Works

1. **User Interaction**: Upon logging in or creating a new account, the user is prompted to rate movies across various genres. This data is stored and used to recommend new movies.
2. **Recommendation Engine**: The system uses collaborative filtering and cosine similarity to analyze patterns in ratings, identifying similar users and suggesting movies they liked that the current user hasn't yet rated.
3. **Movie Database**: The system uses a movie database, where each movie has attributes like title and genre, and each user has their own ratings for those movies.
4. **CSV-based Storage**: All user data and ratings are stored in CSV files, allowing easy manipulation and persistence between sessions.

## Requirements

- Python 3.x
- Pandas
- NumPy
- Scikit-learn

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/joaomsgomes/movie-recommendation-system.git
2. Navigate to the project folder:
   cd movie-recommendation-system

3. Install the necessary dependencies:
   pip install -r requirements.txt

4. Run the application:
   python system.py

## Future Improvements

- Implement more advanced recommendation algorithms (e.g., matrix factorization).
- Add movie descriptions, ratings from other platforms, and user reviews for more enriched recommendations.
- Add FrontEnd part of the Project

## Contributions

Contributions are welcome! Feel free to fork the project, submit issues, or create pull requests with improvements.
   
