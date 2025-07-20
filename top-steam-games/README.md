# Steam Games Visualization

This project is a Streamlit application that visualizes Steam games data through three interactive views:
1. Top 10 played games with current and peak player counts
2. Detailed game statistics with store links and thumbnails
3. Price analysis for paid games

## Features

- **Top 10 Games View**:
  - Interactive bar chart showing Current Players and Peak Today
  - Filters for Price Category and Genre Tags
  - Tooltips with detailed game information

- **Game Statistics View**:
  - Search functionality for individual games
  - Game thumbnails and store links
  - Detailed metrics including player counts and pricing
  - Genre information

- **Paid Games Analysis**:
  - Interactive scatter plot of Price vs Player Counts
  - Toggle between Current Players and Peak Today
  - Summary statistics for paid games
  - Price formatting in GBP (£)

## Project Structure

```
top-steam-games
├── data
│   └── steam_top_100_played_games_clean.csv
│   └── steam_top_100_played_games_list.csv
├── app.py
├── data_cleaning.ipynb
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd top-steam-games
   ```

2. **Install the required packages**:
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Then install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run src/app.py
   ```

## Usage

### Top 10 Games View
- View the top 10 games by current players
- Use sidebar filters to filter by price category and genres
- Hover over bars to see detailed statistics

### Game Statistics View
- Search for specific games using the dropdown
- View game thumbnails and direct links to Steam store
- See detailed player counts and genre information

### Paid Games Analysis
- Explore the relationship between game prices and player counts
- Toggle between current and peak player metrics
- View summary statistics for paid games

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements.