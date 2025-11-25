import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ==========================================
# 1. CONFIGURATION & CONSTANTS
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "1.2.0-Alpha",
    "ecosystem": "Base Network",
    "thresholds": {
        "divergence_critical": 15.0,  # % difference to trigger alert
        "divergence_warning": 5.0,    # % difference to trigger observation
        "volatility_high": 10.0,      # Standard deviation % indicating instability
        "liquidity_drop": -20.0       # % volume drop indicating drying up
    },
    "data_sources": {
        "on_chain": ["Beezie", "Collector_Crypt"],
        "off_chain": ["eBay", "TCGPlayer", "Cardmarket"]
    }
}

# The "Database" of cards to monitor
# Volatility Profile: 1 = Stable, 3 = Highly Volatile
WATCHLIST = [
    {"id": "BASE-001", "name": "Charizard VMAX (Shiny)", "base_price": 800, "volatility_profile": 2},
    {"id": "BASE-002", "name": "Pikachu Illustrator (Fractional)", "base_price": 5000, "volatility_profile": 1},
    {"id": "BASE-003", "name": "Mewtwo GX Rainbow", "base_price": 120, "volatility_profile": 3},
    {"id": "BASE-004", "name": "Umbreon VMAX Alt Art", "base_price": 600, "volatility_profile": 2},
]

# ==========================================
# 2. DATA INGESTION LAYER (Mocking Real APIs)
# ==========================================

class MarketDataFetcher:
    """
    Simulates fetching complex time-series data from On-Chain and Off-Chain sources.
    In production, this would connect to Beezie SDK and eBay API.
    """
    
    def get_historical_data(self, card: Dict, days: int = 7) -> pd.DataFrame:
        """
        Generates a 7-day price history to allow for trend analysis.
        """
        data_points = []
        current_price = card['base_price']
        volatility_multiplier = card['volatility_profile'] * 0.02 # 2% to 6% daily swing

        for i in range(days):
            date = datetime.now() - timedelta(days=(days - 1 - i))
            
            # Simulate On-Chain Logic (Often more stable/lagging)
            noise_on = random.uniform(-volatility_multiplier, volatility_multiplier)
            price_on = current_price * (1 + noise_on)
            vol_on = random.randint(5, 50) # Daily transactions

            # Simulate Off-Chain Logic (Higher volatility, reacts faster to hype)
            # We introduce a 'drift' to create divergence
            drift = random.uniform(-0.15, 0.15) # Up to 15% drift from fair value
            price_off = price_on * (1 + drift)
            vol_off = random.randint(50, 200)

            data_points.append({
                "date": date.strftime("%Y-%m-%d"),
                "on_chain_price": round(price_on, 2),
                "off_chain_price": round(price_off, 2),
                "on_chain_vol": vol_on,
                "off_chain_vol": vol_off
            })
            
            # Update base price for next day (random walk)
            current_price = price_on 

        return pd.DataFrame(data_points)

# ==========================================
# 3. ANALYTICAL ENGINE (The Brain)
# ==========================================

class MarketAnalyzer:
    """
    Processes raw data to extract actionable insights: Divergence, Volatility, Liquidity.
    """
    
    def analyze_asset(self, card_name: str, df: pd.DataFrame) -> Dict:
        # Get latest data point
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 1. Price Divergence Calculation
        # Formula: (Off - On) / On
        divergence = (latest['off_chain_price'] - latest['on_chain_price']) / latest['on_chain_price']
        divergence_pct = round(divergence * 100, 2)
        
        # 2. Volatility Analysis (Standard Deviation of last 7 days)
        # We compare standard deviation relative to the mean price
        std_dev = df['off_chain_price'].std()
        mean_price = df['off_chain_price'].mean()
        volatility_score = round((std_dev / mean_price) * 100, 2)
        
        # 3. Liquidity Trend (On-Chain)
        # Compare current volume to 7-day average
        avg_vol = df['on_chain_vol'].mean()
        vol_change_pct = round(((latest['on_chain_vol'] - avg_vol) / avg_vol) * 100, 2)

        return {
            "card_name": card_name,
            "current_on_price": latest['on_chain_price'],
            "current_off_price": latest['off_chain_price'],
            "divergence_pct": divergence_pct,
            "volatility_score": volatility_score,
            "liquidity_trend_pct": vol_change_pct,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

# ==========================================
# 4. PERSONA ENGINE (Wise Slowking)
# ==========================================

class WiseSlowkingPersona:
    """
    Translates raw metrics into the philosophical, movie-inspired Slowking persona.
    """
    
    def craft_message(self, analysis: Dict) -> str:
        div_pct = analysis['divergence_pct']
        vol_score = analysis['volatility_score']
        liq_trend = analysis['liquidity_trend_pct']
        name = analysis['card_name']
        
        # --- SCENARIO 1: CRITICAL ARBITRAGE (High Divergence) ---
        if abs(div_pct) >= CONFIG["thresholds"]["divergence_critical"]:
            direction = "exceeds" if div_pct > 0 else "lags behind"
            advice = "Tokenize immediately." if div_pct > 0 else "Acquire the digital asset."
            
            return (
                f"🚨 **THE BALANCE IS BROKEN** 🚨\n\n"
                f"I sense a disturbance in **{name}**.\n"
                f"The physical world {direction} the digital realm by **{abs(div_pct)}%**.\n\n"
                f"**On-Chain:** ${analysis['current_on_price']:,.2f}\n"
                f"**Off-Chain:** ${analysis['current_off_price']:,.2f}\n\n"
                f"🔮 **Slowking's Decree:** The gap is unsustainable. {advice} \n"
                f"#RWA #BaseChain #Arbitrage"
            )

        # --- SCENARIO 2: HIGH VOLATILITY (Danger) ---
        elif vol_score >= CONFIG["thresholds"]["volatility_high"]:
            return (
                f"🌊 **THE WATERS ARE TURBULENT**\n\n"
                f"**{name}** suffers from a volatility score of **{vol_score}**.\n"
                f"Prices are shifting violently like a storm at sea.\n\n"
                f"🐚 **Slowking's Counsel:** Do not mistake chaos for opportunity. \n"
                f"Let the waves settle before casting your net.\n"
                f"#WiseSlowking #MarketAlert #CryptoVol"
            )

        # --- SCENARIO 3: LIQUIDITY DRY UP (Accumulation?) ---
        elif liq_trend <= CONFIG["thresholds"]["liquidity_drop"]:
            return (
                f"👁️ **THE SILENCE BEFORE THE STORM**\n\n"
                f"On-chain volume for **{name}** has dropped by **{abs(liq_trend)}%**.\n"
                f"The crowd has left, yet value remains.\n\n"
                f"🐚 **Slowking's Observation:** When the noise fades, the wise begin to accumulate.\n"
                f"#RWA #Undervalued #Base"
            )

        # --- SCENARIO 4: STABILITY (The Norm) ---
        else:
            return (
                f"⚖️ **HARMONY RESTORED**\n\n"
                f"**{name}** rests in equilibrium.\n"
                f"The difference between realms is a mere **{div_pct}%**.\n"
                f"True power lies in patience. We watch. We wait.\n"
                f"#WiseSlowking #PokemonTCG"
            )

# ==========================================
# 5. MAIN AGENT ORCHESTRATOR
# ==========================================

class AgentCore:
    def __init__(self):
        self.fetcher = MarketDataFetcher()
        self.analyzer = MarketAnalyzer()
        self.persona = WiseSlowkingPersona()

    def run_cycle(self):
        print(f"\n⚡ {CONFIG['agent_name']} (v{CONFIG['version']}) Initializing on {CONFIG['ecosystem']}...")
        print("📥 Ingesting Cross-Market Data Streams...\n")
        
        results = []

        for card in WATCHLIST:
            # 1. Fetch Data (7-Day History)
            df_history = self.fetcher.get_historical_data(card)
            
            # 2. Analyze Data
            analysis = self.analyzer.analyze_asset(card['name'], df_history)
            
            # 3. Generate Content
            post_content = self.persona.craft_message(analysis)
            
            # 4. Output (Simulating X API Post)
            print("-" * 60)
            print(f"🧩 ANALYZING: {card['name'].upper()}")
            print(f"📊 Tech Specs: Div: {analysis['divergence_pct']}% | Vol: {analysis['volatility_score']} | Liq: {analysis['liquidity_trend_pct']}%")
            print("-" * 60)
            print("📢 GENERATED X POST:")
            print(post_content)
            print("\n")
            
            results.append(analysis)

        return results

# ==========================================
# 6. EXECUTION
# ==========================================

if __name__ == "__main__":
    agent = AgentCore()
    agent.run_cycle()
