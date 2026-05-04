from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

CULTURE_DB = {
    # North America
    "United States": {"food": "Regional BBQ (Texas/Carolina), Clam Chowder (New England), and Artisanal Burgers", "culture": "Tipping (18-25%) is a non-negotiable social contract. Be prepared for large portions and enthusiastic service.", "safety": "Generally safe, but research specific urban neighborhoods. Use ride-hails late at night in big cities.", "mult": 1.8, "language": "English", "currency": "US Dollar ($)", "curr_code": "USD"},
    "Canada": {"food": "Quebecois Poutine, Nanaimo Bars, and fresh Pacific Salmon", "culture": "Punctuality and politeness are highly valued. Tipping 15-20% is the standard in service industries.", "safety": "Very safe. Nature is the biggest risk; check weather for blizzards or wildlife in parks.", "mult": 1.5, "language": "English & French", "currency": "Canadian Dollar (CAD)", "curr_code": "CAD"},
    "Mexico": {"food": "Al Pastor Tacos, Oaxacan Mole, and fresh Aguachile", "culture": "Family-centric and vibrant. 'Mañana' reflects a relaxed pace—don't expect strict timing in social settings.", "safety": "Stick to toll roads (cuotas) and tourist zones. Only use authorized 'Sitio' taxis.", "mult": 0.7, "language": "Spanish • Hello: Hola • Thanks: Gracias", "currency": "Mexican Peso ($)", "curr_code": "MXN"},
    
    # Europe
    "Italy": {"food": "Authentic Carbonara (no cream!), Neapolitan Pizza, and Artisanal Gelato", "culture": "Cappuccino is strictly for mornings. Dinner is a slow, multi-course affair starting after 8 PM.", "safety": "High pickpocket risk in Rome/Venice; keep valuables in a front pocket or cross-body bag.", "mult": 1.5, "language": "Italian • Hello: Buongiorno • Thanks: Grazie", "currency": "Euro (€)", "curr_code": "EUR"},
    "France": {"food": "Buttery Croissants, Coq au Vin, and regional cheeses (Brie, Roquefort)", "culture": "The 'Bonjour' rule: Always greet staff when entering a shop or you'll be seen as rude. Dress is 'effortless chic'.", "safety": "Watch for the 'string' or 'petition' scams near major Parisian landmarks.", "mult": 1.6, "language": "French • Hello: Bonjour • Thanks: Merci", "currency": "Euro (€)", "curr_code": "EUR"},
    "United Kingdom": {"food": "Proper Fish & Chips, Sunday Roast with Yorkshire Pudding, and Afternoon Tea", "culture": "Queuing is sacred. 'Sorry' is used for everything. In pubs, order at the bar; there is no table service.", "safety": "Safe, but remember to 'Look Right'—traffic flows on the left. Watch for rowdy crowds after matches.", "mult": 1.7, "language": "English", "currency": "British Pound (£)", "curr_code": "GBP"},
    "Spain": {"food": "Iberian Ham, Seafood Paella, and various regional Tapas", "culture": "The 'Siesta' is real—many shops close from 2-5 PM. Life happens late; lunch at 2 PM, dinner at 10 PM.", "safety": "Major pickpocket hotspots in Barcelona (Las Ramblas). Use hotel safes for passports.", "mult": 1.3, "language": "Spanish • Hello: Hola • Thanks: Gracias", "currency": "Euro (€)", "curr_code": "EUR"},
    "Germany": {"food": "Currywurst, Soft Pretzels, and various regional Schnitzels", "culture": "Direct communication is valued. Always make eye contact during a toast ('Prost') or it's '7 years of bad luck'.", "safety": "Very safe. Follow 'The Rules'—don't jaywalk, even if no cars are coming.", "mult": 1.4, "language": "German • Hello: Hallo • Thanks: Danke", "currency": "Euro (€)", "curr_code": "EUR"},
    "Greece": {"food": "Moussaka, Grilled Octopus, and authentic Feta-topped Greek Salads", "culture": "Hospitality ('Philoxenia') is deep-rooted. Expect a relaxed 'Island Time' pace. Don't flush toilet paper.", "safety": "Very safe, though driving can be chaotic. Be cautious on moped rentals.", "mult": 1.1, "language": "Greek • Hello: Yassou • Thanks: Efharisto", "currency": "Euro (€)", "curr_code": "EUR"},
    "Portugal": {"food": "Bacalhau, Pastel de Nata, and fresh Sardines", "culture": "Laid back and friendly. 'Saudade' (melancholy) is a key cultural concept. Dinner is generally after 8 PM.", "safety": "Extremely safe country. Be cautious of 'helpful' strangers in nightlife districts.", "mult": 0.9, "language": "Portuguese • Hello: Olá • Thanks: Obrigado", "currency": "Euro (€)", "curr_code": "EUR"},
    "Switzerland": {"food": "Cheese Fondue, Crispy Rösti, and premium Swiss Chocolate", "culture": "Quiet hours are strictly enforced (especially Sundays). Efficiency is the national pride.", "safety": "Statistically one of the safest places on earth. Nature (hiking/skiing) is the only real hazard.", "mult": 2.2, "language": "German/French/Italian • Hello: Grüezi", "currency": "Swiss Franc (CHF)", "curr_code": "CHF"},
    "Netherlands": {"food": "Stroopwafels, Bitterballen, and Raw Herring", "culture": "Radical honesty and directness. Cycling is the primary mode of transport—never walk in the bike lanes.", "safety": "Very safe. Watch for professional pickpockets on trains and in the Red Light District.", "mult": 1.4, "language": "Dutch • Hello: Hallo • Thanks: Dank je", "currency": "Euro (€)", "curr_code": "EUR"},
    "Ireland": {"food": "Irish Stew, Fresh Oysters, and Soda Bread", "culture": "Pubs are the social hub. 'The Craic' (fun/chat) is essential. Avoid talking about sensitive political history.", "safety": "Very safe. The weather is the biggest unpredictability—always carry a rain shell.", "mult": 1.4, "language": "English & Irish", "currency": "Euro (€)", "curr_code": "EUR"},
    
    # Asia
    "Japan": {"food": "Sushi Omakase, Rich Tonkotsu Ramen, and Wagyu Beef", "culture": "A culture of silence and respect. No eating while walking. Tipping is offensive; service is included.", "safety": "Extraordinarily safe. You can leave your bag to save a seat, but always remain polite.", "mult": 1.8, "language": "Japanese • Hello: Konnichiwa • Thanks: Arigatou", "currency": "Japanese Yen (¥)", "curr_code": "JPY"},
    "Thailand": {"food": "Spicy Som Tum, Pad Thai, and Mango Sticky Rice", "culture": "The 'Land of Smiles'. Never point your feet at people or touch anyone's head. Dress modestly for temples.", "safety": "Avoid 'Gem' or 'Closed Palace' scams. Drink only bottled or filtered water.", "mult": 0.6, "language": "Thai • Hello: Sawasdee • Thanks: Khop Khun", "currency": "Thai Baht (฿)", "curr_code": "THB"},
    "India": {"food": "Butter Chicken, regional Thalis, and street-style Chaat", "culture": "Use only your right hand for eating and transactions. Remove shoes before entering any home or temple.", "safety": "Only drink 'sealed' bottled water. Negotiate all rickshaw fares before the journey starts.", "mult": 0.5, "language": "Hindi / English • Hello: Namaste", "currency": "Indian Rupee (₹)", "curr_code": "INR"},
    "China": {"food": "Peking Duck, Dim Sum, and Sichuan Hot Pot", "culture": "Personal space is smaller than in the West. Bargaining is expected in markets. Use apps for everything.", "safety": "Very low street crime. Be aware of the 'Tea Ceremony' scam in tourist areas.", "mult": 1.0, "language": "Mandarin • Hello: Nǐ hǎo • Thanks: Xièxiè", "currency": "Chinese Yuan (CNY)", "curr_code": "CNY"},
    "South Korea": {"food": "Korean BBQ, Spicy Kimchi Stew, and Fried Chicken", "culture": "Respect for elders is paramount. Use two hands when giving or receiving anything. Silence on subways.", "safety": "Extremely safe. Great public Wi-Fi everywhere. Keep your ID/Passport on you as required.", "mult": 1.3, "language": "Korean • Hello: Annyeonghaseyo", "currency": "South Korean Won (KRW)", "curr_code": "KRW"},
    "Vietnam": {"food": "Pho, Banh Mi, and Fresh Spring Rolls", "culture": "Respect for family and history. Remove shoes in homes. Be patient—things move at their own pace here.", "safety": "Traffic is chaotic; walk slowly and steadily across the street. Don't carry bags loosely on bikes.", "mult": 0.4, "language": "Vietnamese • Hello: Xin chào", "currency": "Vietnamese Dong (VND)", "curr_code": "VND"},
    "Indonesia": {"food": "Nasi Goreng, Satay, and Beef Rendang", "culture": "Diverse and religious. Dress modestly in rural areas. Use your right hand for greetings.", "safety": "Traffic is very dense. Watch for volcano/seismic activity updates in certain regions.", "mult": 0.5, "language": "Indonesian • Hello: Halo • Thanks: Terima kasih", "currency": "Indonesian Rupiah (IDR)", "curr_code": "IDR"},
    
    # Middle East & Africa
    "Turkey": {"food": "Iskender Kebab, Baklava with Pistachios, and Turkish Meze", "culture": "Bargaining in the Grand Bazaar is expected. Always accept tea—it's a sign of hospitality, not a sales pitch.", "safety": "Use only official yellow taxis with meters. Be wary of the 'brushed dropped' or 'overpriced bar' scams.", "mult": 0.8, "language": "Turkish • Hello: Merhaba • Thanks: Teşekkürler", "currency": "Turkish Lira (₺)", "curr_code": "TRY"},
    "United Arab Emirates": {"food": "Al Machboos, Luqaimat (sweet dumplings), and Camel Sliders", "culture": "A blend of ultra-modern and deeply traditional. Dress modestly in malls and public spaces. Public displays of affection are discouraged.", "safety": "One of the safest countries globally. Strict laws mean crime is very low, but follow all local regulations closely.", "mult": 1.6, "language": "Arabic & English • Hello: Marhaba", "currency": "UAE Dirham (AED)", "curr_code": "AED"},
    "Egypt": {"food": "Koshari, Ful Medames, and Grilled Squab", "culture": "Bargaining is a way of life. Tipping ('Baksheesh') is expected for even small services. Dress conservatively.", "safety": "Always stay hydrated. Cross the chaotic Cairo streets by walking at a steady, predictable pace.", "mult": 0.6, "language": "Arabic • Hello: Marhaba • Thanks: Shukran", "currency": "Egyptian Pound (E£)", "curr_code": "EGP"},
    "Morocco": {"food": "Slow-cooked Tagine, Fluffy Couscous, and Mint Tea", "culture": "The 'Right Hand' rule is essential for eating and greetings. If offered tea, it is polite to drink at least one cup.", "safety": "Expect persistent 'guides' in the Medinas. A firm 'No, thank you' and continued walking is the best approach.", "mult": 0.6, "language": "Arabic & French • Hello: Salam", "currency": "Moroccan Dirham (MAD)", "curr_code": "MAD"},
    "South Africa": {"food": "Braai (BBQ) feast, Biltong (dried meat), and Malva Pudding", "culture": "Casual, outdoor-focused, and friendly. Tipping 10-15% is the local standard. Respect the complex history.", "safety": "Stay in well-lit, populated areas. Use Uber rather than walking at night. Keep valuables out of sight in cars.", "mult": 0.8, "language": "English, Zulu, Xhosa...", "currency": "South African Rand (ZAR)", "curr_code": "ZAR"},
    "Kenya": {"food": "Nyama Choma (Roasted goat), Ugali, and Sukuma Wiki", "culture": "Very warm and communal. 'Harambee' (pulling together) is a core philosophy. Respect wildlife and local tribes.", "safety": "Stick to guided safaris. In Nairobi, be vigilant of your belongings in crowded markets.", "mult": 0.7, "language": "Swahili & English • Hello: Jambo", "currency": "Kenyan Shilling (KSh)", "curr_code": "KES"},
    
    # South America & Oceania
    "Brazil": {"food": "Feijoada (bean stew), Pão de Queijo, and Acai bowls", "culture": "Expressive and warm. Physical contact (hugs/kisses) is common in greetings. Thumbs up is used for almost everything.", "safety": "Leave expensive jewelry at home. Keep your phone in your pocket while walking in busy city centers.", "mult": 0.9, "language": "Portuguese • Hello: Olá • Thanks: Obrigado", "currency": "Brazilian Real (R$)", "curr_code": "BRL"},
    "Argentina": {"food": "Prime Grass-fed Asado, Empanadas, and Dulce de Leche", "culture": "Passionate about football, politics, and tango. Dinner is extremely late—restaurants are empty before 9 PM.", "safety": "Watch for 'the mustard scam' in Buenos Aires. Carry some cash as smaller shops may not take cards.", "mult": 0.7, "language": "Spanish • Hello: Hola", "currency": "Argentine Peso ($)", "curr_code": "ARS"},
    "Peru": {"food": "Classic Ceviche, Lomo Saltado, and Roasted Cuy", "culture": "Deeply proud of Incan heritage. Respect the 'Pachamama' (Mother Earth). Altitude sickness is a real factor in the Andes.", "safety": "Use only 'App-based' or 'Hotel-called' taxis. Drink only bottled water, even in high-end hotels.", "mult": 0.6, "language": "Spanish • Hello: Hola", "currency": "Peruvian Sol (S/.)", "curr_code": "PEN"},
    "Colombia": {"food": "Bandeja Paisa, Arepas, and world-class Coffee", "culture": "Resilient, musical, and incredibly hospitable. Don't mention the 'Pablo' era—locals find it offensive and outdated.", "safety": "Major improvements in safety, but stick to established tourist hubs. Avoid 'giving papaya' (showing off wealth).", "mult": 0.7, "language": "Spanish • Hello: Hola", "currency": "Colombian Peso ($)", "curr_code": "COP"},
    "Australia": {"food": "Meat Pies, Barramundi, and Smashed Avocado on Toast", "culture": "Loud, friendly, and informal. 'No worries' is the national motto. Strong coffee culture is a way of life.", "safety": "The sun is lethal; wear SPF 50+. Only swim between the red and yellow flags at beaches.", "mult": 1.6, "language": "English", "currency": "Australian Dollar (AUD)", "curr_code": "AUD"},
    "New Zealand": {"food": "Hangi (earth oven) feast, Lamb, and Hokey Pokey Ice Cream", "culture": "High respect for Māori traditions. Extremely eco-conscious; follow 'Leave No Trace' principles strictly.", "safety": "Very safe. The weather is the biggest danger in the outdoors; check mountain forecasts religiously.", "mult": 1.5, "language": "English & Māori", "currency": "New Zealand Dollar (NZD)", "curr_code": "NZD"},
    
    # Additional Europe & Asia
    "Singapore": {"food": "Hainanese Chicken Rice, Chili Crab, and Laksa", "culture": "A hyper-efficient 'Fine City'. Rules are followed strictly. Tipping is not expected as a 10% service charge is added.", "safety": "One of the safest places on earth. You can leave your phone on a table to 'chope' (reserve) it without worry.", "mult": 1.6, "language": "English, Mandarin, Malay, Tamil", "currency": "Singapore Dollar (SGD)", "curr_code": "SGD"},
    "Norway": {"food": "Smoked Salmon, Brown Cheese (Brunost), and Reindeer", "culture": "Equality and the outdoors are sacred. 'Allemannsretten' gives you the right to roam anywhere in nature.", "safety": "Extraordinarily safe. Be careful on slippery rocks near fjords and always dress for 'four seasons in one day'.", "mult": 2.1, "language": "Norwegian • Hello: Hallo", "currency": "Norwegian Krone (NOK)", "curr_code": "NOK"},
    "Sweden": {"food": "Swedish Meatballs, Gravlax, and Cinnamon Buns (Kanelbulle)", "culture": "The concept of 'Lagom' (not too much, not too little) permeates life. 'Fika' (coffee and cake break) is mandatory.", "safety": "Very safe. Be polite, don't be loud in public, and always recycle correctly.", "mult": 1.7, "language": "Swedish • Hello: Hej", "currency": "Swedish Krona (SEK)", "curr_code": "SEK"},
    "Denmark": {"food": "Smørrebrød (Open sandwiches), pastries, and organic produce", "culture": "Focused on 'Hygge' (coziness). Cycling is the primary transport—follow bike traffic lights as strictly as car lights.", "safety": "Extremely safe. Use common sense in Christiania and avoid walking in bike lanes.", "mult": 1.8, "language": "Danish • Hello: Hej", "currency": "Danish Krone (DKK)", "curr_code": "DKK"},
    "Poland": {"food": "Pierogi (Dumplings), Żurek soup, and Kielbasa", "culture": "Incredibly hospitable. If invited to a home, bring flowers (odd numbers only) and remove your shoes.", "safety": "Very safe. Use apps like Bolt/Uber for taxis and be careful crossing roads without lights.", "mult": 0.8, "language": "Polish • Hello: Cześć", "currency": "Polish Złoty (PLN)", "curr_code": "PLN"},
    "Czech Republic": {"food": "Svíčková (Beef in cream), Trdelník, and Pilsner Beer", "culture": "Quiet and reserved in public, but warm once you know them. Beer is often cheaper than water and is a cultural staple.", "safety": "Safe, but watch out for currency exchange '0% commission' traps in Prague.", "mult": 0.9, "language": "Czech • Hello: Ahoj", "currency": "Czech Koruna (CZK)", "curr_code": "CZK"},
    "Hungary": {"food": "Spicy Goulash, Chicken Paprikash, and Lángos", "culture": "Deep appreciation for classical music and thermal bath culture. Don't clink beer glasses (historical superstition).", "safety": "Safe. Check restaurant menus for 'service fees' and use official taxi apps like Bolt.", "mult": 0.7, "language": "Hungarian • Hello: Szia", "currency": "Hungarian Forint (HUF)", "curr_code": "HUF"},
    "Austria": {"food": "Wiener Schnitzel, Sachertorte, and Apple Strudel", "culture": "Formal and polite. Punctuality is expected. Sunday is a total day of rest—almost everything is closed.", "safety": "One of the safest countries. Take alpine safety seriously if hiking or skiing.", "mult": 1.5, "language": "German • Hello: Servus", "currency": "Euro (€)", "curr_code": "EUR"},
    "Taiwan": {"food": "Beef Noodle Soup, Din Tai Fung Dumplings, and Bubble Tea", "culture": "Unbelievably polite. Night markets are the social heart. Always stand on the right of the escalator.", "safety": "Safe at any hour. Great emergency services and very helpful locals if you look lost.", "mult": 1.2, "language": "Mandarin • Hello: Nǐ hǎo", "currency": "New Taiwan Dollar (TWD)", "curr_code": "TWD"},
    "Saudi Arabia": {"food": "Kabsa (Spiced rice & meat), Dates, and Arabic Coffee", "culture": "Deeply hospitable but conservative. Follow dress codes (shoulders/knees covered). Respect prayer times.", "safety": "Very safe. Observe local laws and customs strictly to avoid fines or legal issues.", "mult": 1.5, "language": "Arabic • Hello: Marhaba", "currency": "Saudi Riyal (SAR)", "curr_code": "SAR"}
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
    "Japan": [{"title": "Overpriced Bars", "desc": "Touts in Kabukicho may lure you with 'cheap' drinks but hit you with massive hidden cover charges."}, {"title": "The Fake Monk", "desc": "People dressed as monks hand you a 'gold' card/bracelet, then aggressively demand a donation."}],
    "France": [{"title": "The Friendship Bracelet", "desc": "Touts in Montmartre try to tie a string around your finger, then demand €20 once you're 'stuck'."}, {"title": "The Petition Scam", "desc": "Groups of teenagers ask you to sign a petition for a fake charity while a partner picks your pocket."}],
    "Italy": [{"title": "Rose Sellers", "desc": "A vendor hands a rose to your partner as a 'gift', then demands payment from you once accepted."}, {"title": "Self-Appointed Porters", "desc": "Touts at train stations grab your bags to 'help' and then refuse to leave without a high tip."}],
    "Thailand": [{"title": "Grand Palace is Closed", "desc": "Tuk-tuk drivers claim the Palace is closed for a royal event to redirect you to overpriced jewelry shops."}, {"title": "The Jet Ski Scam", "desc": "Operators claim you damaged a jet ski (using old scratches) and demand thousands in 'repairs'."}],
    "India": [{"title": "The Fake Tourist Office", "desc": "Drivers claim your hotel is 'burned down' or 'full' and take you to a fake agency to rebook at 10x the price."}, {"title": "The Gem Scam", "desc": "Strangers offer a 'tax-free' gem export deal that is actually a high-priced fraud."}],
    "Turkey": [{"title": "The Shoe Brusher", "desc": "A brusher drops their brush; when you pick it up, they 'thank' you with a brush and charge an exorbitant fee."}, {"title": "The Tea/Beer Invite", "desc": "A friendly local invites you for a drink, then leaves you with a bill for hundreds of dollars."}],
    "Spain": [{"title": "Bird Dropping Scam", "desc": "Someone sprays a white liquid on you, offers to 'help' clean it, and pickpockets you during the distraction."}, {"title": "The Trileros (Shell Game)", "desc": "Fake street games designed to distract you while accomplices work your pockets."}],
    "Vietnam": [{"title": "The Coconut Yoke", "desc": "A vendor puts their coconut yoke on your shoulder for a 'free' photo, then demands payment and overcharges for fruit."}, {"title": "The Shoe Repair", "desc": "Someone starts 'fixing' your shoe while you're sitting, then demands a huge fee for the unrequested work."}],
    "USA": [{"title": "The CD Handout", "desc": "In Times Square/Hollywood, people hand you a 'free' CD, then aggressively demand a 'donation' once you touch it."}, {"title": "The Broken Glasses", "desc": "Someone bumps into you, drops broken glasses, and blames you for the 'accident' to get cash."}],
    "Egypt": [{"title": "The Free Camel Ride", "desc": "Getting on the camel is 'free', but they won't let the camel sit down to let you off until you pay a high price."}, {"title": "The Hidden Museum Ticket", "desc": "Touts claim you need a 'special' ticket to enter certain areas that are actually included."}],
    "Brazil": [{"title": "The Good Samaritan", "desc": "Someone points out a 'stain' or 'dirt' on your clothes, offers to help, and robs you during the process."}],
    "Morocco": [{"title": "The Henna Grab", "desc": "Women in squares grab your hand and start a henna tattoo, then demand €30 for the 'completed' work."}, {"title": "The Closed Path", "desc": "Youths claim a street is 'closed' or 'blocked' to lead you into a dead end where they demand money to guide you out."}],
    "Czech Republic": [{"title": "The 0% Commission Trap", "desc": "Exchange booths offer 0% commission but use a hidden, terrible exchange rate found in the fine print."}, {"title": "The Fake Police", "desc": "People in fake uniforms ask to check your wallet for 'counterfeit' bills, then swap them for fakes."}],
}

APPS_DB = {
    "Japan": [{"name": "Google Maps", "usage": "Best for train exits and platform info."}, {"name": "Google Translate", "usage": "Essential for camera-translating menus."}, {"name": "Suica/Pasmo", "usage": "Digital transit cards."}],
    "Thailand": [{"name": "Grab", "usage": "Safety and fair pricing for taxis and bikes."}, {"name": "Google Translate", "usage": "Helpful for rural areas."}, {"name": "Klook", "usage": "Best for booking island tours."}],
    "India": [{"name": "Uber/Ola", "usage": "Reliable ride-hailing with fixed prices."}, {"name": "Zomato/Swiggy", "usage": "Best for food delivery and ratings."}, {"name": "MakeMyTrip", "usage": "Leading app for Indian domestic travel."}],
    "France": [{"name": "Citymapper", "usage": "The gold standard for Paris Metro navigation."}, {"name": "TheFork", "usage": "Essential for restaurant reservations and discounts."}, {"name": "Bonjour RATP", "usage": "Official Paris transit app."}],
    "USA": [{"name": "Uber/Lyft", "usage": "Primary ride-sharing apps."}, {"name": "Yelp", "usage": "Most reliable for real food and service reviews."}, {"name": "AllTrails", "usage": "Best for hiking in National Parks."}],
    "Singapore": [{"name": "Grab", "usage": "Unified app for rides, food, and delivery."}, {"name": "Citymapper", "usage": "Best for MRT and bus timing."}, {"name": "Chope", "usage": "Top restaurant booking platform."}],
    "South Korea": [{"name": "Naver Maps", "usage": "Far more accurate than Google Maps in Korea."}, {"name": "KakaoTaxi", "usage": "Best for calling official taxis."}, {"name": "Papago", "usage": "The best translator for Korean language."}],
    "Germany": [{"name": "DB Navigator", "usage": "Mandatory for train schedules and mobile tickets."}, {"name": "FreeNow", "usage": "Main taxi and e-scooter app."}, {"name": "Komoot", "usage": "Best for cycling and hiking routes."}],
    "Vietnam": [{"name": "Grab", "usage": "Indispensable for safe transport and food."}, {"name": "Zalo", "usage": "Local messaging app used for all business bookings."}],
    "Norway": [{"name": "Vy", "usage": "Booking trains and long-distance buses."}, {"name": "Ruter", "usage": "Essential for Oslo metro and ferry tickets."}, {"name": "UT.no", "usage": "Best for finding hiking trails."}],
    "Argentina": [{"name": "Cabify", "usage": "The safest and most reliable way to get around Buenos Aires."}, {"name": "PedidosYa", "usage": "Top app for food and grocery delivery."}],
}

EMERGENCY_DB = {
    "Japan": {"police": "110", "medical": "119", "fire": "119"},
    "France": {"police": "17", "medical": "15", "fire": "18", "all": "112"},
    "USA": {"all": "911"},
    "UK": {"all": "999", "eu": "112"},
    "Thailand": {"police": "191", "tourist_police": "1155", "medical": "1669"},
    "India": {"all": "112"},
    "Spain": {"all": "112"},
    "Germany": {"police": "110", "medical": "112", "fire": "112"},
    "Singapore": {"police": "999", "medical": "995", "fire": "995"},
    "Australia": {"all": "000"},
    "Canada": {"all": "911"},
    "Switzerland": {"police": "117", "medical": "144", "fire": "118", "all": "112"},
    "Norway": {"police": "112", "medical": "113", "fire": "110"},
    "Poland": {"all": "112"},
    "Argentina": {"police": "911", "medical": "107", "fire": "100"},
    "Kenya": {"all": "999"},
    "Turkey": {"all": "112"},
    "UAE": {"police": "999", "medical": "998", "fire": "997"}
}

UTILITIES_DB = {
    "Japan": {"power": "Type A/B, 100V, 60Hz", "water": "Tap water is safe and high quality.", "sim": "Ubigi or Airalo (eSIM) for easy data; physical SIMs are hard for tourists."},
    "UK": {"power": "Type G, 230V, 50Hz", "water": "Tap water is perfectly safe to drink.", "sim": "EE or Vodafone have the best coverage; pick up at Heathrow/Gatwick."},
    "USA": {"power": "Type A/B, 120V, 60Hz", "water": "Tap water is safe everywhere.", "sim": "T-Mobile Tourist Plan or Airalo eSIM are the easiest options."},
    "India": {"power": "Type C/D/M, 230V, 50Hz", "water": "Strictly drink bottled or filtered water; avoid ice in street drinks.", "sim": "Airtel or Jio; requires Passport/Visa and can take 2-12 hours to activate."},
    "Thailand": {"power": "Type A/B/C/O, 220V", "water": "Drink only bottled water; usually provided free in hotels.", "sim": "AIS or TrueMove Tourist SIMs are excellent and available at every airport."},
    "France": {"power": "Type C/E, 230V", "water": "Tap water is safe and free in restaurants ('une carafe d'eau').", "sim": "Orange Holiday SIM offers great data across the EU."},
    "Germany": {"power": "Type C/F, 230V", "water": "Tap water is safe and highly regulated.", "sim": "Telekom or Vodafone; requires ID registration for physical SIMs."},
    "Spain": {"power": "Type C/F, 230V", "water": "Tap water is safe, though tastes 'hard' in coastal cities.", "sim": "Movistar or Orange; available at any local shop with a passport."},
    "Singapore": {"power": "Type G, 230V", "water": "Tap water is high-quality and safe to drink.", "sim": "Singtel or StarHub; can be bought at any 7-Eleven with a passport."},
    "Switzerland": {"power": "Type J, 230V", "water": "Tap water is world-class; refill at any public fountain.", "sim": "Swisscom offers the best coverage; Salt is cheaper."},
    "Norway": {"power": "Type C/F, 230V", "water": "Tap water is among the world's purest.", "sim": "Telenor or Telia; physical SIMs require ID registration."},
    "Argentina": {"power": "Type C/I, 220V", "water": "Tap water is safe in major cities like BA, but buy bottled in rural areas.", "sim": "Claro or Personal; go to an official 'Centro de Atención' with your passport."},
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
    "Japan": ["Don't tip at restaurants; it's considered rude and might be refused.", "Carry a small bag for your trash; public bins are almost non-existent.", "Stand on the left on escalators in Tokyo, but on the right in Osaka.", "Bowing is the standard way to greet; a slight nod is usually enough for tourists.", "Silence is expected on public transport; avoid talking on your phone."],
    "India": ["Always carry small cash notes (₹10, ₹20) for local markets and tips.", "Download offline maps for rural areas as signal can be spotty.", "Respect local dress codes; cover shoulders and knees at all religious sites.", "Remove shoes before entering homes, temples, and some small shops.", "Only use your right hand for eating and passing items to others."],
    "France": ["Always say 'Bonjour' (day) or 'Bonsoir' (evening) when entering a shop or café.", "Don't rush your meal; dining is a slow social experience in France.", "Validate your train/metro ticket at the yellow machines before boarding.", "A 'service compris' is usually included, but leaving a few euros is appreciated.", "Avoid wearing loud 'tourist' clothes if you want to blend in."],
    "Thailand": ["Never touch someone's head; it's considered the most sacred part of the body.", "Point with your chin or your whole hand, never with your index finger.", "Dress modestly for temples (cover shoulders and knees); sarongs are often for rent.", "The King and Royal Family are deeply respected; never make negative comments.", "Always remove your shoes before entering a home or a temple."],
    "USA": ["Tipping 18-22% is expected for table service in restaurants.", "Sales tax is almost never included in the price tag; it's added at checkout.", "Portion sizes are usually massive; don't be afraid to ask for a 'to-go' box.", "In big cities, walking fast and looking like you know where you're going is the best safety tip.", "Prices in bars/clubs can be much higher than they appear; check for cover charges."],
    "Singapore": ["Chewing gum is technically prohibited and cannot be bought locally.", "Strict fines for littering, smoking in non-designated areas, and eating on the MRT.", "Use the MRT for everything; it is one of the cleanest and most efficient systems in the world.", "Tap your credit/debit card directly for bus and train fares.", "The word 'Chope' means reserving a seat with a packet of tissues—it's a local law!"],
    "Switzerland": ["Water from public fountains is safe and often better than bottled water.", "Punctuality is a national religion; if the train says 10:02, it leaves at 10:02.", "Sunday is a day of rest; most supermarkets and shops are strictly closed.", "Hiking trails are exceptionally well-marked; follow the yellow signs.", "COOP and Migros are the best places for high-quality, affordable 'picnic' lunches."],
    "Norway": ["Tap water is among the cleanest in the world; don't waste money on plastic bottles.", "Alcohol is very expensive and sold only in state-run 'Vinmonopolet' shops.", "Tipping is not required, but rounding up the bill is a nice gesture for good service.", "Nature is for everyone; the 'Right to Roam' means you can camp almost anywhere for one night.", "The weather changes in minutes; 'There is no such thing as bad weather, only bad clothing'."],
    "Argentina": ["Be prepared for late dinners; restaurants rarely see locals before 9:30 or 10:00 PM.", "Research the 'Blue Dollar' (informal exchange rate) to get significantly more value for your money.", "Always keep a small amount of cash for 'propina' (tips) and small café purchases.", "Football is a religion; avoid wearing the jersey of a rival team on match days.", "The 'Merienda' (tea time) at 5:00 PM is a mandatory ritual for coffee and pastries."],
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
        "curr_code": culture_info.get("curr_code", "EUR"),
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
    days = ctx.get('days', 0)

    # World-Class Concierge Persona
    prefix = f"As your Dora Concierge for {dest}, I'm here to help. "
    
    # Intent Matching Logic
    def matches(keywords):
        return any(k in message for k in keywords)

    # 1. Greetings & Persona
    if matches(['hello', 'hi', 'hey', 'who are you', 'help']):
        reply = f"Hello! I am your Dora AI Travel Concierge. I've analyzed your {days}-day plan for {dest} and I'm ready to help you with hidden gems, cultural nuances, or logistical hacks. What's on your mind?"

    # 2. Culinary / Food Deep-Dive
    elif matches(['food', 'eat', 'restaurant', 'cuisine', 'dish', 'drink', 'vegetarian', 'vegan', 'halal', 'breakfast', 'lunch', 'dinner']):
        if food:
            reply = f"For your culinary journey in {dest}, you simply cannot miss {food}. Beyond those, I suggest looking for small 'hole-in-the-wall' spots where locals congregate—that's where the soul of the cuisine lives. Would you like a specific recommendation for a budget or fine-dining experience?"
        else:
            reply = f"Exploring the local flavors is the heart of any trip to {dest}. I'd recommend starting with the central food markets early in the morning for the freshest experience. Is there a specific dietary preference you have?"

    # 3. Cultural Etiquette & Social Norms
    elif matches(['culture', 'custom', 'etiquette', 'tradition', 'behavior', 'behave', 'tip', 'tipping', 'greeting', 'respect']):
        if culture:
            reply = f"Understanding local customs is key to a smooth trip. In {dest}, remember: {culture}. A small tip from me: learning 'Hello' and 'Thank You' in the local language opens many doors that remain closed to most tourists."
        else:
            reply = f"The culture in {dest} is rich and welcoming. Generally, a polite attitude and observing how locals interact will serve you well. Would you like me to help you find some basic phrases?"

    # 4. Safety & Security (Granular)
    elif matches(['safe', 'safety', 'crime', 'dangerous', 'danger', 'scam', 'pickpocket', 'night', 'alone', 'police']):
        if safety:
            reply = f"Your safety is my priority. In {dest}, {safety} Always keep a digital copy of your passport in the cloud and avoid displaying expensive jewelry in crowded transit hubs. Do you have a specific neighborhood concern?"
        else:
            reply = f"Generally, {dest} is welcoming, but like any global hub, stay vigilant in crowded areas. Keep your belongings in a front-facing bag. I can check for specific local emergency contacts if you'd like?"

    # 5. Logistics / Money / Budget
    elif matches(['currency', 'money', 'cash', 'exchange', 'pay', 'cost', 'price', 'budget', 'cheap', 'expensive', 'atm', 'card']):
        if currency:
            reply = f"Managing your finances in {dest}: The local currency is {currency}. While major shops take cards, I recommend always having small denominations of cash for local markets or small transport. ATMs are best found inside banks for better security."
        else:
            reply = f"Budgeting for {dest} is key. I've calculated spend estimators in your Travel Intel tab. Generally, having a mix of credit cards and a small amount of local cash is the most resilient strategy."

    # 6. Packing & Gear
    elif matches(['pack', 'packing', 'luggage', 'bring', 'carry', 'clothes', 'clothing', 'wear', 'shoes', 'jacket']):
        reply = (f"For {dest}, my 'Pro-Traveler' checklist includes: "
                 f"1. A high-quality universal power adapter. 2. Broken-in walking shoes (trust me on this). "
                 f"3. A reusable water bottle with a filter. 4. Layers—even in warm climates, AC can be freezing! "
                 f"Since you're staying for {days} days, I recommend a modular packing system to keep organized.")

    # 7. Itinerary / Timing / Attractions
    elif matches(['day', 'itinerary', 'plan', 'schedule', 'activity', 'activities', 'tour', 'visit', 'landmarks', 'see', 'do']):
        reply = (f"Your {days}-day itinerary is designed to balance major landmarks with local discovery. "
                 f"If you're feeling energetic, I suggest doing the 'big' attractions before 10 AM. "
                 f"Would you like me to suggest a 'hidden gem' in {dest} that isn't on the standard tourist maps?")

    # 8. Weather & Seasonal Advice
    elif matches(['weather', 'temperature', 'rain', 'hot', 'cold', 'climate', 'season', 'best time']):
        reply = (f"I'm monitoring the live conditions for {dest}. Always pack a compact umbrella or a light shell—weather in this region can be beautifully unpredictable. Check your Weather widget for the 7-day outlook!")

    # 9. Transport / Transit
    elif matches(['transport', 'taxi', 'uber', 'metro', 'bus', 'train', 'flight', 'airport', 'transit', 'drive', 'car']):
        reply = (f"Navigating {dest} is part of the adventure! Public transit is usually the most efficient. "
                 f"Pro tip: Download the local transit app as soon as you land. For late-night travel, always use reputable rideshare apps over unmarked taxis.")

    # 10. Thank You / Closing
    elif matches(['thank', 'thanks', 'great', 'awesome', 'perfect', 'good', 'helpful', 'bye', 'goodbye']):
        reply = f"It's my absolute pleasure to assist with your {dest} journey! I'll be right here if you need anything else. Safe travels, and enjoy every moment!"

    # Fallback
    else:
        reply = (f"That's a fascinating question about {dest}! While I don't have that specific data point yet, "
                 f"I can certainly help you with food, local etiquette, safety, or logistical planning. "
                 f"What aspect of your {days}-day trip shall we optimize next?")

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
