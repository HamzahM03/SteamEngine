# Steam Game Recommendation System

A content-based recommendation system that suggests similar Steam games based on user input. Get 5 personalized game recommendations by simply entering a game title.
<img width="2000" height="2000" alt="Steam Engine" src="https://github.com/user-attachments/assets/a829f996-e988-4d35-b276-8ebd96a2398e" />

## Overview

This system analyzes game attributes from the top 1000 Steam games to find and recommend titles similar to your favorites. Built with a straightforward web interface, it provides instant recommendations to help you discover your next gaming adventure.

## Features

- **Simple Input**: Enter any game title from the dataset
- **Smart Recommendations**: Receive 5 similar games based on content analysis
- **Fast Results**: Instant recommendations powered by Python backend
- **Clean Interface**: Intuitive web UI for seamless user experience

## Technologies Used

- **Model**: Python (Google Colab)
- **Frontend**: HTML, CSS, JavaScript
- **Dataset**: (https://www.kaggle.com/datasets/joebeachcapital/top-1000-steam-games)

## Dataset

The recommendation engine uses the "Top 1000 Steam Games" dataset from Kaggle, which includes information about:
- Game titles
- Genres
- User reviews and ratings
- Release dates
- Other relevant game metadata

## How It Works

1. **Input**: User enters the exact name of a Steam game
2. **Processing**: The system analyzes game features and finds similar titles
3. **Output**: Displays 5 games most similar to the input game
<img width="1344" height="906" alt="example" src="https://github.com/user-attachments/assets/6c42067d-0d48-4891-b792-311be9e664ac" />

## Current Limitations

- **Exact Match Required**: Game names must be entered exactly as they appear in the dataset
- No autocomplete or spell-checking functionality (yet!)

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries (see `requirements.txt`)
- Web browser

### Installation

#Work in progress

## Usage

1. Enter the exact title of a Steam game from the dataset
2. Click the submit button
3. View your 5 personalized game recommendations

## Future Improvements

- Add autocomplete functionality
- Implement fuzzy matching for game titles
- Add filtering options (genre, price, rating)
- Include game thumbnails and detailed descriptions
- Dataset provided by [Joe Beach Capital on Kaggle](https://www.kaggle.com/joebeachcapital)
