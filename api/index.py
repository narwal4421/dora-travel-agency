from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

CULTURE_DB = {
    # North America
    "United States": {"food": "Burgers, BBQ Ribs, clam chowder, and regional specialties", "culture": "Tipping (15-20%) is mandatory. Portions are large.", "safety": "Varies by neighborhood; use standard urban awareness.", "mult": 1.8, "language": "English", "currency": "US Dollar ($)"},
    "Canada": {"food": "Poutine, Maple Syrup treats, Salmon", "culture": "Canadians are famous for politeness. Tipping (15-20%) is standard.", "safety": "Generally very safe. Watch for extreme winter weather.", "mult": 1.5, "language": "English, French (Quebec)", "currency": "Canadian Dollar (CAD)"},
    "Mexico": {"food": "Street Tacos, Mole, Chilaquiles, Ceviche", "culture": "Warm and festive. Learning a bit of Spanish goes a long way.", "safety": "Stick to tourist zones and use registered taxis.", "mult": 0.7, "language": "Spanish • Hello: Hola • Thanks: Gracias", "currency": "Mexican Peso ($)"},
    
    # Europe
    "Italy": {"food": "Pasta Carbonara, Neapolitan Pizza, Gelato", "culture": "Greet with 'Buongiorno'. Dinner is usually late (8PM+). Dress smartly.", "safety": "Beware of pickpockets in crowded tourist spots.", "mult": 1.5, "language": "Italian • Hello: Buongiorno • Thanks: Grazie", "currency": "Euro (€)"},
    "France": {"food": "Croissants, Escargot, Boeuf Bourguignon", "culture": "Always say 'Bonjour' when entering a shop.", "safety": "Watch for petty theft around major landmarks.", "mult": 1.6, "language": "French • Hello: Bonjour • Thanks: Merci", "currency": "Euro (€)"},
    "United Kingdom": {"food": "Fish and Chips, Sunday Roast, Full English", "culture": "Queuing is practically a religion. Stand on the right on escalators.", "safety": "Safe, but look both ways before crossing (cars drive on left).", "mult": 1.7, "language": "English", "currency": "British Pound (£)"},
    "Spain": {"food": "Tapas, Paella, Churros con Chocolate", "culture": "Siesta is real; shops may close mid-day. Dinner happens after 9 PM.", "safety": "Beware of pickpockets in major cities.", "mult": 1.3, "language": "Spanish • Hello: Hola • Thanks: Gracias", "currency": "Euro (€)"},
    "Germany": {"food": "Bratwurst, Pretzels, Schnitzel", "culture": "Punctuality is essential. Toast with 'Prost' and make eye contact.", "safety": "Highly safe infrastructure. Observe pedestrian lights.", "mult": 1.4, "language": "German • Hello: Hallo • Thanks: Danke", "currency": "Euro (€)"},
    "Greece": {"food": "Moussaka, Souvlaki, fresh Greek Salad", "culture": "Pace of life is relaxed. Hospitality is very important.", "safety": "Very safe. Be cautious on roads if renting a scooter.", "mult": 1.1, "language": "Greek • Hello: Yassou • Thanks: Efharisto", "currency": "Euro (€)"},
    "Portugal": {"food": "Bacalhau, Pastel de Nata, Francesinha", "culture": "Laid back and friendly. Dinner is generally after 8 PM.", "safety": "Extremely safe country, standard precautions apply.", "mult": 0.9, "language": "Portuguese • Hello: Olá • Thanks: Obrigado", "currency": "Euro (€)"},
    "Switzerland": {"food": "Fondue, Raclette, Swiss Chocolate", "culture": "Very punctual. Sundays are strict rest days (shops closed).", "safety": "One of the safest countries in the world.", "mult": 2.2, "language": "German/French/Italian • Hello: Grüezi", "currency": "Swiss Franc (CHF)"},
    "Netherlands": {"food": "Stroopwafel, Bitterballen, Herring", "culture": "Very direct communication. Cycling is the primary transport.", "safety": "Very safe. Watch out for cyclists in bike lanes!", "mult": 1.4, "language": "Dutch • Hello: Hallo • Thanks: Dank je", "currency": "Euro (€)"},
    "Ireland": {"food": "Irish Stew, Boxty, Guinness bread", "culture": "Pub culture is central. 'Craic' means fun/conversation.", "safety": "Very safe. Weather changes rapidly, so layer up.", "mult": 1.4, "language": "English, Irish", "currency": "Euro (€)"},
    
    # Asia
    "Japan": {"food": "Fresh Sushi, Ramen bowls, Takoyaki", "culture": "Bowing is the standard greeting. Tipping is considered rude.", "safety": "Extremely safe, but observe etiquette on public transit.", "mult": 1.8, "language": "Japanese • Hello: Konnichiwa • Thanks: Arigatou", "currency": "Japanese Yen (¥)"},
    "Thailand": {"food": "Pad Thai, Green Curry, Mango Sticky Rice", "culture": "Do not touch people's heads. Respect the royal family.", "safety": "Watch out for tuk-tuk scams and drink bottled water.", "mult": 0.6, "language": "Thai • Hello: Sawasdee • Thanks: Khop Khun", "currency": "Thai Baht (฿)"},
    "India": {"food": "Butter Chicken, Masala Dosa, Biryani", "culture": "Use your right hand for eating and giving/receiving.", "safety": "Drink only bottled water. Negotiate fare for rickshaws.", "mult": 0.5, "language": "Hindi / English • Hello: Namaste • Thanks: Dhanyavad", "currency": "Indian Rupee (₹)"},
    "China": {"food": "Peking Duck, Dim Sum, Hot Pot", "culture": "Respect for elders is paramount. Bring cash or use WeChat Pay.", "safety": "Low street crime. Internet requires a VPN.", "mult": 1.0, "language": "Mandarin • Hello: Nǐ hǎo • Thanks: Xièxiè", "currency": "Chinese Yuan (CNY)"},
    "South Korea": {"food": "Kimchi, Korean BBQ, Bibimbap", "culture": "Use two hands when giving/receiving items. Bow to greet.", "safety": "Extremely safe with fantastic public transit.", "mult": 1.3, "language": "Korean • Hello: Annyeonghaseyo • Thanks: Gamsahamnida", "currency": "South Korean Won (KRW)"},
    "Vietnam": {"food": "Pho, Banh Mi, Fresh Spring Rolls", "culture": "Modest dress for temples. Haggling is common in markets.", "safety": "Traffic is chaotic; walk confidently across streets.", "mult": 0.4, "language": "Vietnamese • Hello: Xin chào", "currency": "Vietnamese Dong (VND)"},
    "Indonesia": {"food": "Nasi Goreng, Satay, Beef Rendang", "culture": "Predominantly Muslim (except Bali). Dress modestly.", "safety": "Beware of chaotic traffic. Drink bottled water.", "mult": 0.5, "language": "Indonesian • Hello: Halo • Thanks: Terima kasih", "currency": "Indonesian Rupiah (IDR)"},
    
    # Middle East & Africa
    "Turkey": {"food": "Iskender Kebab, Baklava, Turkish Delight", "culture": "Bargaining is common in bazaars. Accept tea if offered.", "safety": "Generally safe. Use marked taxis.", "mult": 0.8, "language": "Turkish • Hello: Merhaba • Thanks: Teşekkürler", "currency": "Turkish Lira (₺)"},
    "United Arab Emirates": {"food": "Shawarma, Machboos, Falafel", "culture": "Dress modestly in public. Public displays of affection are illegal.", "safety": "Extremely safe with strict laws.", "mult": 1.6, "language": "Arabic • Hello: Marhaba • Thanks: Shukran", "currency": "UAE Dirham (AED)"},
    "Egypt": {"food": "Koshari, Ful Medames, Shawarma", "culture": "Dress conservatively. Bargaining is expected.", "safety": "Stay hydrated. Cross bustling streets confidently.", "mult": 0.6, "language": "Arabic • Hello: Marhaba • Thanks: Shukran", "currency": "Egyptian Pound (E£)"},
    "Morocco": {"food": "Tagine, Couscous, Mint Tea", "culture": "Use right hand for eating. Tipping a few dirhams is standard.", "safety": "Beware of persistent vendors or fake guides.", "mult": 0.6, "language": "Arabic/French • Hello: Salam", "currency": "Moroccan Dirham (MAD)"},
    "South Africa": {"food": "Braai (BBQ), Biltong, Bobotie", "culture": "Casual and friendly. Tipping 10-15% is standard.", "safety": "Stay aware of your surroundings, avoid walking at night.", "mult": 0.8, "language": "English, Zulu, Xhosa...", "currency": "South African Rand (ZAR)"},
    
    # South America & Oceania
    "Brazil": {"food": "Feijoada, Pão de Queijo, Churrasco", "culture": "Very warm and affectionate people. Thumbs up is common.", "safety": "Keep phones out of sight in crowded urban areas.", "mult": 0.9, "language": "Portuguese • Hello: Olá • Thanks: Obrigado/a", "currency": "Brazilian Real (R$)"},
    "Argentina": {"food": "Asado, Empanadas, Alfajores", "culture": "Dinner is very late (10 PM). Mate (tea) sharing is common.", "safety": "Watch for pickpockets in Buenos Aires.", "mult": 0.7, "language": "Spanish • Hello: Hola", "currency": "Argentine Peso ($)"},
    "Peru": {"food": "Ceviche, Lomo Saltado, Cuy", "culture": "Very proud of their Incan heritage. Altitude acclimation needed.", "safety": "Use registered taxis. Drink bottled water.", "mult": 0.6, "language": "Spanish • Hello: Hola", "currency": "Peruvian Sol (PEN)"},
    "Australia": {"food": "Meat Pies, Vegemite on Toast, Tim Tams", "culture": "Very laid-back ('No worries'). Strong coffee culture.", "safety": "Sun is extremely harsh (wear SPF). Swim between the flags.", "mult": 1.6, "language": "English", "currency": "Australian Dollar (AUD)"},
    "New Zealand": {"food": "Hangi, Fish and Chips, Pavlova", "culture": "Very eco-conscious. Māori culture is highly respected.", "safety": "Extremely safe. Weather can change rapidly.", "mult": 1.5, "language": "English, Māori", "currency": "New Zealand Dollar (NZD)"}
}

FAMOUS_LANDMARKS = {
    # North American Cities
    "new york": ["Statue of Liberty", "Central Park", "Times Square", "Empire State Building"],
    "new york city": ["Statue of Liberty", "Central Park", "Times Square", "Empire State Building"],
    "los angeles": ["Hollywood Sign", "Griffith Observatory", "Santa Monica Pier", "Universal Studios"],
    "las vegas": ["The Las Vegas Strip", "Bellagio Fountains", "Fremont Street", "The Venetian"],
    "san francisco": ["Golden Gate Bridge", "Alcatraz Island", "Fisherman's Wharf", "Lombard Street"],
    "chicago": ["Cloud Gate (The Bean)", "Willis Tower", "Navy Pier", "Millennium Park"],
    "washington dc": ["The White House", "Lincoln Memorial", "Washington Monument", "US Capitol"],
    "miami": ["South Beach", "Art Deco Historic District", "Little Havana", "Vizcaya Museum"],
    "toronto": ["CN Tower", "Royal Ontario Museum", "Ripley's Aquarium", "Casa Loma"],
    "vancouver": ["Stanley Park", "Capilano Suspension Bridge", "Granville Island"],
    "mexico city": ["Zócalo", "Chapultepec Castle", "Frida Kahlo Museum", "Palacio de Bellas Artes"],
    
    # European Cities
    "paris": ["The Eiffel Tower", "The Louvre", "Arc de Triomphe", "Notre-Dame Cathedral"],
    "rome": ["The Colosseum", "Trevi Fountain", "The Pantheon", "Roman Forum"],
    "london": ["Big Ben", "Tower of London", "The London Eye", "Buckingham Palace", "Westminster Abbey"],
    "istanbul": ["Hagia Sophia", "Blue Mosque", "Grand Bazaar", "Topkapi Palace", "Basilica Cistern"],
    "barcelona": ["La Sagrada Familia", "Park Güell", "Casa Batlló", "Gothic Quarter"],
    "madrid": ["Royal Palace of Madrid", "Prado Museum", "Plaza Mayor", "Retiro Park"],
    "amsterdam": ["Anne Frank House", "Van Gogh Museum", "Rijksmuseum", "Vondelpark"],
    "berlin": ["Brandenburg Gate", "Berlin Wall Memorial", "Reichstag Building"],
    "venice": ["Grand Canal", "St. Mark's Basilica", "Doge's Palace", "Rialto Bridge"],
    "florence": ["Duomo di Firenze", "Uffizi Gallery", "Ponte Vecchio"],
    "athens": ["The Acropolis", "Parthenon", "National Archaeological Museum"],
    "prague": ["Charles Bridge", "Prague Castle", "Old Town Square", "Astronomical Clock"],
    "vienna": ["Schönbrunn Palace", "Hofburg", "St. Stephen's Cathedral", "Belvedere Palace"],
    "budapest": ["Hungarian Parliament Building", "Buda Castle", "Fisherman's Bastion", "Széchenyi Thermal Bath"],
    "dublin": ["Guinness Storehouse", "Trinity College", "Temple Bar", "Dublin Castle"],
    "lisbon": ["Belém Tower", "Jerónimos Monastery", "Castelo de S. Jorge", "Alfama"],
    "edinburgh": ["Edinburgh Castle", "Arthur's Seat", "Royal Mile", "Palace of Holyroodhouse"],

    # Asian & Middle Eastern Cities
    "tokyo": ["Tokyo Skytree", "Senso-ji Temple", "Shibuya Crossing", "Meiji Shrine", "Imperial Palace"],
    "kyoto": ["Fushimi Inari Shrine", "Kinkaku-ji (Golden Pavilion)", "Arashiyama Bamboo Grove", "Kiyomizu-dera"],
    "osaka": ["Osaka Castle", "Dotonbori", "Universal Studios Japan", "Umeda Sky Building"],
    "agra": ["The Taj Mahal", "Agra Fort", "Fatehpur Sikri"],
    "delhi": ["Red Fort", "India Gate", "Qutub Minar", "Humayun's Tomb"],
    "mumbai": ["Gateway of India", "Marine Drive", "Elephanta Caves"],
    "bangkok": ["Grand Palace", "Wat Arun", "Chatuchak Market", "Wat Phra Kaew"],
    "singapore": ["Marina Bay Sands", "Gardens by the Bay", "Sentosa Island", "Merlion Park"],
    "kuala lumpur": ["Petronas Twin Towers", "Batu Caves", "KL Tower"],
    "seoul": ["Gyeongbokgung Palace", "N Seoul Tower", "Bukchon Hanok Village", "Myeong-dong"],
    "beijing": ["The Great Wall of China", "Forbidden City", "Temple of Heaven", "Summer Palace"],
    "shanghai": ["The Bund", "Oriental Pearl Tower", "Yu Garden"],
    "hong kong": ["Victoria Peak", "Tian Tan Buddha", "Hong Kong Disneyland", "Star Ferry"],
    "dubai": ["Burj Khalifa", "The Dubai Mall", "Palm Jumeirah", "Dubai Marina"],
    "abu dhabi": ["Sheikh Zayed Grand Mosque", "Louvre Abu Dhabi", "Ferrari World"],
    "jerusalem": ["Western Wall", "Dome of the Rock", "Church of the Holy Sepulchre"],

    # South America, Africa & Oceania
    "cairo": ["Pyramids of Giza", "The Great Sphinx", "Egyptian Museum", "Khan el-Khalili"],
    "rio": ["Christ the Redeemer", "Sugarloaf Mountain", "Copacabana Beach", "Ipanema Beach"],
    "rio de janeiro": ["Christ the Redeemer", "Sugarloaf Mountain", "Copacabana Beach"],
    "buenos aires": ["Teatro Colón", "La Boca", "Casa Rosada", "Recoleta Cemetery"],
    "lima": ["Plaza Mayor", "Huaca Pucllana", "Larco Museum"],
    "sydney": ["Sydney Opera House", "Sydney Harbour Bridge", "Bondi Beach", "Taronga Zoo"],
    "melbourne": ["Federation Square", "Royal Botanic Gardens", "Great Ocean Road", "Melbourne Cricket Ground"],
    "cape town": ["Table Mountain", "Cape of Good Hope", "Kirstenbosch Botanical Gardens", "Robben Island"],
    "marrakech": ["Jemaa el-Fnaa", "Majorelle Garden", "Koutoubia", "Bahia Palace"],
    
    # Famous Regions/Landmarks (Direct search)
    "machu picchu": ["Machu Picchu Citadel", "Temple of the Sun", "Huayna Picchu"],
    "bali": ["Uluwatu Temple", "Sacred Monkey Forest Sanctuary", "Tegallalang Rice Terrace", "Tanah Lot"],
    "phuket": ["Big Buddha", "Phi Phi Islands", "Patong Beach", "Wat Chalong"],
    "santorini": ["Oia", "Akrotiri", "Red Beach", "Fira"],
    "petra": ["The Treasury (Al-Khazneh)", "The Monastery", "Siq"],
    
    # Country Fallbacks
    "india": ["The Taj Mahal", "Golden Temple", "Gateway of India", "Hawa Mahal", "Red Fort"],
    "france": ["The Eiffel Tower", "Palace of Versailles", "Mont Saint-Michel", "French Riviera"],
    "italy": ["The Colosseum", "Leaning Tower of Pisa", "Pompeii", "Amalfi Coast"],
    "japan": ["Mount Fuji", "Fushimi Inari Shrine", "Osaka Castle", "Hiroshima Peace Memorial"],
    "egypt": ["Pyramids of Giza", "Valley of the Kings", "Karnak Temple", "Abu Simbel"],
    "usa": ["Statue of Liberty", "Grand Canyon", "Yellowstone National Park", "Yosemite National Park"],
    "united states": ["Statue of Liberty", "Grand Canyon", "Yellowstone National Park", "Yosemite National Park"],
    "uk": ["Big Ben", "Stonehenge", "Loch Ness", "Edinburgh Castle"],
    "united kingdom": ["Big Ben", "Stonehenge", "Loch Ness", "Edinburgh Castle"],
    "spain": ["La Sagrada Familia", "Alhambra", "Prado Museum", "Ibiza"],
    "germany": ["Neuschwanstein Castle", "Brandenburg Gate", "Cologne Cathedral", "Black Forest"],
    "brazil": ["Christ the Redeemer", "Iguazu Falls", "Amazon Rainforest"],
    "australia": ["Sydney Opera House", "Great Barrier Reef", "Uluru", "Bondi Beach"],
    "mexico": ["Chichen Itza", "Tulum Ruins", "Teotihuacan", "Copper Canyon"],
    "china": ["The Great Wall of China", "Terracotta Army", "Forbidden City", "The Bund"],
    "south africa": ["Kruger National Park", "Table Mountain", "Cape of Good Hope"],
    "greece": ["The Acropolis", "Santorini Caldera", "Meteora Monasteries"],
    "thailand": ["Grand Palace", "Phi Phi Islands", "Ayutthaya Historical Park"],
    "turkey": ["Hagia Sophia", "Pamukkale", "Cappadocia", "Ephesus"],
    "switzerland": ["The Matterhorn", "Lake Geneva", "Jungfraujoch", "Château de Chillon"],
    "portugal": ["Belém Tower", "Pena Palace", "Algarve Coast", "Douro Valley"],
    "ireland": ["Cliffs of Moher", "Ring of Kerry", "Guinness Storehouse", "Blarney Castle"],
    "new zealand": ["Milford Sound", "Hobbiton Movie Set", "Tongariro National Park", "Fiordland"]
}


@app.route('/api/weather', methods=['GET'])
@app.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    destination = request.args.get('dest')

    if not destination and (not lat or not lon):
        return jsonify({"error": "Missing coordinates or destination"}), 400

    if not lat or not lon:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={destination}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url).json()
        if not geo_resp.get("results"):
            return jsonify({"error": "Destination not found"}), 404
        
        location = geo_resp["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
    
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_resp = requests.get(weather_url).json()

    if "current_weather" not in weather_resp:
         return jsonify({"error": "Weather data unavailable"}), 500

    weather_data = weather_resp["current_weather"]
    
    code_map = {
        0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
        45: 'Fog', 48: 'Depositing rime fog',
        51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
        61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
        71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
        95: 'Thunderstorm'
    }
    condition = code_map.get(weather_data.get('weathercode', 0), 'Unknown')
    temp = weather_data.get('temperature', 0)
    
    tips = "Perfect travel weather."
    if temp < 10:
        tips = "It's quite cold out there. Pack warm layers!"
    elif temp > 30:
        tips = "Very hot! Stay hydrated and wear sunscreen."
        
    if weather_data.get('weathercode', 0) in [61, 63, 65, 95]:
        tips += " Looks like rain or storms. Bring an umbrella."

    return jsonify({
        "temperature": temp,
        "condition": condition,
        "tips": tips
    })

def get_location_data(dest):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={dest}&count=1&language=en&format=json"
    country = "Unknown"
    try:
        geo_resp = requests.get(geo_url).json()
        if not geo_resp.get("results"):
            return [], country, 0, 0
        
        loc_data = geo_resp["results"][0]
        lat = loc_data["latitude"]
        lon = loc_data["longitude"]
        country = loc_data.get("country", "Unknown")
        
        query = f"""
        [out:json];
        (
          node["tourism"~"museum|gallery|theme_park"](around:25000,{lat},{lon});
          way["historic"~"monument|castle|ruins"](around:25000,{lat},{lon});
          node["historic"~"monument|castle|ruins"](around:25000,{lat},{lon});
          node["leisure"~"park|garden"](around:25000,{lat},{lon});
        );
        out center 25;
        """
        url = "http://overpass-api.de/api/interpreter"
        resp = requests.post(url, data={'data': query}, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            places = [el.get('tags', {}).get('name') for el in data.get('elements', []) if el.get('tags', {}).get('name')]
            return list(set(places)), country, lat, lon
    except Exception as e:
        print("Error fetching real places:", e)
    return [], country, 0, 0

def generate_itinerary(dest, days, interests, places, signature_food):
    days_list = []
    
    activities = []
    for p in places:
        activities.append(f"Visit the magnificent {p}.")
        activities.append(f"Explore the area around {p}.")
        
    fallback = [
         f"Enjoy a local culinary tour downtown.",
         f"Explore historical landmarks in the morning.",
         f"Spend the day doing outdoor activities (hiking/walking).",
         f"Shopping and souvenir hunting in distinct neighborhoods.",
         f"Sunset watching at a scenic viewpoint."
    ]
    activities.extend(fallback)
    
    if interests:
        activities.insert(0, f"Special activity focused on: {interests}")

    for i in range(days):
        food_suggestion = signature_food if i == 0 else "a highly rated local spot"
        days_list.append({
            "day": i + 1,
            "title": f"Day {i+1} Explorer",
            "activities": [
                 random.choice(activities),
                 random.choice(activities),
                 f"Dinner featuring {food_suggestion}."
            ]
        })
    return days_list

@app.route('/api/plan-trip', methods=['POST'])
@app.route('/plan-trip', methods=['POST'])
def plan_trip():
    data = request.json
    dest = data.get('destination', 'Unknown')
    days = int(data.get('days', 3))
    interests = data.get('interests', '')
    flight_option = data.get('flightOption', 'any')
    hotel_choice = data.get('hotelChoice', '')

    if not dest or days <= 0:
         return jsonify({"error": "Invalid input"}), 400

    places, country, lat, lon = get_location_data(dest)
    
    culture_info = CULTURE_DB.get(country, {
        "food": f"Ask the locals in {country} for their top recommended regional dishes or specialty street food.",
        "culture": f"Embrace the local {country} traditions. Read up on specific etiquette before you arrive to show respect.",
        "safety": f"Maintain standard travel awareness while exploring {dest}. Keep valuables secure in crowded public areas.",
        "language": f"National language of {country}. Consider learning basic greetings before you travel.",
        "currency": f"Local {country} currency. We recommend researching the current exchange rate and keeping local cash on hand.",
        "mult": 0.9
    })

    food_list = culture_info["food"].split(',')
    signature_food = food_list[0].strip() if food_list else "local delicacies"
    base_cost = int(days * 100 * culture_info["mult"])

    packages = [
        {
            "id": "budget",
            "name": "Low Budget",
            "description": "Affordable travel keeping costs low.",
            "estimatedCost": f"${base_cost}",
            "hotel": "Hostels or 2-Star Hotels",
            "flights": "Economy class, connecting flights",
            "transportation": "Public transit (buses/subway)",
            "itinerary": generate_itinerary(dest, days, interests, places, signature_food)
        },
        {
            "id": "medium",
            "name": "Medium Budget",
            "description": "A comfortable balance of value and experience.",
            "estimatedCost": f"${base_cost * 2}",
            "hotel": "3 to 4-Star Hotels",
            "flights": "Premium Economy, direct flights",
            "transportation": "Ride-hailing apps & public transit",
            "itinerary": generate_itinerary(dest, days, interests, places, signature_food)
        },
        {
            "id": "high",
            "name": "High Budget",
            "description": "Luxury travel experience without compromises.",
            "estimatedCost": f"${int(base_cost * 4.5)}",
            "hotel": "5-Star Resorts",
            "flights": "Business Class",
            "transportation": "Private car service",
            "itinerary": generate_itinerary(dest, days, interests, places, signature_food)
        }
    ]
    
    for pkg in packages:
        if hotel_choice:
            pkg["hotel"] = f"{hotel_choice} (User Preferred)"
        
        if flight_option == "none":
            pkg["flights"] = "N/A - Arranged by User"
        elif flight_option == "economy":
            pkg["flights"] = "Economy Class"
        elif flight_option == "business":
            pkg["flights"] = "Business/First Class"

    dest_lower = dest.lower().strip()
    country_lower = country.lower().strip() if country else ""
    
    iconic_sights = FAMOUS_LANDMARKS.get(dest_lower, [])
    if not iconic_sights:
        iconic_sights = FAMOUS_LANDMARKS.get(country_lower, [])

    # Combine iconic sights first, then pad with dynamic map data, remove duplicates
    all_places = iconic_sights.copy()
    for p in places:
        if p not in all_places:
            all_places.append(p)

    must_visits = []
    if all_places:
        for i, p in enumerate(all_places[:10]):
            must_visits.append({"name": p, "category": "Top Attraction", "desc": f"Iconic landmark or cultural site for your trip."})
    else:
        must_visits = [
            {"name": f"The Great {dest} Square", "category": "Historical", "desc": "Central historical spot representing the city's past."},
            {"name": f"{dest} Observatory", "category": "Entertainment", "desc": "Get a bird's eye view of the entire area."},
            {"name": f"Local {dest} Market", "category": "Shopping/Food", "desc": "Authentic street food and local crafts."}
        ]

    local_guide = {
        "culture": culture_info["culture"],
        "food": f"You must try {culture_info['food']}. It is a culinary requirement here!",
        "safety": culture_info["safety"],
        "language": culture_info.get("language", f"National language of {country}."),
        "currency": culture_info.get("currency", "Local currency")
    }

    return jsonify({
        "destination": dest,
        "days": days,
        "lat": lat,
        "lon": lon,
        "packages": packages,
        "mustVisits": must_visits,
        "localGuide": local_guide
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
