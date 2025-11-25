import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION & PLATFORMS
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "2.0-Grand-Oracle",
    "platforms": {
        "on_chain": ["Beezie", "Collector Crypt"],
        "off_chain": ["eBay", "TCGPlayer", "Cardmarket"]
    },
    "thresholds": {
        "divergence_critical": 15.0,  # % difference
        "supply_squeeze": -10.0,      # % drop in listings (Accumulation)
        "liquidity_drop": -25.0       # % drop in volume
    }
}

# Assets to monitor
WATCHLIST = [
    {"id": "PKM-001", "name": "Charizard VMAX (Shiny)", "base_price": 800},
    {"id": "PKM-002", "name": "Pikachu Illustrator (Fractional)", "base_price": 5000},
    {"id": "PKM-003", "name": "Umbreon VMAX Alt Art", "base_price": 600},
    {"id": "PKM-004", "name": "Mewtwo GX Rainbow", "base_price": 120},
]

# ==========================================
# 2. GRANULAR DATA INGESTION (Mocking Specific Platforms)
# ==========================================

class GranularDataFetcher:
    """
    Simulates fetching data from SPECIFIC platforms (Beezie vs eBay vs TCGPlayer).
    """
    
    def get_market_snapshot(self, card: Dict, scenario_type: str = "random") -> Dict:
        """
        Generates data based on a specific scenario to demonstrate all Agent capabilities.
        """
        base = card['base_price']
        
        # Default: Everything is roughly equal
        prices = {
            "Beezie": base,
            "Collector Crypt": base,
            "eBay": base,
            "TCGPlayer": base,
            "Cardmarket": base
        }
        supply = {"on_chain": 100, "off_chain": 500}
        volume_trend = 0.0 # Stable

        # --- SCENARIO INJECTION FOR DEMO ---
        if scenario_type == "divergence_on_chain_cheap":
            # Beezie is way cheaper than eBay
            prices["Beezie"] = base * 0.80  # -20%
            prices["eBay"] = base * 1.10    # +10%
            
        elif scenario_type == "divergence_off_chain_cheap":
            # TCGPlayer is way cheaper than Collector Crypt
            prices["TCGPlayer"] = base * 0.75
            prices["Collector Crypt"] = base * 1.05

        elif scenario_type == "accumulation":
            # Prices stable, but supply is vanishing on Beezie
            supply["on_chain"] = 20 # Huge drop from 100
            
        elif scenario_type == "liquidity_crisis":
            # Volume is dead
            volume_trend = -40.0

        return {
            "card_name": card['name'],
            "prices": prices,
            "supply": supply,
            "volume_trend": volume_trend,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

# ==========================================
# 3. ANALYTICAL ENGINE (Logic & Comparison)
# ==========================================

class DeepMarketAnalyzer:
    """
    Identifies the EXACT platform causing the discrepancy.
    """
    
    def analyze(self, data: Dict) -> Dict:
        prices = data['prices']
        
        # 1. Identify Lowest and Highest Sources
        min_source = min(prices, key=prices.get)
        max_source = max(prices, key=prices.get)
        min_price = prices[min_source]
        max_price = prices[max_source]
        
        # 2. Calculate Divergence
        # (High - Low) / Low
        divergence_pct = ((max_price - min_price) / min_price) * 100
        
        # 3. Classify the Opportunity
        insight_type = "Stability"
        
        if divergence_pct >= CONFIG["thresholds"]["divergence_critical"]:
            insight_type = "Arb_Opportunity"
        elif data['supply']['on_chain'] < 40: # Arbitrary threshold for demo
            insight_type = "Silent_Accumulation"
        elif data['volume_trend'] <= CONFIG["thresholds"]["liquidity_drop"]:
            insight_type = "Liquidity_Crisis"
            
        return {
            "card_name": data['card_name'],
            "insight_type": insight_type,
            "cheapest_platform": min_source,
            "expensive_platform": max_source,
            "price_low": min_price,
            "price_high": max_price,
            "divergence": divergence_pct,
            "volume_trend": data['volume_trend']
        }

# ==========================================
# 4. PERSONA ENGINE (The Wise Slowking - NO HASHTAGS)
# ==========================================

class WiseSlowkingPersona:
    """
    Generates plain text, philosophical, platform-specific insights.
    """
    
    def speak(self, analysis: Dict) -> str:
        card = analysis['card_name']
        low_plat = analysis['cheapest_platform']
        high_plat = analysis['expensive_platform']
        low_price = f"${analysis['price_low']:,.2f}"
        high_price = f"${analysis['price_high']:,.2f}"
        
        # --- SCENARIO 1: ARBITRAGE (Price Gap) ---
        if analysis['insight_type'] == "Arb_Opportunity":
            return (
                f"🚨 THE BALANCE IS BROKEN for {card}\n\n"
                f"I have consulted the scrolls. A significant disparity exists.\n"
                f"The marketplace of **{low_plat}** undervalues this asset at {low_price}.\n"
                f"Meanwhile, **{high_plat}** trades at a premium of {high_price}.\n\n"
                f"The wise collector sees what others miss. The opportunity lies within {low_plat}."
            )

        # --- SCENARIO 2: ACCUMULATION (Supply Squeeze) ---
        elif analysis['insight_type'] == "Silent_Accumulation":
            return (
                f"👁️ SILENT ACCUMULATION DETECTED for {card}\n\n"
                f"Do not be fooled by the price stability. The quantity of listings on **Beezie** and **Collector Crypt** is vanishing.\n"
                f"The supply thins while the demand remains unspoken.\n\n"
                f"History teaches us that scarcity precedes value. Verify the on-chain data immediately."
            )

        # --- SCENARIO 3: LIQUIDITY CRISIS (Volume Drop) ---
        elif analysis['insight_type'] == "Liquidity_Crisis":
            return (
                f"❄️ THE MARKET FREEZES for {card}\n\n"
                f"Volume has evaporated by {abs(analysis['volume_trend'])}%.\n"
                f"Liquidity on **eBay** and **Beezie** alike has stalled.\n\n"
                f"This silence is dangerous. One must not mistake lack of movement for stability. Exercise extreme caution."
            )

        # --- SCENARIO 4: STABILITY ---
        else:
            return (
                f"⚖️ HARMONY RESTORED for {card}\n\n"
                f"I have scanned **Beezie**, **Collector Crypt**, and **eBay**.\n"
                f"Prices are aligned across the physical and digital realms.\n"
                f"True wisdom lies in patience. We watch. We wait."
            )

# ==========================================
# 5. MAIN EXECUTION LOOP
# ==========================================

if __name__ == "__main__":
    fetcher = GranularDataFetcher()
    analyzer = DeepMarketAnalyzer()
    persona = WiseSlowkingPersona()
    
    print("="*60)
    print("🐚 WISE SLOWKING: INITIALIZING GRANULAR MARKET SCAN")
    print("   Scanning: Beezie, Collector Crypt, eBay, TCGPlayer, Cardmarket")
    print("="*60 + "\n")

    # We manually force different scenarios to demonstrate the full range of the Agent
    test_scenarios = [
        ("PKM-001", "divergence_on_chain_cheap"), # Beezie is cheap
        ("PKM-002", "divergence_off_chain_cheap"), # TCGPlayer is cheap
        ("PKM-003", "accumulation"),               # Supply squeeze
        ("PKM-004", "liquidity_crisis")            # No volume
    ]

    for card_id, scenario in test_scenarios:
        # 1. Find the card object
        card_obj = next(item for item in WATCHLIST if item["id"] == card_id)
        
        # 2. Fetch Data (Mocking the specific scenario)
        raw_data = fetcher.get_market_snapshot(card_obj, scenario_type=scenario)
        
        # 3. Analyze
        analysis = analyzer.analyze(raw_data)
        
        # 4. Speak
        post = persona.speak(analysis)
        
        print(f"--- ANALYZING: {card_obj['name']} ---")
        print(f"🔍 Scenario Detected: {scenario.upper()}")
        print("📢 GENERATED POST (No Hashtags):")
        print(post)
        print("\n" + "-"*60 + "\n")
