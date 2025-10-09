# ESPN Sports Web Crawler

A comprehensive web crawler for extracting sports data from ESPN using intelligent table detection and BFS (Breadth-First Search) crawling.

## Features

- **Multi-Sport Support**: NBA, NFL, MLB, NHL, College Football, College Basketball, MLS, WNBA
- **Intelligent Table Detection**: Advanced scoring system to identify correct roster tables
- **BFS Crawling**: Systematic exploration to discover better data sources
- **League-Wide Crawling**: Crawl all teams in a sport with a single command
- **Comprehensive Data**: Player names, jersey numbers, positions, ages, heights, weights, colleges
- **Error Handling**: Robust error recovery and graceful degradation
- **Rate Limiting**: Respectful crawling with configurable delays

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/espn-sports-crawler.git
cd espn-sports-crawler

# Install dependencies
pip install -r requirements.txt
```

### Git Setup Commands

```bash
# Initialize repository (if starting fresh)
git init
git add .
git commit -m "Initial commit: ESPN Sports Web Crawler"

# Connect to GitHub repository
git remote add origin https://github.com/yourusername/espn-sports-crawler.git
git branch -M main
git push -u origin main

# Daily workflow commands
git status                          # Check file changes
git add .                          # Stage all changes
git add filename.py                # Stage specific file
git commit -m "Add new feature"    # Commit with message
git push                          # Push to GitHub
git pull                          # Pull latest changes

# Branch management
git checkout -b feature/new-crawler    # Create new branch
git checkout main                      # Switch to main branch
git merge feature/new-crawler          # Merge branch to main
git branch -d feature/new-crawler      # Delete merged branch

# View history and status
git log --oneline                  # View commit history
git diff                          # See uncommitted changes
git diff --staged                 # See staged changes
```

### Basic Usage

```bash
# Crawl a single team
python sports_crawler.py
# Enter: nba
# Enter: houston-rockets
# Enter: 8

# Crawl all teams in a league
python sports_crawler.py
# Enter: nba
# Enter: none
# Enter: 5
```

### Advanced Usage

```python
from sports_crawler import SportsCrawler

# Create crawler for specific team
crawler = SportsCrawler('nba', 'houston-rockets', 'hou')

# Crawl with custom settings
crawler.crawl(max_pages=10, delay=1)

# Access scraped data
print(f"Found {len(crawler.scraped_data['roster'])} players")
```
### Training Datasets

Screenshots before training
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d96aee73-a5da-4b9f-ada8-44406649b27b" />

Screenshots after training.
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/7cd071ba-0238-409e-8997-7074e0dbe7c5" />

Link to the full training set.
Using a train/validate/test split of 70/20/10

https://app.roboflow.com/basketballplayers-a5i9q/basketballtraditional-qgzma/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true

## Example Output

```
HOUSTON-ROCKETS ROSTER:
--------------------------------------------------------------------------------
Name                      Jersey   Pos   Age  Height   College
--------------------------------------------------------------------------------
Steven Adams              #12      C     32   6' 11"   Pittsburgh
Kevin Durant              #7       PF    37   6' 11"   Texas
Clint Capela              #30      C     31   6' 10"   --
Alperen Sengun            #28      C     22   6' 11"   --
Fred VanVleet             #5       PG    31   6' 0"    Wichita State
```

## Project Structure

```
espn-sports-crawler/
├── sports_crawler.py          # Main crawler with BFS and table detection
├── sports_webcrawl_fixed.py   # Simple single-team roster scraper
├── sports_data.py             # Team data for all major sports
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── docs/                      # Documentation
│   ├── table_detection_guide.py
│   ├── page_discovery_explanation.py
│   └── crawl_visualization.py
├── tests/                     # Test files
│   └── test_crawler_features.py
└── examples/                  # Example scripts
    └── sports_webcrawl.py     # Basic example
```

## How It Works

### 1. Intelligent Table Detection

The crawler uses a multi-strategy scoring system to identify correct roster tables:

- **Header Analysis** (30 points): Looks for roster-specific column headers
- **Jersey Numbers** (25 points): Finds ESPN's jersey number CSS classes
- **Player Links** (20 points): Identifies links to player profile pages
- **Data Patterns** (15 points): Matches height/weight patterns
- **Table Size** (10 points): Validates typical roster table dimensions

### 2. BFS URL Discovery

```
Main Page → Seed URLs → Alternative Formats → Quality Data
    ↓           ↓              ↓                  ↓
  Links     Wrong Format   Better URLs      Real Roster
```

The crawler discovers better URL formats through link following:
- Page 2: `/team/_/name/hou/houston-rockets/roster` (wrong format)
- Page 7: `/team/roster/_/name/hou/houston-rockets` (correct format)

### 3. Multi-Sport Architecture

Supports 200+ teams across 8 major sports with proper URL patterns and team abbreviations.

## Performance

- **Single Team**: 5-10 pages optimal (2-3 seconds)
- **League Crawl**: 30 teams × 5 pages = 150 pages (2-3 minutes)
- **Rate Limiting**: 1 request/second (respectful to ESPN)
- **Success Rate**: 90%+ for roster data, 80%+ for schedule data

## Use Cases

- **Sports Analytics**: Automated data collection for analysis
- **Fantasy Sports**: Real-time player information
- **Sports Journalism**: Comprehensive team databases
- **Research**: Academic sports data studies
- **Fan Websites**: Up-to-date roster information

## Advanced Features

### League-Wide Crawling

```python
# Crawl all NBA teams
python sports_crawler.py
# Enter: nba
# Enter: none
# Enter: 5

# Results saved to nba_league_data.txt
```

### Custom URL Patterns

```python
# Add custom include/exclude patterns
crawler.include_patterns.append(r'/custom-pattern/')
crawler.exclude_patterns.append(r'/avoid-this/')
```

### Data Export

```python
# Access structured data
roster_data = crawler.scraped_data['roster']
schedule_data = crawler.scraped_data['schedule']

# Export to JSON
import json
with open('team_data.json', 'w') as f:
    json.dump(crawler.scraped_data, f, indent=2)
```

## Configuration

### Crawler Settings

```python
crawler = SportsCrawler('nba', 'team-name', 'abbrev')

# Adjust crawling behavior
crawler.crawl(
    max_pages=10,        # Pages per team
    delay=1,             # Seconds between requests
)

# Modify URL patterns
crawler.include_patterns = [...]
crawler.exclude_patterns = [...]
```

### Supported Sports

| Sport | Teams | Example Team |
|-------|-------|--------------|
| NBA | 30 | houston-rockets |
| NFL | 32 | new-england-patriots |
| MLB | 30 | boston-red-sox |
| NHL | 32 | boston-bruins |
| College Football | 60+ | alabama-crimson-tide |
| College Basketball | 32+ | duke-blue-devils |
| MLS | 29 | atlanta-united-fc |
| WNBA | 12 | las-vegas-aces |

## Contributing

### Development Workflow

```bash
# Fork and clone your fork
git clone https://github.com/yourusername/espn-sports-crawler.git
cd espn-sports-crawler

# Set up upstream remote
git remote add upstream https://github.com/originalowner/espn-sports-crawler.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git add .
git commit -m "Add amazing feature: detailed description"

# Push to your fork
git push origin feature/amazing-feature

# Keep your fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Contribution Steps

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Make your changes and add tests
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request on GitHub

### Code Standards

```bash
# Run tests before committing
python -m pytest tests/

# Check code style
flake8 *.py

# Format code
black *.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This crawler is for educational and research purposes. Please respect ESPN's robots.txt and terms of service. Use appropriate delays and don't overload their servers.

## Acknowledgments

- ESPN for providing comprehensive sports data
- BeautifulSoup for HTML parsing
- My love for the Houston Rockets

## Support

### Getting Help

```bash
# Check issues for common problems
# https://github.com/yourusername/espn-sports-crawler/issues

# Create new issue for bugs
# Use the issue templates provided

# For questions, use discussions
# https://github.com/yourusername/espn-sports-crawler/discussions
```

### Repository Management

```bash
# Star the repository
# https://github.com/yourusername/espn-sports-crawler

# Watch for updates
# Click "Watch" button on GitHub

# Fork for contributions
# Click "Fork" button on GitHub
```

---

**Built for sports data enthusiasts and developers**
