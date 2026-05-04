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
    "New Zealand": {"food": "Hangi, Fish and Chips, Pavlova", "culture": "Very eco-conscious. Māori culture is highly respected.", "safety": "Extremely safe. Weather can change rapidly.", "mult": 1.5, "language": "English, Māori", "currency": "New Zealand Dollar (NZD)"},
    "Singapore": {"food": "Hainanese Chicken Rice, Chili Crab, Laksa", "culture": "Efficiency-driven and extremely orderly. Respect for laws is paramount.", "safety": "One of the safest cities in the world. Strict on littering.", "mult": 1.6, "language": "English, Mandarin, Malay, Tamil", "currency": "Singapore Dollar (SGD)"},
    "Malaysia": {"food": "Nasi Lemak, Satay, Roti Canai", "culture": "Multi-ethnic and religious. Dress modestly in rural areas.", "safety": "Generally safe. Use ride-hailing apps like Grab.", "mult": 0.6, "language": "Malay, English", "currency": "Malaysian Ringgit (MYR)"},
    "Philippines": {"food": "Adobo, Sinigang, Lechon", "culture": "Very hospitable and music-loving. Respect for elders (Mano Po).", "safety": "Stick to tourist hubs. Use official transport.", "mult": 0.5, "language": "Filipino, English", "currency": "Philippine Peso (PHP)"},
    "Israel": {"food": "Hummus, Falafel, Shakshuka", "culture": "Direct communication. Shabbat (Friday sunset to Saturday sunset) is a rest day.", "safety": "High security awareness. Follow local guidelines.", "mult": 1.4, "language": "Hebrew, Arabic", "currency": "Israeli Shekel (ILS)"},
    "Norway": {"food": "Smoked Salmon, Brown Cheese, Reindeer meat", "culture": "Love for the outdoors (Friluftsliv). Very egalitarian and reserved.", "safety": "Extremely safe. Nature is the biggest hazard; dress for the cold.", "mult": 2.1, "language": "Norwegian • Hello: Hallo", "currency": "Norwegian Krone (NOK)"},
    "Sweden": {"food": "Meatballs with Lingonberries, Gravlax, Fika (coffee break)", "culture": "Value for consensus and equality (Lagom). Fika is a daily ritual.", "safety": "Very safe. Observe recycling rules and avoid being loud in public.", "mult": 1.7, "language": "Swedish • Hello: Hej", "currency": "Swedish Krona (SEK)"},
    "Denmark": {"food": "Smørrebrød (open sandwiches), Danish pastries, Hot Dogs", "culture": "Focused on coziness and well-being (Hygge). Cycling is life.", "safety": "Extremely safe. Use bike lanes and follow traffic signals strictly.", "mult": 1.8, "language": "Danish • Hello: Hej", "currency": "Danish Krone (DKK)"},
    "Poland": {"food": "Pierogi, Kielbasa, Bigos (Hunter's Stew)", "culture": "Hospitality and history are key. Poles are proud of their heritage.", "safety": "Generally very safe. Watch for traffic and crosswalk rules.", "mult": 0.8, "language": "Polish • Hello: Cześć", "currency": "Polish Złoty (PLN)"},
    "Czech Republic": {"food": "Goulash, Svíčková, Fried Cheese, World-class beer", "culture": "Appreciation for arts and history. Tipping (10%) is standard.", "safety": "Safe, but watch for pickpockets in Prague's Old Town.", "mult": 0.9, "language": "Czech • Hello: Ahoj", "currency": "Czech Koruna (CZK)"},
    "Hungary": {"food": "Goulash, Lángos, Dobos Tort (Cake)", "culture": "Rich bathing culture (thermal baths). High regard for music and wine.", "safety": "Safe. Use official taxis and check prices in tourist restaurants.", "mult": 0.7, "language": "Hungarian • Hello: Szia", "currency": "Hungarian Forint (HUF)"},
    "Austria": {"food": "Wiener Schnitzel, Sachertorte, Apple Strudel", "culture": "Polite and formal. Respect for classical music and mountain traditions.", "safety": "Extremely safe. Be careful during mountain activities.", "mult": 1.5, "language": "German • Hello: Servus", "currency": "Euro (€)"},
    "Argentina": {"food": "Asado (BBQ), Empanadas, Alfajores", "culture": "Passionate about football and tango. Dinner is very late (9PM+).", "safety": "Standard urban awareness. Stick to well-lit areas in Buenos Aires.", "mult": 0.8, "language": "Spanish • Hello: Hola", "currency": "Argentine Peso ($)"},
    "Chile": {"food": "Pastel de Choclo, Empanadas de Pino, Ceviche", "culture": "Polite and focused on community. National pride in poets like Neruda.", "safety": "Safe, but be cautious of earthquakes and pickpockets in Santiago.", "mult": 1.0, "language": "Spanish • Hello: Hola", "currency": "Chilean Peso ($)"},
    "Peru": {"food": "Ceviche, Lomo Saltado, Cuy (Guinea Pig)", "culture": "Proud Incan heritage. Respect for the Earth (Pachamama).", "safety": "Use registered taxis. Altitude sickness is common in the Andes.", "mult": 0.7, "language": "Spanish • Hello: Hola", "currency": "Peruvian Sol (S/.)"},
    "Colombia": {"food": "Bandeja Paisa, Arepas, Ajiaco", "culture": "Extremely warm and musical. Value for family and resilience.", "safety": "Major improvements. Stick to tourist areas; avoid 'no-go' zones.", "mult": 0.7, "language": "Spanish • Hello: Hola", "currency": "Colombian Peso ($)"},
    "Morocco": {"food": "Tagine, Couscous, Harira soup", "culture": "Hospitality involves mint tea. Modest dress is required in many areas.", "safety": "Safe, but beware of aggressive vendors in the souks.", "mult": 0.6, "language": "Arabic, French • Hello: Salam", "currency": "Moroccan Dirham (MAD)"},
    "Kenya": {"food": "Ugali, Nyama Choma (Roasted meat), Pilau", "culture": "Warm and diverse. Respect for wildlife and tribal traditions.", "safety": "Stick to guided safaris and safe neighborhoods in Nairobi.", "mult": 0.7, "language": "Swahili, English • Hello: Jambo", "currency": "Kenyan Shilling (KSh)"},
    "Taiwan": {"food": "Beef Noodle Soup, Bubble Tea, Xiaolongbao", "culture": "Extremely polite and hospitable. High respect for temples and elders.", "safety": "Extremely safe even at night. Great public transit.", "mult": 1.2, "language": "Mandarin • Hello: Nǐ hǎo", "currency": "New Taiwan Dollar (TWD)"},
    "Saudi Arabia": {"food": "Kabsa, Mandi, Arabic Coffee & Dates", "culture": "Conservative and deeply religious. Respect for Islamic laws is mandatory.", "safety": "Very safe. Be mindful of strict cultural codes and prayer times.", "mult": 1.5, "language": "Arabic • Hello: Marhaba", "currency": "Saudi Riyal (SAR)"}
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
    "santiago": ["San Cristóbal Hill", "Plaza de Armas", "La Chascona", "Cajón del Maipo"],
    "lima": ["Plaza Mayor", "Huaca Pucllana", "Larco Museum", "Magic Water Circuit"],
    "bogota": ["Monserrate", "Gold Museum", "La Candelaria", "Botero Museum"],
    "oslo": ["Vigeland Park", "Viking Ship Museum", "Opera House", "Holmenkollen"],
    "stockholm": ["Vasa Museum", "Gamla Stan", "Skansen", "ABBA The Museum"],
    "copenhagen": ["The Little Mermaid", "Tivoli Gardens", "Nyhavn", "Amalienborg"],
    "prague": ["Charles Bridge", "Prague Castle", "Old Town Square", "Astronomical Clock"],
    "vienna": ["Schönbrunn Palace", "St. Stephen's Cathedral", "Hofburg", "Belvedere"],
    "budapest": ["Parliament Building", "Buda Castle", "Fisherman's Bastion", "Széchenyi Baths"],
    "warsaw": ["Old Town Market Square", "Royal Castle", "Łazienki Park", "Palace of Culture"],
    "nairobi": ["Nairobi National Park", "Giraffe Centre", "David Sheldrick Wildlife Trust"],
    "marrakesh": ["Jemaa el-Fnaa", "Majorelle Garden", "Bahia Palace", "Koutoubia"],
    "taipei": ["Taipei 101", "National Palace Museum", "Shilin Night Market", "Elephant Mountain"],
    "riyadh": ["Kingdom Centre", "Masmak Fortress", "Diriyah", "National Museum"],
    
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
    "new zealand": ["Milford Sound", "Hobbiton Movie Set", "Tongariro National Park", "Waitomo Caves"],
    "malaysia": ["Petronas Twin Towers", "Batu Caves", "Langkawi Archipelago", "Mount Kinabalu"],
    "philippines": ["El Nido (Palawan)", "Chocolate Hills", "Boracay White Beach"],
    "austria": ["Schönbrunn Palace", "Hallstatt", "Salzburg Old Town"],
    "norway": ["Geirangerfjord", "Lofoten Islands", "Trolltunga", "The Northern Lights"],
    "sweden": ["Vasa Museum", "Stockholm Archipelago", "Ice Hotel", "Turning Torso"],
    "denmark": ["Tivoli Gardens", "Legoland", "The Little Mermaid", "Nyhavn"],
    "poland": ["Auschwitz-Birkenau", "Wieliczka Salt Mine", "Wawel Castle"],
    "czech republic": ["Prague Castle", "Charles Bridge", "Kutná Hora"],
    "hungary": ["Parliament Building", "Lake Balaton", "Thermal Baths"],
    "argentina": ["Iguazu Falls", "Perito Moreno Glacier", "La Boca"],
    "chile": ["Torres del Paine", "Atacama Desert", "Easter Island"],
    "peru": ["Machu Picchu", "Nazca Lines", "Lake Titicaca"],
    "colombia": ["Cartagena Old Town", "Tayrona Park", "Coffee Triangle"],
    "morocco": ["Sahara Desert", "Chefchaouen", "Atlas Mountains"],
    "kenya": ["Maasai Mara", "Mount Kenya", "Diani Beach"],
    "taiwan": ["Taroko Gorge", "Alishan", "Sun Moon Lake"],
    "saudi arabia": ["Al-Ula", "Edge of the World", "Red Sea Project"]
}

# ─── NEW TRAVEL INTEL DATABASES ───────────────────────────────────

BEST_TIME_DB = {
    "Japan": {"months": "Mar-May, Oct-Nov", "advice": "Spring for cherry blossoms, Autumn for foliage. Avoid June (rain) and Aug (heat)."},
    "France": {"months": "Apr-Jun, Sep-Oct", "advice": "Spring and Autumn offer mild weather and fewer crowds than July/August."},
    "Italy": {"months": "Apr-Jun, Sep-Oct", "advice": "Perfect temperatures. July/August can be sweltering and extremely crowded."},
    "Thailand": {"months": "Nov-Feb", "advice": "Cool and dry season. Avoid Sep-Oct due to heavy monsoon rains."},
    "India": {"months": "Oct-Mar", "advice": "Best weather for most regions. Apr-Jun is extremely hot; Jul-Sep is monsoon."},
    "USA": {"months": "Apr-Jun, Sep-Oct", "advice": "Spring and Fall are ideal for most states. Summer is peak but hot."},
    "United Kingdom": {"months": "May-Sep", "advice": "Warmest months and longest daylight hours. Be ready for rain anytime."},
    "UAE": {"months": "Nov-Mar", "advice": "Pleasant outdoor weather. Avoid Jun-Sep as temperatures exceed 40°C."},
    "Turkey": {"months": "Apr-May, Sep-Oct", "advice": "Ideal for exploring ruins and cities. Summer is great for beaches."},
    "Greece": {"months": "May-Jun, Sep-Oct", "advice": "Great weather, everything is open, and prices are lower than August."},
    "Mexico": {"months": "Dec-Apr", "advice": "Dry season. May-Nov is rainy and hurricane season on the coasts."},
    "Brazil": {"months": "Sep-Nov, Mar-May", "advice": "Avoid peak summer heat and humidity if you aren't there for Carnival."},
    "Egypt": {"months": "Oct-Apr", "advice": "Ideal for monuments. May-Sep is dangerously hot in the desert."},
    "Australia": {"months": "Sep-Nov, Mar-May", "advice": "Spring and Autumn. Note that seasons are reversed (Summer is Dec-Feb)."},
    "Spain": {"months": "Apr-Jun, Sep-Oct", "advice": "Ideal for sightseeing. July/August is very hot, especially in the south."},
    "Canada": {"months": "Jun-Aug, Sep-Oct", "advice": "Summer for hiking and festivals. Fall for spectacular foliage."},
    "Singapore": {"months": "Feb-Apr", "advice": "Slightly less rain. It is humid and tropical year-round."},
    "Germany": {"months": "May-Sep, Dec", "advice": "Summer for gardens and beer festivals. December for Christmas Markets."},
    "Switzerland": {"months": "Jun-Sep, Dec-Mar", "advice": "Summer for hiking; Winter for world-class skiing and cozy chalets."},
    "South Korea": {"months": "Apr-Jun, Sep-Nov", "advice": "Cherry blossoms in Spring, vibrant colors in Autumn. Avoid July/August (monsoon/heat)."},
    "Vietnam": {"months": "Nov-Apr", "advice": "Dry season for most of the country. North can be chilly in Jan/Feb."},
    "Indonesia": {"months": "May-Sep", "advice": "Dry season. Perfect for Bali and island hopping. Oct-Apr is rainy."},
    "Portugal": {"months": "Mar-May, Sep-Oct", "advice": "Pleasant weather, great for coastal walks and wine tasting."},
    "Maldives": {"months": "Nov-Apr", "advice": "Peak dry season. Clear blue skies and perfect for diving."},
    "Netherlands": {"months": "Apr-May, Jun-Aug", "advice": "April/May for tulips. Summer for cycling and canal festivals."},
    "Norway": {"months": "Jun-Aug, Dec-Mar", "advice": "Summer for fjords and hiking; Winter for Northern Lights and skiing."},
    "Sweden": {"months": "Jun-Aug, Dec-Mar", "advice": "Summer for Stockholm archipelago; Winter for Lapland and skiing."},
    "Denmark": {"months": "May-Aug, Dec", "advice": "Summer for beaches and cycling. December for Christmas markets."},
    "Poland": {"months": "May-Jun, Sep-Oct", "advice": "Spring and Fall offer mild weather and beautiful landscapes."},
    "Czech Republic": {"months": "May-Sep, Dec", "advice": "Summer for festivals. December for magical Christmas markets."},
    "Hungary": {"months": "May-Jun, Sep-Oct", "advice": "Ideal for exploring Budapest and the wine regions."},
    "Austria": {"months": "Jun-Aug, Dec-Mar", "advice": "Summer for lakes and hiking; Winter for world-class skiing."},
    "Argentina": {"months": "Oct-Dec, Mar-May", "advice": "Spring and Autumn. Note that Patagonia is best in Summer (Dec-Feb)."},
    "Chile": {"months": "Oct-Apr", "advice": "Best time for hiking in Patagonia and exploring Santiago."},
    "Peru": {"months": "May-Sep", "advice": "Dry season in the Andes. Perfect for Machu Picchu and trekking."},
    "Colombia": {"months": "Dec-Mar", "advice": "Dry season. Ideal for Caribbean beaches and Coffee Region."},
    "Morocco": {"months": "Mar-May, Sep-Nov", "advice": "Pleasant temperatures for exploring cities and the desert."},
    "Kenya": {"months": "Jul-Oct, Jan-Feb", "advice": "Great Migration occurs Jul-Oct. Dry season is best for safaris."},
    "Taiwan": {"months": "Oct-Apr", "advice": "Cooler and drier weather. Spring for cherry blossoms."},
    "Saudi Arabia": {"months": "Nov-Mar", "advice": "Coolest months. Avoid summer heat (May-Sep)."}
}

TIMEZONE_DB = {
    "Japan": "Asia/Tokyo", "France": "Europe/Paris", "Italy": "Europe/Rome", "Thailand": "Asia/Bangkok",
    "India": "Asia/Kolkata", "USA": "America/New_York", "United Kingdom": "Europe/London", "UAE": "Asia/Dubai",
    "Turkey": "Europe/Istanbul", "Greece": "Europe/Athens", "Mexico": "America/Mexico_City", "Brazil": "America/Sao_Paulo",
    "Egypt": "Africa/Cairo", "Australia": "Australia/Sydney", "Canada": "America/Toronto", "Spain": "Europe/Madrid",
    "Singapore": "Asia/Singapore", "Germany": "Europe/Berlin", "Switzerland": "Europe/Zurich", "South Korea": "Asia/Seoul",
    "Vietnam": "Asia/Ho_Chi_Minh", "Indonesia": "Asia/Jakarta", "Portugal": "Europe/Lisbon", "Maldives": "Indian/Maldives",
    "Netherlands": "Europe/Amsterdam", "South Africa": "Africa/Johannesburg", "New Zealand": "Pacific/Auckland",
    "Norway": "Europe/Oslo", "Sweden": "Europe/Stockholm", "Denmark": "Europe/Copenhagen", "Poland": "Europe/Warsaw",
    "Czech Republic": "Europe/Prague", "Hungary": "Europe/Budapest", "Austria": "Europe/Vienna", "Argentina": "America/Argentina/Buenos_Aires",
    "Chile": "America/Santiago", "Peru": "America/Lima", "Colombia": "America/Bogota", "Morocco": "Africa/Casablanca",
    "Kenya": "Africa/Nairobi", "Taiwan": "Asia/Taipei", "Saudi Arabia": "Asia/Riyadh"
}

SCAM_DB = {
    "Japan": [{"title": "Overpriced Bars", "desc": "Touts in Roppongi/Kabukicho may lure you into bars with 'cheap' drinks but hit you with huge hidden fees."}],
    "France": [{"title": "The Friendship Bracelet", "desc": "Someone tries to tie a string around your finger in Montmartre and then demands payment."}],
    "Italy": [{"title": "Helpful Luggage Carriers", "desc": "Random people at stations grab your bags to 'help' and then demand a high tip."}],
    "Thailand": [{"title": "Grand Palace is Closed", "desc": "Tuk-tuk drivers tell you the Palace is closed for a holiday to take you to overpriced gem shops."}],
    "India": [{"title": "The Fake Tourist Office", "desc": "Drivers claim your hotel is closed/full and take you to a 'government' agency to rebook at 5x price."}],
    "Turkey": [{"title": "The Shoe Brusher", "desc": "A brusher drops their brush, you pick it up, they 'thank' you with a brush and then charge you."}],
    "Spain": [{"title": "Bird Dropping Scam", "desc": "Someone sprays a substance on you, offers to clean it, and picks your pocket in the process."}],
    "Vietnam": [{"title": "The Coconut Guy", "desc": "Someone puts a coconut yoke on your shoulder for a photo, then demands a huge fee."}],
    "USA": [{"title": "CD Handout", "desc": "In NYC/LA, people hand you a 'free' CD, then aggressively demand a 'donation' once it's in your hand."}],
    "Egypt": [{"title": "Free Camel Ride", "desc": "Getting on the camel is 'free', but you have to pay a massive fee to get down."}],
    "Morocco": [{"title": "The Henna Scam", "desc": "Women aggressively grab your hand to start a henna tattoo and then demand payment for the 'service'."}],
    "Czech Republic": [{"title": "Currency Exchange Trap", "desc": "Unofficial exchange booths offer poor rates or huge fees hidden in fine print."}],
    "Hungary": [{"title": "Overpriced Menu", "desc": "Restaurants in tourist areas may show a cheap menu outside but charge much higher prices inside."}],
    "Argentina": [{"title": "The Mustard Scam", "desc": "Someone 'accidentally' spills mustard on you, helps you clean up, and pickpockets you."}]
}

APPS_DB = {
    "Japan": [{"name": "Google Maps", "usage": "Best for complex train navigation."}, {"name": "Google Translate", "usage": "Camera mode for menus."}],
    "Thailand": [{"name": "Grab", "usage": "Essential for fair-priced taxis and bikes."}, {"name": "Klook", "usage": "Discounted attraction tickets."}],
    "India": [{"name": "Ola/Uber", "usage": "Avoid rickshaw bargaining."}, {"name": "Zomato", "usage": "Top food delivery and reviews."}],
    "France": [{"name": "Citymapper", "usage": "Best for Paris Metro."}, {"name": "TheFork", "usage": "Restaurant reservations and discounts."}],
    "USA": [{"name": "Uber/Lyft", "usage": "Primary ride sharing."}, {"name": "Yelp", "usage": "Most reliable for food reviews."}],
    "Singapore": [{"name": "Grab", "usage": "Standard for rides and food."}, {"name": "Citymapper", "usage": "Best for MRT/Bus routes."}],
    "South Korea": [{"name": "Naver Maps", "usage": "Much better than Google Maps in Korea."}, {"name": "KakaoTaxi", "usage": "Leading taxi hailing app."}],
    "Germany": [{"name": "DB Navigator", "usage": "Essential for train schedules and tickets."}, {"name": "FreeNow", "usage": "Main taxi app."}],
    "Vietnam": [{"name": "Grab", "usage": "Cheapest and safest way to get around."}, {"name": "Zalo", "usage": "Local messaging app for bookings."}],
    "Spain": [{"name": "Cabify", "usage": "Better and safer than local taxis."}, {"name": "Glovo", "usage": "Multi-category delivery."}],
    "Norway": [{"name": "Vy", "usage": "Essential for train and bus tickets."}, {"name": "Ruter", "usage": "Best for Oslo public transport."}],
    "Poland": [{"name": "Jakdojade", "usage": "Leading public transport planner."}, {"name": "Bolt", "usage": "Cheap and reliable ride sharing."}],
    "Argentina": [{"name": "Cabify", "usage": "Safer alternative to street taxis."}, {"name": "PedidosYa", "usage": "Top food delivery service."}]
}

EMERGENCY_DB = {
    "Japan": {"police": "110", "medical": "119"},
    "France": {"police": "17", "medical": "15", "all": "112"},
    "USA": {"all": "911"},
    "UK": {"all": "999", "eu": "112"},
    "Thailand": {"police": "191", "tourist_police": "1155"},
    "India": {"all": "112"},
    "Spain": {"all": "112"},
    "Germany": {"police": "110", "medical": "112"},
    "Singapore": {"police": "999", "medical": "995"},
    "Australia": {"all": "000"},
    "Canada": {"all": "911"},
    "Switzerland": {"police": "117", "medical": "144", "all": "112"},
    "Norway": {"police": "112", "medical": "113"},
    "Poland": {"all": "112"},
    "Argentina": {"police": "911", "medical": "107"},
    "Kenya": {"all": "999"}
}

UTILITIES_DB = {
    "Japan": {"power": "Type A/B, 100V", "water": "Tap water is safe", "sim": "Ubigi or Airalo (eSIM) recommended"},
    "UK": {"power": "Type G, 230V", "water": "Tap water is safe", "sim": "EE or Vodafone (Pick up at airport)"},
    "USA": {"power": "Type A/B, 120V", "water": "Tap water is safe", "sim": "T-Mobile Tourist Plan"},
    "India": {"power": "Type C/D/M, 230V", "water": "Drink only bottled water", "sim": "Airtel or Jio (Requires Passport)"},
    "Thailand": {"power": "Type A/B/C/O, 220V", "water": "Drink only bottled water", "sim": "AIS or TrueMove Tourist SIM"},
    "France": {"power": "Type C/E, 230V", "water": "Tap water is safe", "sim": "Orange Holiday SIM"},
    "Germany": {"power": "Type C/F, 230V", "water": "Tap water is safe", "sim": "Telekom or Vodafone"},
    "Spain": {"power": "Type C/F, 230V", "water": "Tap water is safe", "sim": "Movistar or Orange"},
    "Singapore": {"power": "Type G, 230V", "water": "Tap water is safe", "sim": "Singtel or StarHub (7-Eleven)"},
    "Switzerland": {"power": "Type J, 230V", "water": "Tap water is world's best", "sim": "Swisscom or Salt"},
    "Norway": {"power": "Type C/F, 230V", "water": "Tap water is high quality", "sim": "Telenor or Telia"},
    "Argentina": {"power": "Type C/I, 220V", "water": "Drink bottled water in rural areas", "sim": "Claro or Personal"}
}

SPEND_DB = {
    "Japan": {"low": "$45", "mid": "$95", "high": "$280+"},
    "India": {"low": "$15", "mid": "$38", "high": "$130+"},
    "France": {"low": "$55", "mid": "$120", "high": "$320+"},
    "Thailand": {"low": "$22", "mid": "$48", "high": "$160+"},
    "USA": {"low": "$65", "mid": "$150", "high": "$400+"},
    "UK": {"low": "$60", "mid": "$140", "high": "$350+"},
    "Singapore": {"low": "$50", "mid": "$115", "high": "$300+"},
    "Switzerland": {"low": "$80", "mid": "$180", "high": "$450+"},
    "Vietnam": {"low": "$18", "mid": "$35", "high": "$110+"},
    "Spain": {"low": "$45", "mid": "$90", "high": "$250+"},
    "Norway": {"low": "$90", "mid": "$200", "high": "$500+"},
    "Poland": {"low": "$35", "mid": "$75", "high": "$200+"},
    "Argentina": {"low": "$25", "mid": "$60", "high": "$180+"}
}

TIPS_DB = {
    "Japan": ["Don't tip at restaurants; it's considered rude.", "Carry a small bag for your trash; bins are rare.", "Stand on the left on escalators (except Osaka).", "Bowing is the standard way to greet."],
    "India": ["Always carry small cash notes for local markets.", "Download offline maps for rural areas.", "Respect local dress codes at religious sites.", "Remove shoes before entering homes/temples."],
    "France": ["Always say 'Bonjour' when entering a shop.", "Don't rush your meal; dining is an experience here.", "Validate your ticket before boarding trains.", "Tipping is appreciated but not mandatory."],
    "Thailand": ["Never touch someone's head; it's considered sacred.", "Point with your chin or whole hand, not your finger.", "Dress modestly for temples (cover shoulders/knees)."],
    "USA": ["Tipping 18-22% is standard in restaurants.", "Taxes are rarely included in the displayed price.", "Portion sizes are usually very large."],
    "Singapore": ["Chewing gum is technically prohibited.", "Strict fines for littering and smoking in public.", "Use the MRT; it's one of the best in the world."],
    "Switzerland": ["Water from public fountains is safe and delicious.", "Punctuality is extremely important for transport.", "Sunday is a day of rest; most shops are closed."],
    "Norway": ["Tap water is among the cleanest in the world; don't buy plastic bottles.", "Alcohol is very expensive and sold only in Vinmonopolet shops.", "Tipping is not required but rounding up is nice."],
    "Argentina": ["Be prepared for late dinners; restaurants often don't open until 8 PM.", "Blue Dollar refers to the unofficial exchange rate; research it.", "Always keep a small amount of cash for tips (propina)."]
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
    
    # Prioritize places that match interests
    relevant_places = []
    other_places = []
    
    interests_keywords = interests.lower().split() if interests else []
    
    for p in places:
        if any(kw in p.lower() for kw in interests_keywords):
            relevant_places.append(p)
        else:
            other_places.append(p)
            
    # Combine lists, putting relevant ones first
    sorted_places = relevant_places + other_places
    place_idx = 0

    for i in range(days):
        day_num = i + 1
        activities = []
        
        if day_num == 1:
            # Day 1: Arrival & First Landmark
            activities.append(f"Arrive in {dest} and check into your accommodation.")
            if sorted_places:
                activities.append(f"Kick off your trip with a visit to the iconic {sorted_places[place_idx]}.")
                place_idx = (place_idx + 1) % len(sorted_places)
            else:
                activities.append(f"Take a relaxing walk through the central district to soak in the atmosphere.")
            activities.append(f"Welcome dinner: Try {signature_food} at a highly rated local tavern.")
            
        elif day_num == days:
            # Last Day: Shopping & Farewell
            activities.append("Enjoy a slow morning with a local breakfast and coffee.")
            activities.append(f"Last-minute souvenir shopping in the artisanal markets of {dest}.")
            activities.append(f"Farewell dinner: A grand multi-course meal featuring regional specialties.")
            
        else:
            # Middle Days: Deep Dive
            if sorted_places:
                activities.append(f"Morning exploration of {sorted_places[place_idx]}.")
                place_idx = (place_idx + 1) % len(sorted_places)
                activities.append(f"Afternoon visit to {sorted_places[place_idx]}.")
                place_idx = (place_idx + 1) % len(sorted_places)
            else:
                activities.append("Explore hidden gems and local neighborhoods off the beaten path.")
                activities.append("Visit a local museum or cultural gallery.")
            
            if interests:
                activities.append(f"Special interest activity: Focused on {interests}.")
            else:
                activities.append("Evening at leisure to discover the local nightlife or night markets.")

        days_list.append({
            "day": day_num,
            "title": f"Explore {dest} - Day {day_num}",
            "activities": activities
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
        "food": f"Ask the locals in {country} for their top recommended regional dishes.",
        "culture": f"Embrace the local {country} traditions and etiquette.",
        "safety": f"Maintain standard travel awareness while exploring {dest}.",
        "language": f"National language of {country}.",
        "currency": f"Local {country} currency.",
        "mult": 1.0
    })

    food_list = culture_info["food"].split(',')
    signature_food = food_list[0].strip() if food_list else "local delicacies"
    
    # Realistic Pricing Logic
    # We use SPEND_DB as a base if available, otherwise fallback to multiplier
    spend_data = SPEND_DB.get(country, {"low": "$40", "mid": "$100", "high": "$300+"})
    
    def parse_cost(cost_str):
        return int(cost_str.replace('$', '').replace('+', '').replace(',', '').strip())

    base_daily_low = parse_cost(spend_data["low"])
    base_daily_mid = parse_cost(spend_data["mid"])
    base_daily_high = parse_cost(spend_data["high"])

    # Calculate base costs (Accommodation + Food + Transit per day)
    low_cost = int(days * base_daily_low)
    mid_cost = int(days * base_daily_mid)
    high_cost = int(days * base_daily_high)

    # Add Flight Costs (Estimated)
    flight_cost = 0
    if flight_option != "none":
        flight_cost = 400 if culture_info["mult"] < 1.0 else 800
        if flight_option == "biz": flight_cost *= 4
        elif flight_option == "econ": flight_cost *= 0.8

    packages = [
        {
            "id": "budget",
            "name": "Essential Package",
            "description": "Authentic experience focused on local life and value.",
            "estimatedCost": f"${low_cost + int(flight_cost * 0.7)}",
            "hotel": "Boutique Hostels or Eco-Lodges",
            "flights": "Economy Class (Best Value)",
            "transportation": "Public Transit & Walking Maps",
            "itinerary": generate_itinerary(dest, days, interests, places, signature_food)
        },
        {
            "id": "medium",
            "name": "Signature Collection",
            "description": "The perfect balance of comfort, style, and exploration.",
            "estimatedCost": f"${mid_cost + flight_cost}",
            "hotel": "4-Star Character Hotels",
            "flights": "Premium Economy / Direct",
            "transportation": "Private Transfers & Ride-hailing",
            "itinerary": generate_itinerary(dest, days, interests, places, signature_food)
        },
        {
            "id": "high",
            "name": "Royal Prestige",
            "description": "Ultra-luxury experience with curated VIP access.",
            "estimatedCost": f"${high_cost + int(flight_cost * 3)}",
            "hotel": "5-Star Luxury Resorts",
            "flights": "Business / First Class",
            "transportation": "Chauffeur Driven Private Car",
            "itinerary": generate_itinerary(dest, days, interests, places, signature_food)
        }
    ]
    
    for pkg in packages:
        if hotel_choice:
            pkg["hotel"] = f"{hotel_choice} (Preferred)"
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

    # Fetch new travel intel
    intel = {
        "bestTime": BEST_TIME_DB.get(country, {"months": "Anytime", "advice": "Consult local weather forecasts for the best experience."}),
        "timezone": TIMEZONE_DB.get(country, "UTC"),
        "scams": SCAM_DB.get(country, [{"title": "General Awareness", "desc": "Stay alert in crowded tourist areas and use official transport."}]),
        "apps": APPS_DB.get(country, [{"name": "Google Maps", "usage": "Navigation"}, {"name": "Google Translate", "usage": "Translation"}]),
        "emergency": EMERGENCY_DB.get(country, {"all": "112"}),
        "utilities": UTILITIES_DB.get(country, {"power": "Universal Adapter recommended", "water": "Drink bottled water", "sim": "Pick up at airport"}),
        "spend": SPEND_DB.get(country, {"low": "$30", "mid": "$70", "high": "$200+"}),
        "tips": TIPS_DB.get(country, ["Always respect local traditions.", "Learn basic greetings in the local language.", "Keep a digital copy of your documents."])
    }

    return jsonify({
        "destination": dest,
        "days": days,
        "lat": lat,
        "lon": lon,
        "packages": packages,
        "mustVisits": must_visits,
        "localGuide": local_guide,
        "intel": intel
    })

@app.route('/api/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    body = request.json or {}
    message = body.get('message', '').lower().strip()
    ctx = body.get('context', {})

    dest = ctx.get('destination', 'your destination')
    food = ctx.get('food', '')
    culture = ctx.get('culture', '')
    safety = ctx.get('safety', '')
    currency = ctx.get('currency', '')
    days = ctx.get('days', '')

    # Rule-based intent matching
    def contains(*keywords):
        return any(k in message for k in keywords)

    if contains('hello', 'hi', 'hey', 'greet'):
        reply = f"Hello! I'm your AI companion for your {dest} trip. Ask me about food, culture, safety, currency, packing, or anything else about your journey!"

    elif contains('food', 'eat', 'restaurant', 'cuisine', 'dish', 'drink', 'vegetarian', 'vegan', 'halal'):
        if food:
            reply = f"In {dest}, the must-try dishes are: {food} If you're looking for vegetarian or vegan options, search for local plant-based eateries — most destinations have excellent options near tourist areas."
        else:
            reply = f"I'd recommend exploring the local street food scene in {dest}. Markets and local eateries are always the best bet for authentic flavours."

    elif contains('culture', 'custom', 'etiquette', 'tradition', 'behavior', 'behave', 'tip', 'tipping'):
        if culture:
            reply = f"Cultural notes for {dest}: {culture}"
        else:
            reply = f"Always research local customs before visiting {dest}. Showing respect for traditions goes a long way with locals."

    elif contains('safe', 'safety', 'crime', 'dangerous', 'danger', 'scam', 'pickpocket'):
        if safety:
            reply = f"Safety tips for {dest}: {safety}"
        else:
            reply = f"As with any destination, maintain standard urban awareness in {dest}. Keep valuables close and stay in well-lit areas at night."

    elif contains('currency', 'money', 'cash', 'exchange', 'pay', 'cost', 'price', 'budget', 'cheap', 'expensive'):
        if currency:
            reply = f"The local currency in {dest} is: {currency}. I recommend carrying some local cash for markets and smaller establishments, though cards are widely accepted in most tourist areas."
        else:
            reply = f"Check the current exchange rate before you travel to {dest}. It's always good to have some local cash on hand."

    elif contains('pack', 'packing', 'luggage', 'bring', 'carry', 'clothes', 'clothing', 'wear'):
        reply = (f"For {dest}, here's a smart packing checklist:\n"
                 f"• Passport & travel documents\n"
                 f"• Universal power adapter\n"
                 f"• Comfortable walking shoes\n"
                 f"• Power bank & chargers\n"
                 f"• Any prescription medication\n"
                 f"• Weather-appropriate clothing (check the weather widget for current conditions)\n"
                 f"• A small daypack for excursions")

    elif contains('day', 'itinerary', 'plan', 'schedule', 'activity', 'activities', 'tour', 'visit'):
        reply = (f"Your {days}-day itinerary for {dest} is already planned in the Itinerary tab. "
                 f"I'd suggest starting each morning early to beat the crowds at popular sites. "
                 f"Afternoons are great for local markets, and evenings for dining out. "
                 f"Would you like tips on a specific type of activity — adventure, history, food, or nightlife?")

    elif contains('weather', 'temperature', 'rain', 'hot', 'cold', 'climate', 'season'):
        reply = (f"Check the live weather widget at the top of your dashboard for real-time conditions in {dest}. "
                 f"As a general tip, always pack a light layer regardless of the season — temperatures can surprise you!")

    elif contains('hotel', 'accommodation', 'stay', 'hostel', 'airbnb', 'resort'):
        reply = (f"Your selected package includes accommodation recommendations for {dest}. "
                 f"For the best experience, look for hotels in the city centre or near major transit hubs. "
                 f"Booking in advance (especially for peak season) can save you up to 30%.")

    elif contains('transport', 'taxi', 'uber', 'metro', 'bus', 'train', 'flight', 'airport', 'transit'):
        reply = (f"For getting around {dest}, I recommend using official taxis or rideshare apps (Uber/Grab where available). "
                 f"Public metro and bus networks are usually the most affordable option. "
                 f"Always agree on a price before getting into an unmarked cab.")

    elif contains('visa', 'passport', 'entry', 'immigration', 'requirement'):
        reply = (f"Visa requirements for {dest} vary by nationality. I strongly recommend checking the official embassy website "
                 f"of {dest} for your country's entry requirements at least 6-8 weeks before your trip.")

    elif contains('language', 'speak', 'phrase', 'word', 'translate', 'english'):
        reply = (f"Language tip for {dest}: English is spoken in most tourist areas. "
                 f"Learning a few basic local phrases (hello, thank you, excuse me, how much?) goes a long way. "
                 f"Google Translate with offline download is your best travel companion.")

    elif contains('emergency', 'hospital', 'doctor', 'police', 'help', 'ambulance'):
        reply = (f"In case of emergency in {dest}, always save the local emergency number (usually 112 or 911) and the contact "
                 f"for your country's embassy. Travel insurance with medical coverage is highly recommended for all international trips.")

    elif contains('thank', 'thanks', 'great', 'awesome', 'perfect', 'good', 'helpful'):
        reply = f"You're welcome! Enjoy your trip to {dest}. Feel free to ask anything else before you go!"

    else:
        reply = (f"That's a great question about {dest}! For the most accurate and up-to-date information, "
                 f"I recommend checking travel resources like Lonely Planet, TripAdvisor, or the official tourism board "
                 f"for {dest}. Is there anything specific about food, culture, safety, or packing I can help you with?")

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
