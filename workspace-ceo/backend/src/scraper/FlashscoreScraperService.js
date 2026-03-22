import { chromium } from 'playwright';
import { getMatchLinks, getMatchData } from '../../flashscore-scraping/src/scraper/services/matches/index.js';
import { config } from 'dotenv';

config();

class FlashscoreScraperService {
  constructor() {
    this.browser = null;
    this.context = null;
    this.config = {
      country: process.env.COUNTRY || 'czechia',
      league: process.env.LEAGUE || 'czech-liga-2025-2026',
      concurrency: 10,
      headless: process.env.PLAYWRIGHT_HEADLESS !== 'false',
      updateInterval: parseInt(process.env.UPDATE_INTERVAL) || 30000, // 30 seconds
    };
    
    this.matchesCache = new Map();
    this.updateIntervalId = null;
  }
  
  async initialize() {
    console.log('🔧 Initializing FlashscoreScraperService...');
    console.log(`📋 Config: country=${this.config.country}, league=${this.config.league}`);
    
    this.browser = await chromium.launch({ headless: this.config.headless });
    this.context = await this.browser.newContext();
    
    console.log('✅ FlashscoreScraperService initialized');
    return true;
  }
  
  async getLiveMatches() {
    console.log('🏈 Fetching live matches...');
    
    try {
      const leagueSeasonUrl = this._getLeagueSeasonUrl();
      
      const matchLinksFixtures = await getMatchLinks(
        this.context,
        leagueSeasonUrl,
        'fixtures'
      );
      
      const matchLinksResults = await getMatchLinks(
        this.context,
        leagueSeasonUrl,
        'results'
      );
      
      const matchLinks = [...matchLinksFixtures, ...matchLinksResults];
      
      if (matchLinks.length === 0) {
        console.log('⚠️ No matches found');
        return [];
      }
      
      const matches = await this._processMatches(matchLinks);
      
      // Cache matches
      matches.forEach(match => {
        this.matchesCache.set(match.matchId, match);
      });
      
      console.log(`✅ Fetched ${matches.length} matches`);
      return matches;
      
    } catch (error) {
      console.error('❌ Error fetching matches:', error);
      throw error;
    }
  }
  
  async getMatchById(matchId) {
    console.log(`🔍 Getting match ${matchId}...`);
    
    const cachedMatch = this.matchesCache.get(matchId);
    if (cachedMatch) {
      return cachedMatch;
    }
    
    // Try to fetch from live data
    const matches = await this.getLiveMatches();
    return matches.find(m => m.matchId === matchId) || null;
  }
  
  async refresh() {
    console.log('🔄 Refreshing matches...');
    return await this.getLiveMatches();
  }
  
  async updateConfig(country = null, league = null) {
    if (country) {
      this.config.country = country;
    }
    if (league) {
      this.config.league = league;
    }
    
    console.log(`✅ Config updated: country=${this.config.country}, league=${this.config.league}`);
  }
  
  startBackgroundUpdates() {
    console.log(`🔄 Starting background updates (${this.config.updateInterval}ms)...`);
    
    // Initial fetch
    this.getLiveMatches();
    
    // Set interval
    this.updateIntervalId = setInterval(() => {
      this.getLiveMatches().catch(err => {
        console.error('Background update failed:', err);
      });
    }, this.config.updateInterval);
  }
  
  stopBackgroundUpdates() {
    if (this.updateIntervalId) {
      clearInterval(this.updateIntervalId);
      this.updateIntervalId = null;
      console.log('✅ Background updates stopped');
    }
  }
  
  async close() {
    console.log('👋 Closing FlashscoreScraperService...');
    
    this.stopBackgroundUpdates();
    
    if (this.context) {
      await this.context.close();
    }
    
    if (this.browser) {
      await this.browser.close();
    }
    
    console.log('✅ FlashscoreScraperService closed');
  }
  
  _getLeagueSeasonUrl() {
    // Map country and league to Flashscore URL
    const baseUrl = 'https://www.flashscore.co.uk';
    
    const leaguePaths = {
      'czech-liga-2025-2026': '/football/czechia/czech-liga/2025-2026/',
      'premier-league-2025-2026': '/football/england/premier-league/2025-2026/',
      'la-liga-2025-2026': '/football/spain/la-liga/2025-2026/',
      'serie-a-2025-2026': '/football/italy/serie-a/2025-2026/',
      'bundesliga-2025-2026': '/football/germany/bundesliga/2025-2026/',
      'ligue-1-2025-2026': '/football/france/ligue-1/2025-2026/',
    };
    
    const leaguePath = leaguePaths[this.config.league];
    
    if (!leaguePath) {
      console.warn(`⚠️ Unknown league: ${this.config.league}, using default`);
      return baseUrl;
    }
    
    return baseUrl + leaguePath;
  }
  
  async _processMatches(matchLinks) {
    const matches = [];
    
    for (const link of matchLinks) {
      try {
        const matchData = await getMatchData(this.context, link);
        
        const match = {
          matchId: matchData.matchId,
          home_team: matchData.home?.name || 'Unknown',
          away_team: matchData.away?.name || 'Unknown',
          home_score: matchData.result?.home || 0,
          away_score: matchData.result?.away || 0,
          minute: this._extractMinute(matchData.status),
          league: this.config.league,
          started_at: matchData.date,
          status: matchData.status,
          stage: matchData.stage,
          statistics: matchData.statistics || [],
          information: matchData.information || [],
        };
        
        matches.push(match);
        
      } catch (error) {
        console.error(`Error processing match ${link.id}:`, error);
        continue;
      }
    }
    
    return matches;
  }
  
  _extractMinute(status) {
    const statusUpper = status.toUpperCase();
    
    if (statusUpper === 'LIVE' || statusUpper === 'PLAYING' || statusUpper === 'IN-PLAY') {
      return 0;
    } else if (statusUpper === 'FINISHED' || statusUpper === 'AFTER PENALTIES' || statusUpper === 'ENDED') {
      return 90;
    } else if (statusUpper.includes('MIN')) {
      const match = statusUpper.match(/(\d+)/);
      return match ? parseInt(match[1]) : 0;
    }
    
    return 0;
  }
  
  getMatchesCache() {
    return Array.from(this.matchesCache.values());
  }
  
  getHealthStatus() {
    return {
      scraper: 'FlashscoreScraperService',
      version: '1.0.0',
      browser: this.browser ? 'connected' : 'disconnected',
      cacheSize: this.matchesCache.size,
      config: {
        country: this.config.country,
        league: this.config.league,
      },
    };
  }
}

export { FlashscoreScraperService };
