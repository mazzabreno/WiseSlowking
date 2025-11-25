import json
import os
from typing import Dict, List

# ==========================================
# 1. CONFIGURATION (REAL DATA MODE)
# ==========================================

CONFIG = {
    "agent_name": "Wise Slowking",
    "version": "3.0-Real-Market-Data",
    "data_source": "real_data.json", # Lê o arquivo json criado
    "thresholds": {
        "divergence": 10.0,    # 10% de diferença ativa o alerta
        "scarcity": 10         # Menos de 10 unidades on-chain = Escassez
    }
}

# ==========================================
# 2. REAL DATA INGESTION
# ==========================================

class RealDataFetcher:
    """Lê o snapshot de mercado real para garantir veracidade na demo."""
    
    def load_data(self) -> List[Dict]:
        # Verifica se o arquivo de dados existe
        if not os.path.exists(CONFIG["data_source"]):
            print(f"❌ ERRO CRÍTICO: O arquivo '{CONFIG['data_source']}' não foi encontrado.")
            print("   Por favor, crie o arquivo real_data.json antes de rodar o agente.")
            return []
            
        try:
            with open(CONFIG["data_source"], 'r') as f:
                data = json.load(f)
                print(f"✅ DADOS CARREGADOS COM SUCESSO")
                print(f"   Snapshot de Mercado: {data.get('snapshot_date', 'Data Desconhecida')}")
                return data['cards']
        except Exception as e:
            print(f"❌ Erro ao ler o arquivo JSON: {
