from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

CULTURE_DB = {
    "Italy": {"food": "Pasta Carbonara, Neapolitan Pizza, and Gelato", "culture": "Greet with 'Buongiorno'. Dinner is usually late (8PM+). Dress smartly.", "safety": "Beware of pickpockets in crowded tourist spots like train stations.", "mult": 1.5, "language": "Italian • Hello: Buongiorno • Thanks: Grazie", "currency": "Euro (€)"},
    "France": {"food": "Croissants, Escargot, and Boeuf Bourguignon", "culture": "Always say 'Bonjour' when entering a shop. Embrace the cafe culture.", "safety": "Watch for petty theft around major landmarks.", "mult": 1.6, "language": "French • Hello: Bonjour • Thanks: Merci", "currency": "Euro (€)"},
    "Japan": {"food": "Fresh Sushi, rich Ramen bowls, and Takoyaki", "culture": "Bowing is the standard greeting. Tipping is considered rude.", "safety": "Extremely safe, but observe etiquette on public transit.", "mult": 1.8, "language": "Japanese • Hello: Konnichiwa • Thanks: Arigatou", "currency": "Japanese Yen (¥)"},
    "Turkey": {"food": "Iskender Kebab, Baklava, and Turkish Delight", "culture": "Bargaining is common in bazaars. Accept tea if offered.", "safety": "Generally safe. Use marked taxis and be mindful in busy markets.", "mult": 0.8, "language": "Turkish • Hello: Merhaba • Thanks: Teşekkürler", "currency": "Turkish Lira (₺)"},
    "United Kingdom": {"food": "Fish and Chips, Sunday Roast, and Full English Breakfast", "culture": "Stand on the right on escalators. Queuing (standing in line) is practically a religion.", "safety": "Safe, but look both ways before crossing (cars drive on left).", "mult": 1.7, "language": "English", "currency": "British Pound (£)"},
    "United States": {"food": "Burgers, BBQ Ribs, and regional specialties", "culture": "Tipping (15-20%) is mandatory. Portions are usually very large.", "safety": "Varies by neighborhood; use standard urban awareness.", "mult": 1.8, "language": "English", "currency": "US Dollar ($)"},
    "Thailand": {"food": "Pad Thai, Green Curry, and Mango Sticky Rice", "culture": "Do not touch people's heads. Respect the royal family completely.", "safety": "Watch out for tuk-tuk scams and drink bottled water.", "mult": 0.6, "language": "Thai • Hello: Sawasdee • Thanks: Khop Khun", "currency": "Thai Baht (฿)"},
    "India": {"food": "Butter Chicken, Masala Dosa, and Biryani", "culture": "Use your right hand for eating and giving/receiving objects.", "safety": "Drink only bottled water. Negotiate fare before entering an auto-rickshaw.", "mult": 0.5, "language": "Hindi / English • Hello: Namaste • Thanks: Dhanyavad", "currency": "Indian Rupee (₹)"},
    "United Arab Emirates": {"food": "Shawarma, Machboos, and Falafel", "culture": "Dress modestly in public spaces. Weekends are Friday/Saturday.", "safety": "Extremely safe with strict laws. Public transport is excellent.", "mult": 1.6, "language": "Arabic • Hello: Marhaba • Thanks: Shukran", "currency": "UAE Dirham (AED)"},
    "Spain": {"food": "Tapas, Paella, and Churros con Chocolate", "culture": "Siesta is real; shops may close mid-day. Dinner happens after 9 PM.", "safety": "Beware of pickpockets in major cities like Barcelona and Madrid.", "mult": 1.3, "language": "Spanish • Hello: Hola • Thanks: Gracias", "currency": "Euro (€)"},
    "Mexico": {"food": "Street Tacos, Mole, and Chilaquiles", "culture": "Warm and festive. Learning a bit of Spanish goes a long way.", "safety": "Stick to tourist zones and use registered taxis or rideshares.", "mult": 0.7, "language": "Spanish • Hello: Hola • Thanks: Gracias", "currency": "Mexican Peso ($)"},
    "Greece": {"food": "Moussaka, Souvlaki, and fresh Greek Salad", "culture": "Pace of life is relaxed. Hospitality (philoxenia) is very important.", "safety": "Very safe. Be cautious on roads if renting a scooter.", "mult": 1.1, "language": "Greek • Hello: Yassou • Thanks: Efharisto", "currency": "Euro (€)"},
    "Germany": {"food": "Bratwurst, Pretzels, and Schnitzel", "culture": "Punctuality is essential. Toast with 'Prost' and make eye contact.", "safety": "Highly safe infrastructure. Observe pedestrian lights.", "mult": 1.4, "language": "German • Hello: Hallo • Thanks: Danke", "currency": "Euro (€)"},
    "Egypt": {"food": "Koshari, Ful Medames, and Shawarma", "culture": "Dress conservatively outside of resorts. Bargaining is expected.", "safety": "Stay hydrated. Cross bustling streets with confident locals.", "mult": 0.6, "language": "Arabic • Hello: Marhaba • Thanks: Shukran", "currency": "Egyptian Pound (E£)"},
    "Brazil": {"food": "Feijoada, Pão de Queijo, and Churrasco", "culture": "Very warm and affectionate people. Thumbs up is a common greeting.", "safety": "Keep phones out of sight in crowded urban areas.", "mult": 0.9, "language": "Portuguese • Hello: Olá • Thanks: Obrigado/a", "currency": "Brazilian Real (R$)"}
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
          node["tourism"~"museum|gallery|theme_park"](around:10000,{lat},{lon});
          way["historic"~"monument|castle|ruins"](around:10000,{lat},{lon});
          node["historic"~"monument|castle|ruins"](around:10000,{lat},{lon});
        );
        out center 15;
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
        "food": f"Ask locals for the best authentic {dest} dishes and street food.",
        "culture": f"Observe local customs and be respectful of the {country} way of life.",
        "safety": "Maintain standard travel awareness. Keep valuables secure in crowded areas.",
        "language": f"National language of {country}. English often spoken in tourist areas.",
        "currency": "Local currency. Check exchange rates.",
        "mult": 1.0
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

    must_visits = []
    if places:
        for i, p in enumerate(places[:3]):
            must_visits.append({"name": p, "category": "Top Attraction", "desc": f"Famous landmark located in {dest}."})
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

