from flask import Flask, render_template, request
import requests
from collections import defaultdict
import time

app = Flask(__name__)

# Твой словарь ролей героев (вставь весь свой)
HERO_ROLES = {
    "Abaddon": [1, 3, 4, 5],
    "Alchemist": [1],
    "Ancient Apparition": [4, 5],
    "Anti-Mage": [1],
    "Arc Warden": [2],
    "Axe": [3],
    "Bane": [4, 5],
    "Batrider": [2, 3, 4],
    "Beastmaster": [2, 3],
    "Bloodseeker": [1],
    "Bounty Hunter": [4, 5],
    "Brewmaster": [3],
    "Bristleback": [3],
    "Broodmother": [1, 2],
    "Centaur Warrunner": [3],
    "Chaos Knight": [1, 3],
    "Chen": [5],
    "Clinkz": [1],
    "Clockwerk": [4],
    "Crystal Maiden": [4, 5],
    "Dark Seer": [3],
    "Dark Willow": [4, 5],
    "Dawnbreaker": [3],
    "Dazzle": [4, 5],
    "Death Prophet": [3],
    "Disruptor": [4, 5],
    "Doom": [3],
    "Dragon Knight": [1, 2, 3],
    "Drow Ranger": [1],
    "Earth Spirit": [2, 4],
    "Earthshaker": [2, 3, 4],
    "Elder Titan": [4, 5],
    "Ember Spirit": [2],
    "Enchantress": [4, 5],
    "Enigma": [4, 5],
    "Faceless Void": [1],
    "Grimstroke": [4, 5],
    "Gyrocopter": [1],
    "Hoodwink": [4, 5],
    "Huskar": [2, 3],
    "Invoker": [2, 4, 5],
    "Io": [5],
    "Jakiro": [4, 5],
    "Juggernaut": [1],
    "Keeper of the Light": [2, 4, 5],
    "Kez": [1, 2],
    "Kunkka": [2, 3],
    "Legion Commander": [3],
    "Leshrac": [2],
    "Lich": [4, 5],
    "Lifestealer": [1],
    "Lina": [1, 2, 4, 5],
    "Lion": [4, 5],
    "Lone Druid": [2, 3],
    "Luna": [1],
    "Lycan": [3],
    "Magnus": [3, 4],
    "Marci": [2, 4, 5],
    "Mars": [3],
    "Medusa": [1],
    "Meepo": [2],
    "Mirana": [4, 5],
    "Monkey King": [1, 2],
    "Morphling": [1],
    "Muerta": [1],
    "Naga Siren": [1],
    "Nature's Prophet": [1, 2, 4, 5],
    "Necrophos": [2, 3],
    "Night Stalker": [3],
    "Nyx Assassin": [4, 5],
    "Ogre Magi": [4, 5],
    "Omniknight": [3, 5],
    "Oracle": [4, 5],
    "Outworld Destroyer": [2],
    "Pangolier": [2, 3],
    "Phantom Assassin": [1],
    "Phantom Lancer": [1],
    "Phoenix": [3, 4, 5],
    "Primal Beast": [3],
    "Puck": [2],
    "Pudge": [3, 4, 5],
    "Pugna": [4, 5],
    "Queen of Pain": [2],
    "Razor": [1, 3],
    "Riki": [2, 1],
    "Ringmaster": [4, 5],
    "Rubick": [2, 4],
    "Sand King": [3],
    "Shadow Demon": [4, 5],
    "Shadow Fiend": [1, 2],
    "Shadow Shaman": [4, 5],
    "Silencer": [4, 5],
    "Skywrath Mage": [2, 4, 5],
    "Slardar": [3],
    "Slark": [1],
    "Snapfire": [4, 5],
    "Sniper": [2, 4],
    "Spectre": [1],
    "Spirit Breaker": [3, 4],
    "Storm Spirit": [2],
    "Sven": [1],
    "Techies": [4, 5],
    "Templar Assassin": [1, 2],
    "Terrorblade": [1],
    "Tidehunter": [3],
    "Timbersaw": [3],
    "Tinker": [2],
    "Tiny": [2, 4, 3],
    "Treant Protector": [5],
    "Troll Warlord": [1],
    "Tusk": [4, 5],
    "Underlord": [3],
    "Undying": [4, 5],
    "Ursa": [1],
    "Vengeful Spirit": [4, 5],
    "Venomancer": [4, 5],
    "Viper": [2, 3],
    "Visage": [3],
    "Void Spirit": [2],
    "Warlock": [4, 5],
    "Weaver": [1, 4],
    "Windranger": [1, 4],
    "Winter Wyvern": [4, 5],
    "Wraith King": [1, 3],
    "Zeus": [2, 4, 5],
    "Largo": [3],
}

name_to_id = {}
id_to_name = {}


def load_heroes():
    """Загружаем героев один раз"""
    global name_to_id, id_to_name
    url = "https://api.opendota.com/api/heroes"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        heroes = resp.json()
        name_to_id = {h['localized_name']: h['id'] for h in heroes}
        id_to_name = {h['id']: h['localized_name'] for h in heroes}
        print(f"Загружено {len(heroes)} героев")
    except Exception as e:
        print(f"Ошибка загрузки героев: {e}")


def get_matchups(hero_id):
    """Получаем matchup"""
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        matchups = {}
        for m in data:
            opp_id = m['hero_id']
            games = m['games_played']
            if games > 1:
                winrate = (m['wins'] / games) * 100
                matchups[opp_id] = {'winrate': winrate, 'games': games}
        time.sleep(1.2)
        return matchups
    except:
        return {}


def recommend_heroes(role, enemies, top_k=7, mode='average'):
    if not (1 <= role <= 5):
        return ["Неверная роль"] * top_k

    if not enemies:
        return ["Укажи врагов"] * top_k

    matchups_by_hero = defaultdict(list)
    good_enemies = 0

    for enemy in enemies[:5]:
        enemy_id = name_to_id.get(enemy)
        if not enemy_id:
            continue

        data = get_matchups(enemy_id)
        if data:
            good_enemies += 1
            for candidate_id, stats in data.items():
                matchups_by_hero[candidate_id].append(stats['winrate'])

    if good_enemies == 0:
        return ["Нет статистики по этим врагам"] * top_k

    scores = {}
    for hid, rates in matchups_by_hero.items():
        if not rates:
            continue
        if mode == 'min':
            avg_rate = min(rates)
        else:
            avg_rate = sum(rates) / len(rates)
        advantage = 50 - avg_rate
        scores[hid] = advantage

    banned = {name_to_id.get(e) for e in enemies if e in name_to_id}

    candidates = []
    for hid, adv in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        if hid in banned:
            continue
        name = id_to_name.get(hid)
        if name and name in HERO_ROLES and role in HERO_ROLES[name]:
            candidates.append((name, adv))

    result = []
    for name, adv in candidates[:top_k]:
        sign = '+' if adv >= 0 else ''
        result.append(f"{name} ({sign}{adv:.2f}%)")

    while len(result) < top_k:
        result.append("(герой не найден)")

    return result


# Загружаем героев при старте приложения
load_heroes()


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = None
    error = None

    if request.method == "POST":
        try:
            role = int(request.form["role"])
            enemies_raw = request.form["enemies"]
            enemies = [e.strip() for e in enemies_raw.split(",") if e.strip()]

            if not enemies:
                error = "Укажи хотя бы одного врага"
            else:
                recommendations = recommend_heroes(role, enemies)
        except ValueError:
            error = "Роль должна быть числом от 1 до 5"

    return render_template("index.html", recommendations=recommendations, error=error)


if __name__ == "__main__":
    app.run(debug=True)