import json
import random
import os
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "6.0-Oracle-Persona",
    "data_source": "real_data.json", 
    "thresholds": {
        "divergence": 5.0,     # 5% difference triggers observation
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
        print(f"\n> GAZING INTO THE MARKET STREAMS (real_data.json)...")
        print(f"> OBSERVING THE FLOW OF VALUE...\n")
        
        if not os.path.exists(CONFIG["data_source"]):
            print(f"❌ ERROR: File {CONFIG['data_source']} not found.")
            return []

        with open(CONFIG["data_source"], 'r') as f:
            data = json.load(f)
            all_cards = data['cards']
            
        return random.sample(all_cards, 3)

# ==========================================
# 3. ANALYTICAL ENGINE
# ==========================================

class MarketAnalyzer:
    def analyze(self, card_data: Dict) -> Dict:
        prices = card_data['market_prices']
        rwa_plat = "Beezie" if "Beezie" in prices else "Collector Crypt"
        
        on_chain_p = prices[rwa_plat]
        off_chain_p = prices['eBay']
        
        # Calculate Percentage Difference
        diff_pct = ((off_chain_p - on_chain_p) / on_chain_p) * 100
        
        insight = "NEUTRAL"
        
        if diff_pct > CONFIG["thresholds"]["divergence"]:
            insight = "ON_CHAIN_DISCOUNT" 
        elif diff_pct < -CONFIG["thresholds"]["divergence"]:
            insight = "OFF_CHAIN_DISCOUNT" 
        elif card_data['supply']['on_chain'] < CONFIG["thresholds"]["scarcity"]:
            insight = "SCARCITY_WARNING" 
            
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
# 4. PERSONA ENGINE (THE WISE ORACLE)
# ==========================================

class WiseSlowkingPersona:
    def speak(self, analysis: Dict) -> str:
        name = analysis['name']
        rwa = analysis['rwa_plat']
        p_rwa = f"${analysis['on_chain_p']:,.2f}"
        p_ebay = f"${analysis['off_chain_p']:,.2f}"
        pct = abs(analysis['diff_pct'])
        
        # O Slowking fala sobre "Mundos" (Físico vs Digital) e "Equilíbrio".
        
        if analysis['insight'] == "ON_CHAIN_DISCOUNT":
            return (
                f"🚨 THE BALANCE IS DISTURBED: {name}\n\n"
                f"The Physical Realm demands {p_ebay}, yet the Digital Vaults of {rwa} ask only {p_rwa}.\n\n"
                f"📉 A divergence of {pct:.1f}% reveals a hidden truth.\n"
                f"Counsel: Bridge the realms. Restore value where it lies dormant."
            )
        
        elif analysis['insight'] == "OFF_CHAIN_DISCOUNT":
            return (
                f"⚠️ ILLUSION DETECTED: {name}\n\n"
                f"The Digital price ({p_rwa}) has drifted far from the Physical truth ({p_ebay}).\n\n"
                f"The waters here are treacherous ({pct:.1f}% premium).\n"
                f"Counsel: Do not be swayed. Seek the artifact in the physical world."
            )
            
        elif analysis['insight'] == "SCARCITY_WARNING":
            return (
                f"💎 A DROUGHT APPROACHES: {name}\n\n"
                f"The On-Chain Vaults hold but {analysis['supply']['on_chain']} remnants.\n"
                f"The physical supply ({analysis['supply']['off_chain']}) flows freely, but here it dries up.\n\n"
                f"Counsel: When the tide recedes, the rare stones are revealed. Watch closely."
            )
            
        else:
            return (
                f"⚖️ HARMONY RESTORED: {name}\n\n"
                f"The Physical ({p_ebay}) and the Digital ({p_rwa}) sing in unison.\n\n"
                f"The currents are calm. True wisdom lies in patience."
            )

# ==========================================
# 5. EXECUTION
# ==========================================

if __name__ == "__main__":
    scanner = MarketScanner()
    analyzer = MarketAnalyzer()
    persona = WiseSlowkingPersona()
    
    batch = scanner.scan()
    
    if batch:
        for card in batch:
            result = analyzer.analyze(card)
            tweet = persona.speak(result)
            
            print(tweet)
            print("\n" + " "*20 + "* * *\n")
    else:
        print("The mists obscure my vision (No cards found).")
