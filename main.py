import requests
import json

# Yapılandırma
API_KEY = 'YOUR_TBA_API_KEY'  # Buraya kendi API anahtarını yapıştır
BASE_URL = 'https://www.thebluealliance.com/api/v3'
HEADERS = {'X-TBA-Auth-Key': API_KEY}

def get_all_teams():
    all_teams = []
    page_num = 0
    
    while True:
        # TBA her sayfada 500 takım döndürür
        url = f"{BASE_URL}/teams/{page_num}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Hata: {response.status_code}")
            break
            
        teams = response.json()
        if not teams: # Liste boşsa tüm takımlar çekilmiştir
            break
            
        all_teams.extend(teams)
        print(f"Sayfa {page_num} çekildi...")
        page_num += 1
        
    return all_teams

def classify_by_country(teams):
    countries = {}
    
    for team in teams:
        country = team.get('country')
        if not country:
            country = "Unknown"
            
        if country not in countries:
            countries[country] = []
            
        countries[country].append({
            'team_number': team['team_number'],
            'nickname': team['nickname'],
            'city': team['city']
        })
    
    return countries

# Ana Çalıştırma Bloğu
if __name__ == "__main__":
    print("Veriler çekiliyor, bu işlem biraz sürebilir...")
    teams_data = get_all_teams()
    classified = classify_by_country(teams_data)
    
    # Sonuçları bir JSON dosyasına kaydetme
    with open('frc_teams_by_country.json', 'w', encoding='utf-8') as f:
        json.dump(classified, f, ensure_ascii=False, indent=4)
        
    print(f"\nİşlem tamamlandı! Toplam {len(teams_data)} takım {len(classified)} ülkeye ayrıldı.")
    print("Sonuçlar 'frc_teams_by_country.json' dosyasına kaydedildi.")