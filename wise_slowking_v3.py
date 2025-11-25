import json
import random
import os
import time
import sys
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "v3.1-Demo-Pacing",
    "data_source": "real_data.json", 
    "thresholds": {
        "divergence": 5.0,     # 5% difference triggers message
        "scarcity": 5          # Critical supply count
    }
}

# ==========================================
# 2. VISUAL UTILS (MINIMALIST & PRO)
# ==========================================

def print_header():
    # Clean header, financial terminal style
    print("\n")
    print("="*60)
    print(f"   🐚  WISE SLOWKING | RWA MARKET INTELLIGENCE AGENT")
    print(f"   🔹  NETWORK: BASE MAINNET  |  STATUS: ONLINE")
    print("="*60)
    print("\n")

def loading_step(task_name):
    # Simulates technical connection steps
    sys.stdout.write(f"   [INIT] {task_name}...")
    sys.stdout.flush()
    time.sleep(0.8) # Delay for readability
    print(" OK")
    time.sleep(0.2)

# ==========================================
# 3. DATA ENGINE
# ==========================================

class MarketScanner:
    def scan(self) -> List[Dict]:
        if not os.path.exists(CONFIG["data_source"]):
            return []
        with open(CONFIG["data_source"], 'r') as f:
            data = json.load(f)
            # Pick 1 random card to simulate a live find
            return random.sample(data['cards'], 1)

# ==========================================
# 4. ANALYTICAL ENGINE
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
# 5. PERSONA ENGINE (ORACLE)
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
                f"🐚 THE BALANCE IS DISTURBED: {name}\n"
                f"   Physical: {p_ebay}  |  Digital ({rwa}): {p_rwa}\n"
                f"   🌀 Divergence: {pct:.1f}% (Undervalued On-Chain)\n"
                f"   Counsel: Bridge the realms. Restore value where it lies dormant."
            )
        elif analysis['insight'] == "OFF_CHAIN_DISCOUNT":
            return (
                f"💭 ILLUSION DETECTED: {name}\n"
                f"   Digital ({rwa}): {p_rwa}  |  Physical: {p_ebay}\n"
                f"   ⚠️ Premium: {pct:.1f}% (Overvalued On-Chain)\n"
                f"   Counsel: Do not be swayed. Seek the artifact in the physical world."
            )
        elif analysis['insight'] == "SCARCITY_WARNING":
            return (
                f"🔮 THE TIDE RECEDES: {name}\n"
                f"   On-Chain Vaults: Only {analysis['supply']['on_chain']} left\n"
                f"   Counsel: When the water vanishes, the rare stones are revealed."
            )
        else:
            return (
                f"🌊 HARMONY RESTORED: {name}\n"
                f"   Physical: {p_ebay}  |  Digital: {p_rwa}\n"
                f"   The currents are calm. True wisdom lies in patience."
            )

# ==========================================
# 6. EXECUTION (DEMO PACING MODE)
# ==========================================

if __name__ == "__main__":
    scanner = MarketScanner()
    analyzer = MarketAnalyzer()
    persona = WiseSlowkingPersona()
    
    # 1. Clean Startup
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header()
    
    # 2. Professional Loading Sequence
    loading_step("Connecting to Base Node Provider")
    loading_step("Authenticating with Beezie API")
    loading_step("Authenticating with eBay Developers Program")
    loading_step("Syncing Real-Time Order Books")
    
    print("\n   ✅ SYSTEM READY. EXECUTING AUTONOMOUS LOOP.\n")
    time.sleep(2) # Pausa dramática antes de começar

    # 3. The Monitor Loop
    try:
        while True:
            # Indicador de atividade (Aumentado para 2.5s para leitura)
            print("   > Scanning active liquidity pools...")
            time.sleep(2.5) 
            
            batch = scanner.scan()
            if batch:
                for card in batch:
                    result = analyzer.analyze(card)
                    tweet = persona.speak(result)
                    
                    print("-" * 60)
                    print(tweet)
                    print("-" * 60 + "\n")
            
            # PAUSA AUMENTADA: 8 Segundos para leitura e narração no vídeo
            time.sleep(8) 
            
    except KeyboardInterrupt:
        print("\n   🛑 Session Terminated by User.")
