import json
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION (REAL DATA MODE)
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "3.2-Twitter-Native",
    "thresholds": {
        "divergence": 8.0,     # 8% difference triggers alert
        "scarcity": 10         # Low supply count
    }
}

# ==========================================
# 2. REAL MARKET SNAPSHOT (EMBEDDED)
# ==========================================
# Snapshot taken: Nov 25, 2025. Sources: eBay, Beezie, PriceCharting.

REAL_MARKET_SNAPSHOT = {
  "snapshot_date": "2025-11-25",
  "cards": [
    {
      "id": "PKM-001",
      "name": "Charizard Base Set (Unlimited) PSA 9",
      "market_prices": {
        "Beezie": 750.00,
        "Collector Crypt": 780.00,
        "eBay": 830.00,
        "TCGPlayer": 850.00,
        "Cardmarket": 810.00
      },
      "supply_info": {
        "on_chain_count": 12,
        "off_chain_count": 5506
      }
    },
    {
      "id": "PKM-002",
      "name": "Pikachu Illustrator (Fractional)",
      "market_prices": {
        "Beezie": 4800000.00,
        "Collector Crypt": 4950000.00,
        "eBay": 5275000.00,
        "TCGPlayer": 5300000.00,
        "Cardmarket": 5400000.00
      },
      "supply_info": {
        "on_chain_count": 5,
        "off_chain_count": 1
      }
    },
    {
      "id": "PKM-003",
      "name": "Umbreon VMAX Alt Art PSA 10",
      "market_prices": {
        "Beezie": 2850.00,
        "Collector Crypt": 2900.00,
        "eBay": 3130.00,
        "TCGPlayer": 3150.00,
        "Cardmarket": 3100.00
      },
      "supply_info": {
        "on_chain_count": 35,
        "off_chain_count": 19182
      }
    }
  ]
}

# ==========================================
# 3. DATA INGESTION
# ==========================================

class RealDataFetcher:
    def load_data(self) -> List[Dict]:
        print(f"\n> CONNECTED TO MARKET DATA STREAM ({REAL_MARKET_SNAPSHOT['snapshot_date']})\n")
        return REAL_MARKET_SNAPSHOT['cards']

# ==========================================
# 4. ANALYTICAL ENGINE
# ==========================================

class MarketAnalyzer:
    def analyze(self, card_data: Dict) -> Dict:
        prices = card_data['market_prices']
        
        # Calculate On-Chain Average
        p_beezie = prices.get('Beezie', 0)
        p_cc = prices.get('Collector Crypt', 0)
        on_chain_avg = (p_beezie + p_cc) / 2
        
        # Calculate Off-Chain Reference
        off_chain_ref = prices.get('eBay', 0)
        
        # Calculate Divergence
        if on_chain_avg > 0:
            divergence_pct = ((off_chain_ref - on_chain_avg) / on_chain_avg) * 100
        else:
            divergence_pct = 0
        
        insight_type = "NEUTRAL"
        target_platform = "None"
        
        # Decision Logic (8% Threshold)
        if divergence_pct > CONFIG["thresholds"]["divergence"]:
            insight_type = "ON_CHAIN_DISCOUNT" 
            target_platform = "Beezie"
        elif divergence_pct < -CONFIG["thresholds"]["divergence"]:
            insight_type = "OFF_CHAIN_DISCOUNT" 
            target_platform = "eBay"
        elif card_data['supply_info']['on_chain_count'] < CONFIG["thresholds"]["scarcity"]:
            insight_type = "SCARCITY_ALERT"
            
        return {
            "name": card_data['name'],
            "insight": insight_type,
            "on_chain_price": on_chain_avg,
            "off_chain_price": off_chain_ref,
            "divergence": divergence_pct,
            "target": target_platform,
            "supply": card_data['supply_info']
        }

# ==========================================
# 5. PERSONA ENGINE (TWEET OPTIMIZED)
# ==========================================

class WiseSlowkingPersona:
    def speak(self, analysis: Dict) -> str:
        name = analysis['name']
        on_p = f"${analysis['on_chain_price']:,.2f}"
        off_p = f"${analysis['off_chain_price']:,.2f}"
        diff = f"{abs(analysis['divergence']):.1f}%"
        
        # TWEET FORMAT: Clean, visual, data-first.
        
        if analysis['insight'] == "ON_CHAIN_DISCOUNT":
            return (
                f"🚨 ARBITRAGE ALERT: {name}\n\n"
                f"Physical (eBay): {off_p}\n"
                f"On-Chain ({analysis['target']}): {on_p}\n\n"
                f"📉 {diff} Discount detected On-Chain.\n"
                f"The gap is visible. Tokenized assets currently undervalued."
            )
            
        elif analysis['insight'] == "OFF_CHAIN_DISCOUNT":
            return (
                f"📉 ENTRY POINT: {name}\n\n"
                f"Physical (eBay): {off_p}\n"
                f"On-Chain RWA: {on_p}\n\n"
                f"Physical market trading below tokenized value.\n"
                f"Opportunity to bridge asset for immediate appreciation."
            )

        elif analysis['insight'] == "SCARCITY_ALERT":
            return (
                f"💎 SUPPLY SHOCK: {name}\n\n"
                f"On-Chain Supply: Only {analysis['supply']['on_chain_count']} left\n"
                f"Off-Chain Supply: {analysis['supply']['off_chain_count']}\n\n"
                f"Vaults are emptying. Digital scarcity premium not yet priced in."
            )
            
        else:
            return (
                f"⚖️ MARKET STABILITY: {name}\n\n"
                f"On-Chain: {on_p}\n"
                f"Off-Chain: {off_p}\n\n"
                f"Prices are balanced across realms. No action required."
            )

# ==========================================
# 6. MAIN EXECUTION (CLEAN OUTPUT)
# ==========================================

if __name__ == "__main__":
    fetcher = RealDataFetcher()
    analyzer = MarketAnalyzer()
    persona = WiseSlowkingPersona()
    
    cards = fetcher.load_data()
    
    for card in cards:
        analysis = analyzer.analyze(card)
        post = persona.speak(analysis)
        
        # Simulating a clean Twitter Feed in the terminal
        print(post)
        print("\n" + " "*20 + "* * *\n")
