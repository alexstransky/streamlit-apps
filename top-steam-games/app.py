import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration to wide mode and create main container
st.set_page_config(layout="wide")

# Create main container for tabs
main_container = st.container()

# Load the data (locally)
# data = pd.read_csv('data/steam_top_100_played_games_clean.csv')

# Load the data (github)
data = pd.read_csv('../data/steam_top_100_played_games_clean.csv')

# Create placeholder for tabs
tab_container = st.container()
content_container = st.container()

# Create tabs
tabs = tab_container.tabs(["Top 10 Games", "Game Statistics", "Paid Games Trends"])

# Add content to tabs
with tabs[0]:
    # Show filters in sidebar
    with st.sidebar:
        # Filter options
        price_categories = data['Price Category'].unique().tolist()
        genre_tags = (data['Genre Tags']
                    .str.split(',')
                    .explode()
                    .str.strip()
                    .unique()
                    .tolist())
        genre_tags = sorted([tag for tag in genre_tags if tag])

        # Sidebar filters
        selected_price = st.multiselect('Select Price Category', price_categories)
        selected_genre = st.multiselect('Select Genre Tag', genre_tags)

    # Filter data based on selections
    filtered_data = data.copy()

    # Apply filters
    if selected_price:
        filtered_data = filtered_data[filtered_data['Price Category'].isin(selected_price)]
    if selected_genre:
        filtered_data['Genre List'] = filtered_data['Genre Tags'].str.split(',')
        genre_mask = filtered_data['Genre List'].apply(lambda x: any(genre.strip() in selected_genre for genre in x))
        filtered_data = filtered_data[genre_mask]

    # Sort filtered data and get top 10
    if not filtered_data.empty:
        # Get top 10 by Current Players and sort descending
        top_10_games = filtered_data.nlargest(10, 'Current Players')
        
        # Bar chart visualization using Altair
        st.title('Top 10 Played Games on Steam')
        
        # Create base chart with common properties
        base = alt.Chart(top_10_games).encode(
            x=alt.X('Name:N', 
                sort=alt.EncodingSortField(field='Current Players', order='descending'),
                title='Game Name')
        ).properties(
            height=400
        )
        
        # Create bars for Current Players
        current_players = base.mark_bar(color='steelblue').encode(
            y=alt.Y('Current Players:Q',
                title='Player Count'),
            tooltip=[
                alt.Tooltip('Name:N', title='Game'),
                alt.Tooltip('Current Players:Q', format=',', title='Current Players'),
                alt.Tooltip('Price Category:N'),
                alt.Tooltip('Price:Q', format='$.2f')
            ]
        )
        
        # Create bars for Peak Today
        peak_today = base.mark_bar(color='lightsteelblue', opacity=0.7).encode(
            y=alt.Y('Peak Today:Q'),
            tooltip=[
                alt.Tooltip('Name:N', title='Game'),
                alt.Tooltip('Peak Today:Q', format=',', title='Peak Today'),
                alt.Tooltip('Price Category:N'),
                alt.Tooltip('Price:Q', format='$.2f')
            ]
        )
        
        # Layer the charts and display
        chart = alt.layer(peak_today, current_players)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.title('Top 10 Played Games on Steam')
        st.write("No games found matching the selected filters.")

with tabs[1]:
    # Clear sidebar for Tab 2
    st.sidebar.empty()

    st.title('Game Statistics')
    
    # Create a list of available games for the selectbox
    available_games = sorted(data['Name'].unique().tolist())
    
    # Game search box with autocomplete
    game_search = st.selectbox('Select a game', available_games)
    
    if game_search:
        # Get the selected game's data
        game_data = data[data['Name'] == game_search].iloc[0]
        
        # Display game name with hyperlink
        st.markdown(f"## [{game_data['Name']}]({game_data['Store Link']})")
        
        # Display thumbnail if URL exists
        if pd.notna(game_data['Thumbnail URL']):
            st.image(game_data['Thumbnail URL'], width=300)
        
        # Display metrics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current Players", f"{game_data['Current Players']:,}")
            st.metric("Price Category", game_data['Price Category'])
            st.metric("Price", f"${game_data['Price']:.2f}")
        
        with col2:
            st.metric("Peak Today", f"{game_data['Peak Today']:,}")
            st.text("Genres:")
            st.write(game_data['Genre Tags'])
        
        st.divider()

with tabs[2]:
    # Clear sidebar for Tab 3
    st.sidebar.empty()
    
    st.title('Paid Games Analysis')
    
    # Filter for paid games only
    paid_games = data[data['Price Category'] == 'Paid'].copy()
    
    # Add metric selector
    selected_metric = st.radio(
        "Select Player Count Metric",
        ["Current Players", "Peak Today"],
        horizontal=True
    )
    
    # Create scatter plot using Altair
    scatter = alt.Chart(paid_games).mark_circle(
        size=60,
        color='steelblue'
    ).encode(
        x=alt.X('Price:Q', 
                title='Price (£)',
                axis=alt.Axis(format='$,.2f'),  # Use $ as placeholder, will be replaced with £
                scale=alt.Scale(domain=[0, paid_games['Price'].max() * 1.1])),
        y=alt.Y(f'{selected_metric}:Q',
                title=selected_metric,
                axis=alt.Axis(format=',.0f'),
                scale=alt.Scale(domain=[0, paid_games[selected_metric].max() * 1.1])),
        tooltip=[
            alt.Tooltip('Name:N', title='Game'),
            alt.Tooltip('Price:Q', format='$,.2f', title='Price'),
            alt.Tooltip('Current Players:Q', format=',.0f', title='Current Players'),
            alt.Tooltip('Peak Today:Q', format=',.0f', title='Peak Today')
        ]
    ).properties(
        width='container',
        height=500,
        title=f'Price vs {selected_metric} for Paid Games'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).interactive()

    # Convert $ to £ in the rendered chart
    st.altair_chart(
        scatter.configure_axis(
            labelExpr="replace(datum.label, '$', '£')"
        ), 
        use_container_width=True
    )
    
    # Display summary statistics
    st.subheader('Summary Statistics')
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Paid Games", f"{len(paid_games):,}")
        st.metric("Average Price", f"${paid_games['Price'].mean():.2f}")
    
    with col2:
        metric_mean = paid_games[selected_metric].mean()
        st.metric(f"Average {selected_metric}", f"{int(metric_mean):,}")
        st.metric("Median Price", f"${paid_games['Price'].median():.2f}")