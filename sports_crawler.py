import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time
import re
from sports_data import espn_sports, nba_teams, all_teams

class SportsCrawler:
    def __init__(self, sport, team_name, team_abbrev):
        self.sport = sport
        self.team_name = team_name
        self.team_abbrev = team_abbrev
        self.base_url = "https://www.espn.com"
        
        # Crawl frontier - BFS queue
        self.url_queue = deque()
        self.visited_urls = set()
        self.scraped_data = {
            'roster': [],
            'schedule': [],
            'news': [],
            'stats': []
        }
        
        # Request headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Initialize seed URLs
        self.seed_urls = self._generate_seed_urls()
        
        # URL patterns
        self.include_patterns = [
            rf"/{sport}/team/.*/{team_abbrev}/{team_name}",
            rf"/{sport}/team/roster/.*/{team_abbrev}/{team_name}",
            rf"/{sport}/team/schedule/.*/{team_abbrev}/{team_name}",
            rf"/{sport}/team/stats/.*/{team_abbrev}/{team_name}",
            rf"/{sport}/team/news/.*/{team_abbrev}/{team_name}",
            rf"/{sport}/player/.*"  # Individual player pages
        ]
        
        self.exclude_patterns = [
            r"/login",
            r"/register", 
            r"/subscribe",
            r"/ads/",
            r"/search\?",
            r"\.pdf$",
            r"\.jpg$",
            r"\.png$",
            r"\.gif$",
            r"/video/",
            r"/fantasy/",
            r"/betting/"
        ]
    
    def _generate_seed_urls(self):
        """Generate starting URLs for the crawler"""
        base_team_url = f"{self.base_url}/{self.sport}/team/_/name/{self.team_abbrev}/{self.team_name}"
        
        seed_urls = [
            base_team_url,  # Main team page
            f"{base_team_url}/roster",  # Roster page
            f"{base_team_url}/schedule",  # Schedule page
            f"{base_team_url}/stats",  # Stats page
            f"{self.base_url}/{self.sport}/team/news/_/name/{self.team_abbrev}/{self.team_name}",  # News page
        ]
        
        return seed_urls
    
    def _should_crawl_url(self, url):
        """Check if URL should be crawled based on include/exclude patterns"""
        # Check exclude patterns first
        for pattern in self.exclude_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False
        
        # Check include patterns
        for pattern in self.include_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_links(self, soup, current_url):
        """Extract and filter links from the current page"""
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(current_url, href)
            
            # Clean URL (remove fragments)
            parsed = urlparse(absolute_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                clean_url += f"?{parsed.query}"
            
            # Check if we should crawl this URL
            if (clean_url not in self.visited_urls and 
                self._should_crawl_url(clean_url) and
                clean_url.startswith(self.base_url)):
                links.append(clean_url)
        
        return links
    
    def _scrape_roster_page(self, soup):
        """Extract roster information from roster page"""
        roster_data = []
        
        # Use improved table detection
        roster_table = self._find_roster_table_improved(soup)
        
        if not roster_table:
            print(f"    ❌ No roster table found on page")
            return roster_data
        
        if roster_table:
            rows = roster_table.find_all('tr')
            print(f"    DEBUG: Processing {len(rows)} rows from roster table")
            
            for row in rows[1:]:  # Skip header
                cells = row.find_all('td')
                if len(cells) >= 6:  # Ensure we have enough columns for roster data
                    # Use the proven extraction logic from sports_webcrawl_fixed.py
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
                    
                    # Debug: Show what we're extracting
                    print(f"      DEBUG: Extracted name='{player_name}', number='{player_number}'")
                    
                    # Only add if we found a real player name (not team names)
                    if (player_name != 'N/A' and 
                        len(player_name) > 3 and 
                        not any(team in player_name.lower() for team in ['new orleans', 'dallas', 'san antonio', 'houston', 'memphis', 'atlanta', 'boston'])):
                        
                        player_info = {
                            'name': player_name,
                            'number': player_number,
                            'position': cells[2].get_text(strip=True) if len(cells) > 2 else 'N/A',
                            'age': cells[3].get_text(strip=True) if len(cells) > 3 else 'N/A',
                            'height': cells[4].get_text(strip=True) if len(cells) > 4 else 'N/A',
                            'weight': cells[5].get_text(strip=True) if len(cells) > 5 else 'N/A',
                            'college': cells[6].get_text(strip=True) if len(cells) > 6 else 'N/A'
                        }
                        roster_data.append(player_info)
        
        return roster_data
    
    def _find_roster_table_improved(self, soup):
        """
        Improved roster table detection using multiple strategies
        Returns the table most likely to contain roster data
        """
        
        tables = soup.find_all('table')
        print(f"    DEBUG: Analyzing {len(tables)} tables for roster data")
        table_scores = []
        
        for i, table in enumerate(tables):
            score = 0
            reasons = []
            
            # STRATEGY 1: Header Analysis (Weight: 30 points)
            header_row = table.find('thead') or table.find('tr')
            if header_row:
                header_text = header_row.get_text().lower()
                roster_keywords = ['name', 'player', '#', 'no', 'pos', 'age', 'height', 'weight', 'college']
                header_matches = sum(1 for keyword in roster_keywords if keyword in header_text)
                
                if header_matches >= 3:
                    score += 30
                    reasons.append(f"Headers match ({header_matches} keywords)")
            
            # STRATEGY 2: Jersey Numbers (Weight: 25 points)
            jersey_elements = table.find_all(class_='pl2 n10')
            if len(jersey_elements) >= 5:
                score += 25
                reasons.append(f"Jersey numbers ({len(jersey_elements)} found)")
            elif len(jersey_elements) >= 1:
                score += 10
                reasons.append(f"Some jersey numbers ({len(jersey_elements)} found)")
            
            # STRATEGY 3: Player Profile Links (Weight: 20 points)
            player_links = table.find_all('a', href=lambda x: x and '/player/' in x)
            if len(player_links) >= 10:
                score += 20
                reasons.append(f"Many player links ({len(player_links)} found)")
            elif len(player_links) >= 3:
                score += 10
                reasons.append(f"Some player links ({len(player_links)} found)")
            
            # STRATEGY 4: Data Patterns (Weight: 15 points)
            rows = table.find_all('tr')[1:]  # Skip header
            height_patterns = 0
            weight_patterns = 0
            
            for row in rows[:10]:  # Check first 10 rows
                cells = row.find_all('td')
                row_text = ' '.join(cell.get_text() for cell in cells)
                
                # Look for height patterns
                if "'" in row_text or '"' in row_text:
                    height_patterns += 1
                
                # Look for weight patterns  
                if 'lbs' in row_text or 'kg' in row_text:
                    weight_patterns += 1
            
            if height_patterns >= 3:
                score += 10
                reasons.append(f"Height patterns ({height_patterns} found)")
            
            if weight_patterns >= 3:
                score += 5
                reasons.append(f"Weight patterns ({weight_patterns} found)")
            
            # STRATEGY 5: Table Size (Weight: 10 points)
            row_count = len(table.find_all('tr'))
            if 10 <= row_count <= 25:  # Typical roster size
                score += 10
                reasons.append(f"Good size ({row_count} rows)")
            elif row_count >= 5:
                score += 5
                reasons.append(f"Decent size ({row_count} rows)")
            
            table_scores.append({
                'table': table,
                'score': score,
                'reasons': reasons,
                'index': i
            })
        
        # Sort by score and return best match
        table_scores.sort(key=lambda x: x['score'], reverse=True)
        
        if table_scores and table_scores[0]['score'] > 0:
            best = table_scores[0]
            print(f"    ✅ Selected table {best['index']} (Score: {best['score']})")
            print(f"    Reasons: {', '.join(best['reasons'])}")
            return best['table']
        
        print(f"    ❌ No good roster table found")
        return None
    
    def _scrape_schedule_page(self, soup):
        """Extract schedule information from schedule page"""
        schedule_data = []
        
        # Look for schedule table or game cards
        schedule_table = soup.find('table', class_='Table') or soup.find('div', class_='schedule')
        
        if schedule_table:
            # Extract game information
            games = schedule_table.find_all('tr')[1:] if schedule_table.name == 'table' else schedule_table.find_all('div', class_='game')
            
            for game in games[:10]:  # Limit to 10 games
                game_info = {
                    'opponent': 'N/A',
                    'date': 'N/A',
                    'time': 'N/A',
                    'result': 'N/A'
                }
                
                # Extract game details (this would need refinement based on actual HTML structure)
                text = game.get_text(strip=True)
                if text and len(text) > 10:
                    game_info['raw_text'] = text[:100]  # Store raw text for now
                
                schedule_data.append(game_info)
        
        return schedule_data
    
    def _scrape_news_page(self, soup):
        """Extract news articles from news page"""
        news_data = []
        
        # Look for news articles
        articles = soup.find_all('article') or soup.find_all('div', class_='contentItem')
        
        for article in articles[:5]:  # Limit to 5 articles
            title_elem = article.find('h1') or article.find('h2') or article.find('h3')
            title = title_elem.get_text(strip=True) if title_elem else 'N/A'
            
            # Look for article link
            link_elem = article.find('a', href=True)
            link = urljoin(self.base_url, link_elem['href']) if link_elem else 'N/A'
            
            if title != 'N/A' and len(title) > 5:
                news_data.append({
                    'title': title,
                    'link': link
                })
        
        return news_data
    
    def _scrape_page_content(self, url, soup):
        """Determine page type and scrape appropriate content"""
        if '/roster' in url:
            roster_data = self._scrape_roster_page(soup)
            self.scraped_data['roster'].extend(roster_data)
            print(f"  → Scraped {len(roster_data)} roster entries")
            
        elif '/schedule' in url:
            schedule_data = self._scrape_schedule_page(soup)
            self.scraped_data['schedule'].extend(schedule_data)
            print(f"  → Scraped {len(schedule_data)} schedule entries")
            
        elif '/news' in url:
            news_data = self._scrape_news_page(soup)
            self.scraped_data['news'].extend(news_data)
            print(f"  → Scraped {len(news_data)} news articles")
    
    def crawl(self, max_pages=10, delay=1):
        """Main crawling method using BFS"""
        print(f"Starting crawl for {self.team_name} ({self.sport.upper()})")
        print(f"Seed URLs: {len(self.seed_urls)}")
        
        # Add seed URLs to queue
        for url in self.seed_urls:
            self.url_queue.append(url)
        
        pages_crawled = 0
        
        while self.url_queue and pages_crawled < max_pages:
            # Pop URL from queue (BFS)
            current_url = self.url_queue.popleft()
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
            
            print(f"\n[{pages_crawled + 1}] Crawling: {current_url}")
            
            try:
                # Fetch page
                response = requests.get(current_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Mark as visited
                self.visited_urls.add(current_url)
                pages_crawled += 1
                
                # Scrape content based on page type
                self._scrape_page_content(current_url, soup)
                
                # Extract new links
                new_links = self._extract_links(soup, current_url)
                print(f"  → Found {len(new_links)} new links to crawl")
                
                # Add new links to queue
                for link in new_links:
                    if link not in self.visited_urls:
                        self.url_queue.append(link)
                
                # Respectful delay
                time.sleep(delay)
                
            except Exception as e:
                print(f"  → Error crawling {current_url}: {e}")
                continue
        
        print(f"\nCrawl completed! Visited {len(self.visited_urls)} pages")
        self._print_summary()
    
    def _print_summary(self):
        """Print summary of scraped data"""
        print("\n" + "="*60)
        print("CRAWL SUMMARY")
        print("="*60)
        
        print(f"Roster Players: {len(self.scraped_data['roster'])}")
        print(f"Schedule Entries: {len(self.scraped_data['schedule'])}")
        print(f"News Articles: {len(self.scraped_data['news'])}")
        
        # Show sample roster data
        if self.scraped_data['roster']:
            print(f"\nSAMPLE ROSTER DATA:")
            print("-" * 80)
            print(f"{'Name':<25} {'Jersey':<8} {'Pos':<5} {'Age':<4} {'Height':<8} {'College':<15}")
            print("-" * 80)
            for i, player in enumerate(self.scraped_data['roster'][:10], 1):
                jersey = f"#{player['number']}" if player['number'] != 'N/A' else 'N/A'
                print(f"{player['name']:<25} {jersey:<8} {player['position']:<5} {player['age']:<4} {player['height']:<8} {player['college']:<15}")
            
            # Debug: Show raw data for first player
            if self.scraped_data['roster']:
                print(f"\nDEBUG - First player raw data:")
                print(f"  {self.scraped_data['roster'][0]}")
        
        # Show sample news
        if self.scraped_data['news']:
            print(f"\nSAMPLE NEWS:")
            print("-" * 40)
            for i, article in enumerate(self.scraped_data['news'][:3], 1):
                print(f"{i}. {article['title'][:60]}...")

def crawl_all_teams(sport, max_pages_per_team=5):
    """Crawl all teams in a sport"""
    print(f"\n🏆 CRAWLING ALL {sport.upper()} TEAMS")
    print("="*60)
    
    all_teams = espn_sports[sport]
    total_teams = len(all_teams)
    
    print(f"Found {total_teams} teams in {sport.upper()}")
    print(f"Max pages per team: {max_pages_per_team}")
    print(f"Estimated total pages: {total_teams * max_pages_per_team}")
    
    # Confirm before starting large crawl
    confirm = input(f"\nProceed with crawling {total_teams} teams? (y/n): ").lower()
    if confirm != 'y':
        print("Crawl cancelled.")
        return
    
    # Aggregate results across all teams
    league_data = {
        'teams_crawled': 0,
        'total_players': 0,
        'total_games': 0,
        'total_news': 0,
        'team_summaries': []
    }
    
    for i, team in enumerate(all_teams, 1):
        print(f"\n[{i}/{total_teams}] 🏀 CRAWLING: {team.upper()}")
        print("-" * 50)
        
        try:
            # Create crawler for this team
            team_abbrev = team[:3]  # Simple abbreviation
            crawler = SportsCrawler(sport, team, team_abbrev)
            
            # Crawl this team
            crawler.crawl(max_pages=max_pages_per_team, delay=1)
            
            # Collect team summary
            team_summary = {
                'team': team,
                'players': len(crawler.scraped_data['roster']),
                'schedule_entries': len(crawler.scraped_data['schedule']),
                'news_articles': len(crawler.scraped_data['news']),
                'pages_visited': len(crawler.visited_urls)
            }
            
            league_data['team_summaries'].append(team_summary)
            league_data['teams_crawled'] += 1
            league_data['total_players'] += team_summary['players']
            league_data['total_games'] += team_summary['schedule_entries']
            league_data['total_news'] += team_summary['news_articles']
            
            print(f"✅ {team}: {team_summary['players']} players, {team_summary['schedule_entries']} games")
            
        except Exception as e:
            print(f"❌ Error crawling {team}: {e}")
            continue
    
    # Print league-wide summary
    print_league_summary(sport, league_data)

def print_league_summary(sport, league_data):
    """Print comprehensive league summary"""
    print(f"\n🏆 {sport.upper()} LEAGUE CRAWL SUMMARY")
    print("="*70)
    
    print(f"Teams Successfully Crawled: {league_data['teams_crawled']}")
    print(f"Total Players Found: {league_data['total_players']}")
    print(f"Total Schedule Entries: {league_data['total_games']}")
    print(f"Total News Articles: {league_data['total_news']}")
    
    # Top teams by data found
    if league_data['team_summaries']:
        print(f"\n📊 TOP TEAMS BY ROSTER SIZE:")
        print("-" * 40)
        sorted_teams = sorted(league_data['team_summaries'], 
                            key=lambda x: x['players'], reverse=True)
        
        for i, team in enumerate(sorted_teams[:10], 1):
            print(f"{i:2d}. {team['team']:<25} {team['players']:3d} players")
        
        print(f"\n📅 TOP TEAMS BY SCHEDULE DATA:")
        print("-" * 40)
        sorted_by_games = sorted(league_data['team_summaries'], 
                               key=lambda x: x['schedule_entries'], reverse=True)
        
        for i, team in enumerate(sorted_by_games[:10], 1):
            print(f"{i:2d}. {team['team']:<25} {team['schedule_entries']:3d} games")
    
    # Save results to file
    save_league_data(sport, league_data)

def save_league_data(sport, league_data):
    """Save league data to a file"""
    filename = f"{sport}_league_data.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write(f"{sport.upper()} LEAGUE CRAWL RESULTS\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Teams Crawled: {league_data['teams_crawled']}\n")
            f.write(f"Total Players: {league_data['total_players']}\n")
            f.write(f"Total Games: {league_data['total_games']}\n")
            f.write(f"Total News: {league_data['total_news']}\n\n")
            
            f.write("TEAM BREAKDOWN:\n")
            f.write("-" * 30 + "\n")
            
            for team in league_data['team_summaries']:
                f.write(f"{team['team']:<25} | ")
                f.write(f"Players: {team['players']:3d} | ")
                f.write(f"Games: {team['schedule_entries']:3d} | ")
                f.write(f"News: {team['news_articles']:3d}\n")
        
        print(f"\n💾 Results saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")

def main():
    print("ESPN Sports Crawler")
    print("="*50)
    
    # Get user input
    sport = input("Enter sport (nba, nfl, mlb, nhl, etc.): ").lower()
    
    if sport not in espn_sports:
        print(f"Sport '{sport}' not found in database")
        return
    
    team = input("Enter team name (e.g., boston-celtics) or 'none' for all teams: ").lower()
    
    if team == 'none':
        # Crawl all teams in the sport
        max_pages = int(input("Max pages per team (default 5): ") or "5")
        crawl_all_teams(sport, max_pages_per_team=max_pages)
    else:
        # Crawl single team
        if team not in espn_sports[sport]:
            print(f"Team '{team}' not found in {sport}")
            return
        
        # Create crawler
        team_abbrev = team[:3]  # Simple abbreviation
        crawler = SportsCrawler(sport, team, team_abbrev)
        
        # Start crawling
        max_pages = int(input("Max pages to crawl (default 10): ") or "10")
        crawler.crawl(max_pages=max_pages, delay=1)

if __name__ == "__main__":
    main()