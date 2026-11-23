
import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=BR"
OUTPUT = "data/trends.json"

def buscar_tendencias():
    req = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "Mozilla/5.0 RadarOportunidades/1.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    resultados = []

    for item in root.findall(".//item"):
        titulo = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        publicado = item.findtext("pubDate", "").strip()

        if not titulo:
            continue

        traffic = ""
        for child in item:
            if child.tag.endswith("approx_traffic"):
                traffic = (child.text or "").strip()

        resultados.append({
            "title": titulo,
            "link": link,
            "traffic": traffic,
            "published": publicado
        })

    return resultados

def main():
    try:
        tendencias = buscar_tendencias()

        os.makedirs("data", exist_ok=True)

        dados = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source": "Google Trends Brasil RSS",
            "count": len(tendencias),
            "trends": tendencias
        }

        with open(OUTPUT, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

        print(f"Radar atualizado: {len(tendencias)} tendências.")

    except Exception as erro:
        print(f"Erro ao buscar tendências: {erro}")
        raise

if __name__ == "__main__":
    main()
