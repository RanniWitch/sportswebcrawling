
import webbrowser
import requests
from bs4 import BeautifulSoup

# Import the sports teams data
from sports_data import espn_sports, nba_teams, all_teams

def get_roster_info(sport, team_abbrev, team_name):
    """Scrape roster information from ESPN team roster page"""
    roster_url = f"https://www.espn.com/{sport}/team/roster/_/name/{team_abbrev}/{team_name}"
    print(f"Scraping roster from: {roster_url}")
    
    try:
        # Send GET request to the roster page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(roster_url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find roster table or player information
        roster_data = []
        
        # Look for roster table (ESPN uses different structures for different sports)
        roster_table = soup.find('table', class_='Table')
        if roster_table:
            rows = roster_table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cells = row.find_all('td')
                if len(cells) >= 3:
                    # Extract player name and number separately
                    name_cell = cells[1] if len(cells) > 1 else None
                    player_name = 'N/A'
                    player_number = 'N/A'
                    
                    if name_cell:
                        # Look for the number in the specific class
                        number_element = name_cell.find(class_='pl2 n10')
                        if number_element:
                            player_number = number_element.get_text(strip=True)
                            # Remove the number element to get clean name
                            number_element.decompose()
                        
                        # Get the clean player name
                        player_name = name_cell.get_text(strip=True)
                    
                    # Extract additional player details from other columns
                    age = cells[3].get_text(strip=True) if len(cells) > 3 else 'N/A'
                    height = cells[4].get_text(strip=True) if len(cells) > 4 else 'N/A'
                    weight = cells[5].get_text(strip=True) if len(cells) > 5 else 'N/A'
                    college = cells[6].get_text(strip=True) if len(cells) > 6 else 'N/A'
                    
                    player_info = {
                        'name': player_name,
                        'position': cells[2].get_text(strip=True) if len(cells) > 2 else 'N/A',
                        'number': player_number,
                        'age': age,
                        'height': height,
                        'weight': weight,
                        'college': college
                    }
                    roster_data.append(player_info)
        
        # Alternative: Look for player cards or other roster formats
        if not roster_data:
            player_cards = soup.find_all('div', class_='player-card') or soup.find_all('a', class_='AnchorLink')
            for card in player_cards[:20]:  # Limit to first 20 to avoid non-player links
                name = card.get_text(strip=True)
                if name and len(name) > 2:  # Basic filter for actual names
                    roster_data.append({'name': name, 'position': 'N/A', 'number': 'N/A'})
        
        return roster_data
        
    except requests.RequestException as e:
        print(f"Error fetching roster: {e}")
        return []
    except Exception as e:
        print(f"Error parsing roster: {e}")
        return []

favorite_sport = input("Enter your favorite sport: ")
favorite_team = input("Enter your favorite team: ")

# Check if the team exists in the sport
if favorite_team in espn_sports[favorite_sport]:
    print(f"Found {favorite_team} in {favorite_sport}")
    
    # ESPN URL structure
    teamAbriev = favorite_team[:3]
    team_url = f"https://www.espn.com/{favorite_sport}/team/_/name/{teamAbriev}/{favorite_team}"
    print(f"Team URL: {team_url}")
    
    # Get roster information
    print(f"\nFetching roster for {favorite_team}...")
    roster = get_roster_info(favorite_sport, teamAbriev, favorite_team)
    
    if roster:
        print(f"\n{favorite_team.upper()} ROSTER:")
        print("-" * 90)
        print(f"{'Name':<25} {'#':<4} {'Pos':<4} {'Age':<4} {'Height':<7} {'Weight':<8} {'College':<20}")
        print("-" * 90)
        for i, player in enumerate(roster, 1):
            jersey = f"#{player['number']}" if player['number'] != 'N/A' else 'N/A'
            print(f"{player['name']:<25} {jersey:<4} {player['position']:<4} {player['age']:<4} {player['height']:<7} {player['weight']:<8} {player['college']:<20}")

    else:
        print("Could not retrieve roster information")
        
    # Optionally open the roster page in browser
   # roster_url = f"https://www.espn.com/{favorite_sport}/team/roster/_/name/{teamAbriev}/{favorite_team}"
    #webbrowser.open(roster_url)
        
else:
    print(f"Team {favorite_team} not found in {favorite_sport}")

# You can also check if a team exists in any sport
if favorite_team in all_teams:
    print(f"\n{favorite_team} exists in ESPN sports database")