"""
Visual representation of how page limits affect data discovery
"""

def show_crawl_tree():
    """Show the crawl discovery tree"""
    
    print("🌳 CRAWL DISCOVERY TREE - Houston Rockets Example")
    print("="*70)
    
    tree = """
    
🏠 START: Main Team Page
│   https://www.espn.com/nba/team/_/name/hou/houston-rockets
│
├─📄 Page 2: Seed Roster (WRONG FORMAT)
│   │   https://www.espn.com/nba/team/_/name/hou/houston-rockets/roster
│   │   Table Score: 5/100 ❌
│   │   Data: ['1', '0', '0'] (numbers, not names)
│   │   Players Found: 0
│   │
│   ├─🔗 Discovers: /team/schedule/_/name/...
│   ├─🔗 Discovers: /team/stats/_/name/...
│   └─🔗 Discovers: /player/_/id/123/...
│
├─📄 Page 3: Schedule
│   │   https://www.espn.com/nba/team/_/name/hou/houston-rockets/schedule
│   │   ✅ Schedule Data: 5 games found
│   │
│   ├─🔗 Discovers: /team/roster/_/name/... (BETTER FORMAT!)
│   ├─🔗 Discovers: /game/_/gameId/...
│   └─🔗 Discovers: /team/injuries/_/name/...
│
├─📄 Page 4-6: Stats & Other Pages
│   │   Various stats and team pages
│   │   ✅ More links discovered
│   │
│   └─🔗 Queue grows to 40+ URLs
│
└─🎯 Page 7: REAL ROSTER PAGE (SUCCESS!)
    │   https://www.espn.com/nba/team/roster/_/name/hou/houston-rockets
    │   Table Score: 100/100 ✅
    │   Data: ['Steven Adams', 'Kevin Durant', 'Clint Capela']
    │   Players Found: 18 🎉
    │
    ├─🔗 Discovers: /player/_/id/456/steven-adams
    ├─🔗 Discovers: /player/_/id/789/kevin-durant
    ├─🔗 Discovers: /team/depth/_/name/...
    └─🔗 Queue grows to 80+ URLs
    
    """
    
    print(tree)

def show_page_limit_comparison():
    """Show side-by-side comparison of different page limits"""
    
    print("\n📊 PAGE LIMIT COMPARISON")
    print("="*70)
    
    comparison = """
    
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   2 PAGES   │   5 PAGES   │   8 PAGES   │  15 PAGES   │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ ❌ Stops at  │ ⚠️  Reaches  │ ✅ Finds     │ 🎯 Deep      │
│ seed URLs   │ some alts   │ real data   │ exploration │
│             │             │             │             │
│ Players: 0  │ Players: 0  │ Players: 18 │ Players: 18+│
│ Schedule: 0 │ Schedule: 5 │ Schedule: 10│ Schedule: 15│
│ News: 0     │ News: 0     │ News: 0     │ News: 5     │
│             │             │             │             │
│ Quality:    │ Quality:    │ Quality:    │ Quality:    │
│ Poor ❌     │ Partial ⚠️   │ Good ✅     │ Excellent 🎯│
│             │             │             │             │
│ Speed:      │ Speed:      │ Speed:      │ Speed:      │
│ Fast ⚡     │ Medium 🚶   │ Balanced ⚖️ │ Slow 🐌     │
└─────────────┴─────────────┴─────────────┴─────────────┘

RECOMMENDATION: 5-8 pages for single teams, 3-5 for league crawls
    
    """
    
    print(comparison)

def show_url_discovery_timeline():
    """Show when different URL formats are discovered"""
    
    print("\n⏰ URL DISCOVERY TIMELINE")
    print("="*70)
    
    timeline = """
    
Page 1: 🏠 Main Page
        └─ Seed URLs added to queue
        
Page 2: 📄 /team/_/name/hou/houston-rockets/roster
        ├─ ❌ Wrong format (schedule data)
        └─ Discovers 3 new URLs
        
Page 3: 📄 /team/_/name/hou/houston-rockets/schedule  
        ├─ ✅ Schedule data found
        └─ 🔗 KEY: Discovers /team/roster/_/name/... format
        
Page 4-6: 📄 Stats & Other Pages
          └─ Queue builds up with discovered URLs
          
Page 7: 🎯 /team/roster/_/name/hou/houston-rockets
        ├─ ✅ JACKPOT: Real roster table found!
        ├─ 18 players with complete stats
        └─ Discovers 39 more URLs (player profiles)

WHY PAGE 7 IS DIFFERENT:
• Different URL structure: /team/roster/_/name/ vs /team/_/name/.../roster
• Different page template: Full roster vs summary page  
• Different table format: Complete player data vs preview data
• Only discoverable through link following from other pages!
    
    """
    
    print(timeline)

def show_data_quality_progression():
    """Show how data quality improves with more pages"""
    
    print("\n📈 DATA QUALITY PROGRESSION")
    print("="*70)
    
    progression = """
    
Page Limit │ Data Quality │ What You Get
───────────┼──────────────┼─────────────────────────────────────
    1-2    │     ★☆☆☆☆    │ Seed URLs only, often wrong format
           │              │ Example: Schedule data instead of roster
           │              │
    3-4    │     ★★☆☆☆    │ Some alternative URLs discovered  
           │              │ Example: Schedule found, roster still wrong
           │              │
    5-7    │     ★★★★☆    │ Good URL discovery, finds correct formats
           │              │ Example: Real roster page discovered
           │              │
    8-12   │     ★★★★★    │ Comprehensive data across all sections
           │              │ Example: Roster + Schedule + Depth + Injuries
           │              │
   13-20   │     ★★★★★    │ Deep exploration, player profiles
           │              │ Example: Individual player career stats
           │              │
    20+    │     ★★★☆☆    │ Diminishing returns, irrelevant pages
           │              │ Example: Old news, other teams, ads

SWEET SPOT: 5-10 pages per team for optimal data/speed ratio
    
    """
    
    print(progression)

def main():
    """Show all visualizations"""
    
    show_crawl_tree()
    show_page_limit_comparison() 
    show_url_discovery_timeline()
    show_data_quality_progression()
    
    print("\n🎯 SUMMARY: WHY MORE PAGES = MORE DATA")
    print("="*70)
    print("1. 🔗 BFS discovers NEW URL formats through link following")
    print("2. 📄 ESPN has MULTIPLE pages for the same data type")
    print("3. 🎯 BETTER formats are often 3-7 links deep")
    print("4. ⚖️ Page 2 ≠ Page 7 (different URLs, different data)")
    print("5. 🏆 Real roster page found at Page 7, not Page 2")
    print("6. 📊 More pages = More chances to find QUALITY data")

if __name__ == "__main__":
    main()