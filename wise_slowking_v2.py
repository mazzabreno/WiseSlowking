import json
import random
import os
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "5.0-Json-Scanner",
    "data_source": "real_data.json", # Lê o arquivo externo
    "thresholds": {
        "divergence": 5.0,     # 5% difference triggers alert
        "scarcity": 5          # Critical supply count
    }
}

# ==========================================
# 2. DATA LOADER & RANDOMIZER
# ==========================================

class MarketScanner:
    """
    Loads the full database from JSON and selects a random batch to simulate a live scan.
    """
    def scan(self) -> List[Dict]:
        print(f"\n> CONNECTED TO REAL MARKET DATABASE (real_data.json)...")
        print(f"> SYNCING WALLETS & MARKETPLACES...\n")
        
        if not os.path.exists(CONFIG["data_source"]):
            print(f"❌ ERROR: File {CONFIG['data_source']} not found.")
            return []

        with open(CONFIG["data_source"], 'r') as f:
            data = json.load(f)
            all_cards = data['cards']
            
        # Select 3 random cards to analyze in this "Tweet Batch"
        # This creates dynamic variety every time you run the script.
        return random.sample(all_cards, 3)

# ==========================================
# 3. ANALYTICAL ENGINE
# ==========================================

class MarketAnalyzer:
    def analyze(self, card_data: Dict) -> Dict:
        prices = card_data['market_prices']
        
        # Identify which RWA platform is listed in the JSON for this card
        rwa_plat = "Beezie" if "Beezie" in prices else "Collector Crypt"
        
        on_chain_p = prices[rwa_plat]
        off_chain_p = prices['eBay']
        
        # Calculate Percentage Difference
        # Formula: (Physical - RWA) / RWA
        diff_pct = ((off_chain_p - on_chain_p) / on_chain_p) * 100
        
        insight = "NEUTRAL"
        
        # Logic: 
        if diff_pct > CONFIG["thresholds"]["divergence"]:
            insight = "ON_CHAIN_DISCOUNT" # RWA is cheaper (Arbitrage)
        elif diff_pct < -CONFIG["thresholds"]["divergence"]:
            insight = "OFF_CHAIN_DISCOUNT" # eBay is cheaper (Premium Warning)
        elif card_data['supply']['on_chain'] < CONFIG["thresholds"]["scarcity"]:
            insight = "SCARCITY_WARNING" # Low Supply
            
        return {
            "name": card_data['name'],
            "insight": insight,
            "on_chain_p": on_chain_p,
            "off_chain_p": off_chain_p,
            "diff_pct": diff_pct,
            "rwa_plat": rwa_plat,
            "supply": card_data['supply']
        }

# ==========================================
# 4. PERSONA ENGINE (Direct & Clean)
# ==========================================

class WiseSlowkingPersona:
    def speak(self, analysis: Dict) -> str:
        name = analysis['name']
        rwa = analysis['rwa_plat']
        p_rwa = f"${analysis['on_chain_p']:,.2f}"
        p_ebay = f"${analysis['off_chain_p']:,.2f}"
        pct = abs(analysis['diff_pct'])
        
        if analysis['insight'] == "ON_CHAIN_DISCOUNT":
            return (
                f"🚨 ARBITRAGE DETECTED: {name}\n\n"
                f"Physical (eBay Sold): {p_ebay}\n"
                f"On-Chain ({rwa}): {p_rwa}\n\n"
                f"📉 {pct:.1f}% Spread. The tokenized asset is undervalued.\n"
                f"Action: Bridge to RWA for immediate equity."
            )
        
        elif analysis['insight'] == "OFF_CHAIN_DISCOUNT":
            return (
                f"⚠️ PREMIUM WARNING: {name}\n\n"
                f"On-Chain ({rwa}): {p_rwa}\n"
                f"Physical (eBay Sold): {p_ebay}\n\n"
                f"RWA listing is trading {pct:.1f}% above real market value.\n"
                f"Action: Do not overpay. Source physically."
            )
            
        elif analysis['insight'] == "SCARCITY_WARNING":
            return (
                f"💎 SUPPLY SHOCK: {name}\n\n"
                f"On-Chain Vaults: Only {analysis['supply']['on_chain']} left\n"
                f"eBay Listings: {analysis['supply']['off_chain']}\n\n"
                f"Prices are stable, but RWA supply is critical.\n"
                f"Action: Monitor closely for liquidity crunch."
            )
            
        else:
            return (
                f"⚖️ FAIR VALUE: {name}\n\n"
                f"On-Chain ({rwa}): {p_rwa}\n"
                f"Physical (eBay): {p_ebay}\n\n"
                f"Market is efficient. Prices are aligned."
            )

# ==========================================
# 5. EXECUTION
# ==========================================

if __name__ == "__main__":
    scanner = MarketScanner()
    analyzer = MarketAnalyzer()
    persona = WiseSlowkingPersona()
    
    # 1. Get random sample from JSON File
    batch = scanner.scan()
    
    # 2. Process
    if batch:
        for card in batch:
            result = analyzer.analyze(card)
            tweet = persona.speak(result)
            
            print(tweet)
            print("\n" + " "*20 + "* * *\n")
    else:
        print("No cards found.")
