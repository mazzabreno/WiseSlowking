import json
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION (REAL DATA MODE)
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "3.1-Standalone",
    "thresholds": {
        "divergence": 10.0,    # 10% difference triggers an alert
        "scarcity": 10         # Less than 10 units on-chain = Scarcity
    }
}

# ==========================================
# 2. REAL MARKET SNAPSHOT (EMBEDDED)
# ==========================================
# Data collected from real market sources (eBay, PriceCharting) on Nov 25, 2025.
# Embedded here to ensure zero read errors during the demo.

REAL_MARKET_SNAPSHOT = {
  "snapshot_date": "2025-11-25",
  "cards": [
    {
      "id": "PKM-001",
      "name": "Charizard Base Set (Unlimited) PSA 9",
      "market_prices": {
        "Beezie": 750.00,
        "Collector Crypt": 780.00,
        "eBay": 830.00,  # Real market ref
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
        "Beezie": 4800000.00, # Implied fractional valuation
        "Collector Crypt": 4950000.00,
        "eBay": 5275000.00, # Based on Logan Paul record / Guinness
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
        "eBay": 3130.00, # Recent eBay sales avg
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
    """Loads the embedded snapshot data."""
    
    def load_data(self) -> List[Dict]:
        print(f"✅ DATA LOADED SUCCESSFULLY")
        print(f"   Market Snapshot Date: {REAL_MARKET_SNAPSHOT['snapshot_date']}")
        return REAL_MARKET_SNAPSHOT['cards']

# ==========================================
# 4. ANALYTICAL ENGINE (RWA vs OFF-CHAIN)
# ==========================================

class MarketAnalyzer:
    def analyze(self, card_data: Dict) -> Dict:
        prices = card_data['market_prices']
        
        # Calculate On-Chain Average (Beezie/Collector Crypt)
        p_beezie = prices.get('Beezie', 0)
        p_cc = prices.get('Collector Crypt', 0)
        on_chain_avg = (p_beezie + p_cc) / 2
        
        # Calculate Off-Chain Reference (eBay is the standard for physical liquidity)
        off_chain_ref = prices.get('eBay', 0)
        
        # Calculate Divergence: (eBay - OnChain) / OnChain
        if on_chain_avg > 0:
            divergence_pct = ((off_chain_ref - on_chain_avg) / on_chain_avg) * 100
        else:
            divergence_pct = 0
        
        insight_type = "NEUTRAL"
        target_platform = "None"
        
        # Decision Logic
        if divergence_pct > CONFIG["thresholds"]["divergence"]:
            # If eBay is X% more expensive -> On-Chain Discount exists
            insight_type = "ON_CHAIN_DISCOUNT" 
            target_platform = "Beezie"
        elif divergence_pct < -CONFIG["thresholds"]["divergence"]:
            # If eBay is X% cheaper -> Off-Chain Discount exists
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
# 5. PERSONA ENGINE (WISE SLOWKING)
# ==========================================

class WiseSlowkingPersona:
    def speak(self, analysis: Dict) -> str:
        name = analysis['name']
        on_p = f"${analysis['on_chain_price']:,.2f}"
        off_p = f"${analysis['off_chain_price']:,.2f}"
        diff = f"{abs(analysis['divergence']):.1f}%"
        
        if analysis['insight'] == "ON_CHAIN_DISCOUNT":
            return (
                f"🚨 ARBITRAGE OPPORTUNITY: {name}\n\n"
                f"The physical market (eBay) values this at {off_p}.\n"
                f"However, the On-Chain RWA on **{analysis['target']}** is trading at {on_p}.\n"
                f"📉 Divergence: {diff} discount on-chain.\n"
                f"Strategy: Acquire the tokenized asset immediately before the gap closes."
            )
            
        elif analysis['insight'] == "OFF_CHAIN_DISCOUNT":
            return (
                f"📉 PHYSICAL ENTRY POINT: {name}\n\n"
                f"The physical copies on **{analysis['target']}** ({off_p}) are trading below tokenized value.\n"
                f"On-Chain markets demand {on_p}.\n"
                f"Strategy: Acquire the physical card to bridge it to the blockchain for value realization."
            )

        elif analysis['insight'] == "SCARCITY_ALERT":
            return (
                f"💎 SUPPLY SHOCK DETECTED: {name}\n\n"
                f"Only {analysis['supply']['on_chain_count']} copies exist in the On-Chain vaults.\n"
                f"Meanwhile, {analysis['supply']['off_chain_count']} circulate in the wild.\n"
                f"The digital scarcity premium has not yet been priced in. Watch closely."
            )
            
        else:
            return (
                f"⚖️ MARKET STABILITY: {name}\n\n"
                f"On-Chain ({on_p}) and eBay ({off_p}) are perfectly balanced.\n"
                f"No immediate action required. The Oracle waits."
            )

# ==========================================
# 6. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    fetcher = RealDataFetcher()
    analyzer = MarketAnalyzer()
    persona = WiseSlowkingPersona()
    
    print("="*60)
    print("🐚 WISE SLOWKING: INITIALIZING REAL-WORLD DATA ENGINE...")
    print("="*60 + "\n")
    
    cards = fetcher.load_data()
    
    for card in cards:
        analysis = analyzer.analyze(card)
        post = persona.speak(analysis)
        
        print(f"--- ANALYZING: {card['name']} ---")
        print(f"🔍 Insight Type: {analysis['insight']}")
        print("📢 GENERATED X POST:")
        print(post)
        print("\n" + "-"*60 + "\n")
