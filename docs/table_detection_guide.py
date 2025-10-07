"""
Guide: How to Improve Table Detection for Sports Roster Data
This shows what to look for to identify the correct roster table
"""

import requests
from bs4 import BeautifulSoup

def analyze_table_characteristics():
    """Analyze what makes a roster table different from other tables"""
    
    print("🔍 TABLE DETECTION IMPROVEMENT GUIDE")
    print("="*60)
    
    # What we need to look for in roster tables
    roster_table_indicators = {
        'headers': {
            'description': 'Column headers that indicate player data',
            'examples': ['Name', 'Player', '#', 'No', 'Pos', 'Position', 'Age', 'Ht', 'Height', 'Wt', 'Weight', 'College', 'Exp'],
            'detection_method': 'Check first row (thead or first tr) for these keywords'
        },
        
        'jersey_numbers': {
            'description': 'Cells containing jersey numbers with specific CSS classes',
            'examples': ['pl2 n10', 'jersey-number', 'player-number'],
            'detection_method': 'Look for <span class="pl2 n10">25</span> patterns'
        },
        
        'player_names': {
            'description': 'Cells with player name links',
            'examples': ['<a href="/nba/player/_/id/123/player-name">Player Name</a>'],
            'detection_method': 'Look for links to player profile pages'
        },
        
        'table_structure': {
            'description': 'Roster tables have specific column counts and data patterns',
            'examples': ['6-8 columns typically', '15-20 rows for full roster'],
            'detection_method': 'Count columns and validate data types'
        },
        
        'css_classes': {
            'description': 'ESPN uses specific CSS classes for roster tables',
            'examples': ['Table', 'Table--align-right', 'roster-table'],
            'detection_method': 'Check table class attributes'
        },
        
        'data_patterns': {
            'description': 'Roster data has predictable patterns',
            'examples': ['Heights like "6\' 8\"', 'Weights like "210 lbs"', 'Ages 18-40'],
            'detection_method': 'Validate cell content matches expected patterns'
        }
    }
    
    print("\n📊 ROSTER TABLE INDICATORS:")
    print("-" * 40)
    
    for indicator, details in roster_table_indicators.items():
        print(f"\n{indicator.upper().replace('_', ' ')}:")
        print(f"  Description: {details['description']}")
        print(f"  Examples: {details['examples']}")
        print(f"  Detection: {details['detection_method']}")
    
    return roster_table_indicators

def demonstrate_table_detection_logic():
    """Show improved table detection logic"""
    
    print(f"\n🔧 IMPROVED TABLE DETECTION LOGIC:")
    print("-" * 50)
    
    detection_code = '''
def find_roster_table(soup):
    """Improved roster table detection"""
    
    # 1. HEADER-BASED DETECTION
    roster_headers = ['name', 'player', '#', 'no', 'pos', 'position', 'age', 'height', 'weight', 'college']
    
    tables = soup.find_all('table')
    for table in tables:
        # Check table headers
        header_row = table.find('thead') or table.find('tr')
        if header_row:
            header_text = header_row.get_text().lower()
            header_matches = sum(1 for header in roster_headers if header in header_text)
            
            if header_matches >= 3:  # At least 3 roster-related headers
                print(f"✅ Found roster table by headers: {header_matches} matches")
                return table
    
    # 2. JERSEY NUMBER DETECTION
    for table in tables:
        jersey_elements = table.find_all(class_='pl2 n10')  # ESPN's jersey number class
        if len(jersey_elements) >= 5:  # At least 5 players with jersey numbers
            print(f"✅ Found roster table by jersey numbers: {len(jersey_elements)} found")
            return table
    
    # 3. PLAYER LINK DETECTION
    for table in tables:
        player_links = table.find_all('a', href=lambda x: x and '/player/' in x)
        if len(player_links) >= 5:  # At least 5 player profile links
            print(f"✅ Found roster table by player links: {len(player_links)} found")
            return table
    
    # 4. DATA PATTERN DETECTION
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header
        height_pattern_matches = 0
        
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                text = cell.get_text()
                # Look for height patterns like "6' 8\"" or "6-8"
                if "'" in text or (len(text) == 3 and '-' in text):
                    height_pattern_matches += 1
                    break
        
        if height_pattern_matches >= 5:  # At least 5 height entries
            print(f"✅ Found roster table by height patterns: {height_pattern_matches} found")
            return table
    
    # 5. FALLBACK: LARGEST TABLE
    if tables:
        largest_table = max(tables, key=lambda t: len(t.find_all('tr')))
        print(f"⚠️  Using largest table as fallback: {len(largest_table.find_all('tr'))} rows")
        return largest_table
    
    return None
    '''
    
    print(detection_code)

def show_wrong_vs_right_tables():
    """Show examples of wrong tables vs right tables"""
    
    print(f"\n❌ WRONG TABLES (What to Avoid):")
    print("-" * 40)
    
    wrong_tables = {
        'standings': {
            'description': 'Team standings/records table',
            'example_data': ['Team', 'W', 'L', 'PCT', 'GB'],
            'why_wrong': 'Contains team names, not player names'
        },
        'schedule': {
            'description': 'Game schedule table', 
            'example_data': ['Date', 'Opponent', 'Result', 'Score'],
            'why_wrong': 'Contains game data, not player data'
        },
        'stats_summary': {
            'description': 'Team statistics summary',
            'example_data': ['PPG', 'RPG', 'APG', 'FG%'],
            'why_wrong': 'Contains aggregate stats, not individual players'
        },
        'navigation': {
            'description': 'Navigation or menu tables',
            'example_data': ['Home', 'Schedule', 'Roster', 'Stats'],
            'why_wrong': 'Contains navigation links, not data'
        }
    }
    
    for table_type, details in wrong_tables.items():
        print(f"\n{table_type.upper()}:")
        print(f"  Description: {details['description']}")
        print(f"  Example Data: {details['example_data']}")
        print(f"  Why Wrong: {details['why_wrong']}")
    
    print(f"\n✅ RIGHT TABLE (What to Find):")
    print("-" * 40)
    
    right_table = {
        'description': 'Player roster table',
        'example_data': ['Player Name', '#25', 'PG', '28', '6\' 2"', '185 lbs', 'Duke'],
        'characteristics': [
            'Player names (often as links)',
            'Jersey numbers (#1, #23, etc.)',
            'Positions (PG, SG, SF, PF, C)',
            'Ages (18-40 range)',
            'Heights (feet/inches format)',
            'Weights (lbs format)', 
            'Colleges/Schools'
        ]
    }
    
    print(f"ROSTER TABLE:")
    print(f"  Description: {right_table['description']}")
    print(f"  Example Row: {right_table['example_data']}")
    print(f"  Characteristics:")
    for char in right_table['characteristics']:
        print(f"    • {char}")

def create_improved_detection_function():
    """Create the actual improved detection function"""
    
    print(f"\n🚀 COMPLETE IMPROVED DETECTION FUNCTION:")
    print("-" * 50)
    
    improved_function = '''
def find_roster_table_improved(soup):
    """
    Improved roster table detection using multiple strategies
    Returns the table most likely to contain roster data
    """
    
    tables = soup.find_all('table')
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
    '''
    
    print(improved_function)

def main():
    """Run the complete table detection guide"""
    
    analyze_table_characteristics()
    demonstrate_table_detection_logic()
    show_wrong_vs_right_tables()
    create_improved_detection_function()
    
    print(f"\n🎯 SUMMARY: KEY IMPROVEMENTS NEEDED")
    print("="*50)
    print("1. ✅ Multi-strategy detection (headers + jersey numbers + links)")
    print("2. ✅ Scoring system to rank tables by likelihood")
    print("3. ✅ Pattern matching for heights, weights, ages")
    print("4. ✅ Validation of table size and structure")
    print("5. ✅ Fallback strategies when primary detection fails")
    print("6. ✅ Debug output to understand why tables are selected")

if __name__ == "__main__":
    main()