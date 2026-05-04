// script.js - Application Logic for AI Travel Assistant

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
const API_BASE_URL = isLocal ? 'http://127.0.0.1:5000/api' : '/api';

// Global trip state — shared by map, chat, and calendar features
let _tripData = null;
let _leafletMap = null;
let _mapInitialised = false;
let _clockInterval = null;
let _tipsInterval = null;

const TRANSLATIONS = {
    en: {
        hero_title: "Design Your Dream Trip with AI",
        hero_desc: "Enter your preferences and let our advanced AI assemble the perfect travel package and itinerary in seconds.",
        label_dest: "Destination", label_days: "Duration (Days)", label_budget: "Budget Profile", label_flights: "Flight Preference", label_hotel: "Preferred Hotel", label_interests: "Special Interests (Optional)",
        opt_budget_low: "Budget Friendly", opt_budget_mid: "Balanced / Medium", opt_budget_high: "Luxury",
        opt_flight_any: "Find Best Flights", opt_flight_none: "No Flight Needed", opt_flight_econ: "Economy Class Only", opt_flight_biz: "Business/First Class",
        btn_generate: "Generate Itinerary", loader_desc: "Crafting your perfect itinerary...",
        res_title: "Your trip to", btn_ask_ai: "Ask AI", btn_google_cal: "Google Cal", btn_download_ics: "Download .ics", btn_new_search: "New Search",
        tab_packages: "Packages", tab_itinerary: "Itinerary", tab_local: "Local Guide", tab_intel: "Travel Intel", tab_map: "Interactive Map",
        export_label: "Export itinerary", guide_visits: "Must Visits", guide_lang: "Language", guide_curr: "Currency", guide_culture: "Culture Protocol", guide_food: "Food Scene", guide_safety: "Safety", guide_packing: "Smart Packing List",
        intel_local_time: "Local Time", intel_aqi: "Air Quality", intel_converter: "Converter", intel_best_time: "Best Time to Visit", intel_daily_spend: "Daily Spend Estimator", intel_utilities: "Power & Water", intel_emergency: "Emergency Numbers", intel_sim: "SIM Card Guide", intel_apps: "Must-Download Apps", intel_scams: "Scam Encyclopedia", intel_tips: "Traveler Tips Feed"
    },
    hi: {
        hero_title: "AI के साथ अपनी सपनों की यात्रा डिज़ाइन करें",
        hero_desc: "अपनी प्राथमिकताएं दर्ज करें और हमारे उन्नत AI को सेकंडों में सही यात्रा पैकेज और यात्रा कार्यक्रम बनाने दें।",
        label_dest: "गंतव्य", label_days: "अवधि (दिन)", label_budget: "बजट प्रोफ़ाइल", label_flights: "उड़ान प्राथमिकता", label_hotel: "पसंदीदा होटल", label_interests: "विशेष रुचियां (वैकल्पिक)",
        opt_budget_low: "बजट के अनुकूल", opt_budget_mid: "संतुलित / मध्यम", opt_budget_high: "लक्जरी",
        opt_flight_any: "सर्वोत्तम उड़ानें खोजें", opt_flight_none: "किसी उड़ान की आवश्यकता नहीं", opt_flight_econ: "केवल इकोनॉमी क्लास", opt_flight_biz: "बिजनेस/फर्स्ट क्लास",
        btn_generate: "यात्रा कार्यक्रम तैयार करें", loader_desc: "आपका आदर्श यात्रा कार्यक्रम तैयार किया जा रहा है...",
        res_title: "आपकी यात्रा", btn_ask_ai: "AI से पूछें", btn_google_cal: "गूगल कैलेंडर", btn_download_ics: ".ics डाउनलोड करें", btn_new_search: "नई खोज",
        tab_packages: "पैकेज", tab_itinerary: "यात्रा कार्यक्रम", tab_local: "स्थानीय गाइड", tab_intel: "यात्रा इंटेल", tab_map: "इंटरैक्टिव मैप",
        export_label: "यात्रा कार्यक्रम निर्यात करें", guide_visits: "अवश्य देखें", guide_lang: "भाषा", guide_curr: "मुद्रा", guide_culture: "संस्कृति प्रोटोकॉल", guide_food: "भोजन दृश्य", guide_safety: "सुरक्षा", guide_packing: "स्मार्ट पैकिंग सूची",
        intel_local_time: "स्थानीय समय", intel_aqi: "वायु गुणवत्ता", intel_converter: "कनवर्टर", intel_best_time: "यात्रा का सबसे अच्छा समय", intel_daily_spend: "दैनिक खर्च अनुमानक", intel_utilities: "बिजली और पानी", intel_emergency: "आपातकालीन नंबर", intel_sim: "सिम कार्ड गाइड", intel_apps: "अवश्य डाउनलोड करें ऐप्स", intel_scams: "स्कैम विश्वकोश", intel_tips: "यात्री टिप्स फीड"
    },
    es: {
        hero_title: "Diseña tu viaje de ensueño con IA",
        hero_desc: "Ingresa tus preferencias y deja que nuestra IA avanzada arme el paquete de viaje y el itinerario perfectos en segundos.",
        label_dest: "Destino", label_days: "Duración (Días)", label_budget: "Perfil de presupuesto", label_flights: "Preferencia de vuelo", label_hotel: "Hotel preferido", label_interests: "Intereses especiales (Opcional)",
        opt_budget_low: "Económico", opt_budget_mid: "Equilibrado / Medio", opt_budget_high: "Lujo",
        opt_flight_any: "Buscar mejores vuelos", opt_flight_none: "Sin vuelo", opt_flight_econ: "Clase económica", opt_flight_biz: "Clase Ejecutiva/Primera",
        btn_generate: "Generar itinerario", loader_desc: "Creando tu itinerario perfecto...",
        res_title: "Tu viaje a", btn_ask_ai: "Preguntar a IA", btn_google_cal: "Google Cal", btn_download_ics: "Descargar .ics", btn_new_search: "Nueva búsqueda",
        tab_packages: "Paquetes", tab_itinerary: "Itinerario", tab_local: "Guía local", tab_intel: "Info de viaje", tab_map: "Mapa interactivo",
        export_label: "Exportar itinerario", guide_visits: "Visitas obligadas", guide_lang: "Idioma", guide_curr: "Moneda", guide_culture: "Protocolo cultural", guide_food: "Gastronomía", guide_safety: "Seguridad", guide_packing: "Lista de empaque",
        intel_local_time: "Hora local", intel_aqi: "Calidad del aire", intel_converter: "Conversor", intel_best_time: "Mejor época", intel_daily_spend: "Gasto diario", intel_utilities: "Electricidad y Agua", intel_emergency: "Emergencias", intel_sim: "Guía de SIM", intel_apps: "Apps recomendadas", intel_scams: "Enciclopedia de estafas", intel_tips: "Consejos de viajeros"
    },
    fr: {
        hero_title: "Concevez votre voyage de rêve avec l'IA",
        hero_desc: "Entrez vos préférences et laissez notre IA avancée assembler le forfait voyage et l'itinéraire parfaits en quelques secondes.",
        label_dest: "Destination", label_days: "Durée (Jours)", label_budget: "Profil budgétaire", label_flights: "Préférence de vol", label_hotel: "Hôtel préféré", label_interests: "Intérêts particuliers (Optionnel)",
        opt_budget_low: "Économique", opt_budget_mid: "Équilibré / Moyen", opt_budget_high: "Luxe",
        opt_flight_any: "Trouver les meilleurs vols", opt_flight_none: "Pas de vol nécessaire", opt_flight_econ: "Classe Économie", opt_flight_biz: "Classe Affaires/Première",
        btn_generate: "Générer l'itinéraire", loader_desc: "Création de votre itinéraire...",
        res_title: "Votre voyage à", btn_ask_ai: "Demander à l'IA", btn_google_cal: "Google Cal", btn_download_ics: "Télécharger .ics", btn_new_search: "Nouvelle recherche",
        tab_packages: "Forfaits", tab_itinerary: "Itinéraire", tab_local: "Guide local", tab_intel: "Infos voyage", tab_map: "Carte interactive",
        export_label: "Exporter l'itinéraire", guide_visits: "Incontournables", guide_lang: "Langue", guide_curr: "Devise", guide_culture: "Protocole culturel", guide_food: "Gastronomie", guide_safety: "Sécurité", guide_packing: "Liste de bagages",
        intel_local_time: "Heure locale", intel_aqi: "Qualité de l'air", intel_converter: "Convertisseur", intel_best_time: "Meilleure période", intel_daily_spend: "Dépenses quotidiennes", intel_utilities: "Électricité et Eau", intel_emergency: "Urgences", intel_sim: "Guide SIM", intel_apps: "Apps recommandées", intel_scams: "Encyclopédie des arnaques", intel_tips: "Conseils voyageurs"
    }
};

document.addEventListener('DOMContentLoaded', () => {

    // Language Switching
    const langSelect = document.getElementById('lang-select');
    langSelect.addEventListener('change', (e) => {
        applyLanguage(e.target.value);
    });

    function applyLanguage(lang) {
        const t = TRANSLATIONS[lang] || TRANSLATIONS.en;
        document.querySelectorAll('[data-t]').forEach(el => {
            const key = el.getAttribute('data-t');
            if (t[key]) el.textContent = t[key];
        });
    }
    
    // Set initial language from selector
    applyLanguage(langSelect.value);

    // Theme Toggling
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {
        const html = document.documentElement;
        if (html.getAttribute('data-theme') === 'dark') {
            html.removeAttribute('data-theme');
            themeToggle.innerHTML = '<i class="fa-solid fa-sun" style="color: #fbbf24;"></i>';
        } else {
            html.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        }
    });

    // View Management
    const searchView = document.getElementById('search-view');
    const resultsView = document.getElementById('results-view');
    const loadingOverlay = document.getElementById('cinematic-loader');
    const globeViz = document.getElementById('globeViz');
    const destReveal = document.getElementById('destination-reveal');
    const destName = document.getElementById('cinematic-dest-name');
    const newSearchBtn = document.getElementById('new-search-btn');

    newSearchBtn.addEventListener('click', () => {
        resultsView.classList.remove('active');
        resultsView.classList.add('hidden');
        searchView.classList.remove('hidden');
        setTimeout(() => searchView.classList.add('active'), 50);
        if (_clockInterval) clearInterval(_clockInterval);
        if (_tipsInterval) clearInterval(_tipsInterval);
    });

    // Form Submission
    const tripForm = document.getElementById('trip-form');
    tripForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const destination = document.getElementById('destination').value.trim();
        const days = document.getElementById('days').value;
        const budget = document.getElementById('budget').value;
        const interests = document.getElementById('interests').value.trim();
        const flightOption = document.getElementById('flight-option').value;
        const hotelChoice = document.getElementById('hotel-choice').value.trim();

        if(!destination) return;

        loadingOverlay.classList.remove('hidden');
        destReveal.classList.add('hidden');
        destName.textContent = destination;
        
        globeViz.innerHTML = '';
        const world = Globe()
            (globeViz)
            .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
            .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
            .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
            .backgroundColor('#000000')
            .atmosphereColor('#d4af37')
            .atmosphereAltitude(0.25);
            
        const parsingArcs = [...Array(100).keys()].map(() => ({
            startLat: (Math.random() - 0.5) * 180, startLng: (Math.random() - 0.5) * 360,
            endLat: (Math.random() - 0.5) * 180, endLng: (Math.random() - 0.5) * 360,
            color: ['rgba(212, 175, 55, 0)', 'rgba(212, 175, 55, 0.4)']
        }));
        
        world.arcsData(parsingArcs)
            .arcColor('color')
            .arcDashLength(0.3)
            .arcDashGap(0.1)
            .arcDashInitialGap(() => Math.random() * 2)
            .arcDashAnimateTime(2000)
            .arcStroke(0.3);

        world.pointOfView({ altitude: 2.5 }, 0);
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 4;
        world.controls().enableZoom = false;

        try {
            const planResponse = await fetch(`${API_BASE_URL}/plan-trip`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ destination, days, budget, interests, flightOption, hotelChoice })
            });

            if (!planResponse.ok) throw new Error('Failed to generate trip');
            const planData = await planResponse.json();

            fetchWeather(destination);
            renderResults(planData, budget);

            world.controls().autoRotate = false;
            world.ringsData([
                { lat: planData.lat, lng: planData.lon, maxR: 4, speed: 2 },
                { lat: planData.lat, lng: planData.lon, maxR: 8, speed: 1.5 },
                { lat: planData.lat, lng: planData.lon, maxR: 15, speed: 1 }
            ])
            .ringColor(() => '#d4af37')
            .ringMaxRadius('maxR')
            .ringPropagationSpeed('speed')
            .ringRepeatPeriod(800);
            
            world.arcsData([{ startLat: 51.5, startLng: -0.1, endLat: planData.lat, endLng: planData.lon }])
                .arcColor(() => ['rgba(212, 175, 55, 0)', '#d4af37'])
                .arcDashLength(0.8)
                .arcDashGap(0.2)
                .arcDashAnimateTime(2500)
                .arcAltitudeAutoScale(0.6)
                .arcStroke(2.5);

            world.htmlElementsData([{ lat: planData.lat, lng: planData.lon }])
                .htmlElement(d => {
                    const el = document.createElement('div');
                    el.innerHTML = `
                      <div style="animation: bounce 1s infinite alternate; filter: drop-shadow(0 0 30px #e5c558);">
                          <i class="fa-solid fa-location-dot" style="color: #d4af37; font-size: 3.5rem;"></i>
                      </div>
                      <style>@keyframes bounce { 0% { transform: translateY(0); } 100% { transform: translateY(-20px); } }</style>
                    `;
                    return el;
                });
                
            world.pointOfView({ lat: planData.lat, lng: planData.lon, altitude: 0.04 }, 4500);

            setTimeout(() => {
                destReveal.classList.remove('hidden');
                setTimeout(() => {
                    loadingOverlay.classList.add('hidden');
                    searchView.classList.remove('active');
                    searchView.classList.add('hidden');
                    resultsView.classList.remove('hidden');
                    setTimeout(() => resultsView.classList.add('active'), 50);
                }, 3500);
            }, 4000);

        } catch (error) {
            console.error(error);
            alert("Error generating trip. Please make sure the backend server responds.");
            loadingOverlay.classList.add('hidden');
        }
    });

    // Weather Fetching
    async function fetchWeather(destination) {
        const wTemp = document.getElementById('w-temp');
        const wCond = document.getElementById('w-condition');
        const wTips = document.getElementById('w-tips');
        const wIcon = document.getElementById('weather-icon-class');

        wTemp.textContent = '--°C';
        wCond.textContent = 'Fetching weather...';
        wTips.textContent = '';
        wIcon.className = 'fa-solid fa-cloud-sun';

        try {
            const resp = await fetch(`${API_BASE_URL}/weather?dest=${encodeURIComponent(destination)}`);
            if(!resp.ok) throw new Error('Weather fetch failed');
            
            const data = await resp.json();
            wTemp.textContent = `${data.temperature}°C`;
            wCond.textContent = data.condition;
            wTips.textContent = data.tips;
            generatePackingList(data.temperature);

            const cond = data.condition.toLowerCase();
            if(cond.includes('clear')) wIcon.className = 'fa-solid fa-sun';
            else if(cond.includes('rain') || cond.includes('drizzle')) wIcon.className = 'fa-solid fa-cloud-rain';
            else if(cond.includes('snow')) wIcon.className = 'fa-snowflake';
            else if(cond.includes('thunder')) wIcon.className = 'fa-bolt';
            else wIcon.className = 'fa-solid fa-cloud';

        } catch (err) {
            console.error(err);
            wCond.textContent = 'Weather data unavailable';
            generatePackingList(null);
        }
    }

    // Render Data
    function renderResults(data, preferredBudget) {
        document.getElementById('res-destination').textContent = data.destination;

        const packagesContainer = document.getElementById('packages-container');
        packagesContainer.innerHTML = '';
        
        data.packages.forEach(pkg => {
            const isPreferred = pkg.id === preferredBudget;
            const card = document.createElement('div');
            card.className = `package-card ${isPreferred ? 'selected' : ''}`;
            if(isPreferred) {
                card.innerHTML = `<div style="position: absolute; top:0; right:0; background: var(--accent-gradient); color: white; padding: 4px 12px; font-size: 0.8rem; border-bottom-left-radius: 8px; font-weight: bold;">Matches Budget</div>`;
            }

            card.innerHTML += `
                <div class="package-header">
                    <h3>${pkg.name}</h3>
                    <p>${pkg.description}</p>
                    <div class="package-price">${pkg.estimatedCost}</div>
                </div>
                <ul class="package-features">
                    <li><i class="fa-solid fa-bed"></i> ${pkg.hotel}</li>
                    <li><i class="fa-solid fa-plane"></i> ${pkg.flights}</li>
                    <li><i class="fa-solid fa-car"></i> ${pkg.transportation}</li>
                </ul>
                <div style="display:flex; gap:1rem; margin-top:1rem;">
                    <button class="primary-btn select-pkg-btn" style="flex:1;" data-id="${pkg.id}">View Itinerary</button>
                    <button class="secondary-btn" style="flex:1; justify-content:center; opacity:0.6; cursor:not-allowed;" disabled>Book Package <span class="badge">Soon</span></button>
                </div>
            `;
            packagesContainer.appendChild(card);
        });

        document.querySelectorAll('.select-pkg-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const pkgId = e.target.getAttribute('data-id');
                const selectedPkg = data.packages.find(p => p.id === pkgId);
                renderItinerary(selectedPkg.itinerary);
                switchTab('itinerary');
            });
        });

        const defaultPkg = data.packages.find(p => p.id === preferredBudget) || data.packages[0];
        renderItinerary(defaultPkg.itinerary);

        const mustVisitsList = document.getElementById('must-visits-list');
        mustVisitsList.innerHTML = '';
        data.mustVisits.forEach(v => {
            mustVisitsList.innerHTML += `
                <li>
                    <strong>${v.name}</strong>
                    <small style="color: var(--accent-color)">${v.category}</small>
                    <p style="margin-top: 5px;">${v.desc}</p>
                </li>
            `;
        });

        document.getElementById('guide-culture').textContent = data.localGuide.culture;
        document.getElementById('guide-food').textContent = data.localGuide.food;
        document.getElementById('guide-safety').textContent = data.localGuide.safety;
        document.getElementById('guide-language').textContent = data.localGuide.language;
        document.getElementById('guide-currency').textContent = data.localGuide.currency;

        // Render Travel Intel
        renderTravelIntel(data.intel, data.destination);
        initCurrencyConverter('USD', data.localGuide.currency);
        initAQI(data.lat, data.lon);

        _tripData = data;
        _mapInitialised = false;

        ['cal-google-btn','it-google-btn'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.onclick = () => exportToGoogleCalendar(data);
        });
        ['cal-ics-btn','it-ics-btn'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.onclick = () => exportToICS(data);
        });
    }

    function renderTravelIntel(intel, destination) {
        // Best Time
        document.getElementById('intel-best-months').textContent = intel.bestTime.months;
        document.getElementById('intel-best-advice').textContent = intel.bestTime.advice;

        // Timezone
        if (_clockInterval) clearInterval(_clockInterval);
        _clockInterval = setInterval(() => {
            const timeStr = new Date().toLocaleTimeString('en-US', { timeZone: intel.timezone, hour12: false });
            document.getElementById('intel-local-time').textContent = timeStr;
        }, 1000);

        // Spend Grid
        const spendGrid = document.getElementById('intel-spend-grid');
        spendGrid.innerHTML = `
            <div class="spend-item"><span class="spend-label">Budget</span><span class="spend-val">${intel.spend.low}</span></div>
            <div class="spend-item"><span class="spend-label">Mid-Range</span><span class="spend-val">${intel.spend.mid}</span></div>
            <div class="spend-item"><span class="spend-label">Luxury</span><span class="spend-val">${intel.spend.high}</span></div>
        `;

        // Utilities
        const utilList = document.getElementById('intel-util-list');
        utilList.innerHTML = `
            <div class="util-item">
                <div class="util-icon"><i class="fa-solid fa-plug"></i></div>
                <div class="util-text"><h4>Power</h4><p>${intel.utilities.power}</p></div>
            </div>
            <div class="util-item">
                <div class="util-icon"><i class="fa-solid fa-droplet"></i></div>
                <div class="util-text"><h4>Water</h4><p>${intel.utilities.water}</p></div>
            </div>
        `;
        document.getElementById('intel-sim-guide').textContent = intel.utilities.sim;

        // Emergency
        const emGrid = document.getElementById('intel-emergency-grid');
        emGrid.innerHTML = '';
        for (const [key, val] of Object.entries(intel.emergency)) {
            emGrid.innerHTML += `<div class="emergency-item"><small>${key}</small><strong>${val}</strong></div>`;
        }

        // Apps
        const appsGrid = document.getElementById('intel-apps-grid');
        appsGrid.innerHTML = '';
        intel.apps.forEach(app => {
            appsGrid.innerHTML += `<div class="app-card"><strong><i class="fa-solid fa-circle-check"></i> ${app.name}</strong><p>${app.usage}</p></div>`;
        });

        // Scams
        const scamList = document.getElementById('intel-scam-list');
        scamList.innerHTML = '';
        intel.scams.forEach(s => {
            scamList.innerHTML += `<div class="scam-item"><h4>${s.title}</h4><p>${s.desc}</p></div>`;
        });

        // Tips Carousel
        startTipsCarousel(intel.tips);
    }

    async function initCurrencyConverter(from, toRaw) {
        // Simple regex to extract ISO code if possible, e.g. "Japanese Yen (¥)" -> "JPY" is hard, 
        // so we'll look for keywords or use a fallback.
        const currTo = document.getElementById('curr-to-sym');
        const currVal = document.getElementById('curr-to-val');
        const amountInput = document.getElementById('curr-amount');
        
        // Map common names to ISO codes
        const currMap = { "Yen": "JPY", "Euro": "EUR", "Pound": "GBP", "Rupee": "INR", "Baht": "THB", "Dollar": "USD", "Peso": "MXN", "Real": "BRL", "Franc": "CHF" };
        let toISO = "EUR"; // default
        for (const [name, code] of Object.entries(currMap)) {
            if (toRaw.includes(name)) { toISO = code; break; }
        }
        
        document.getElementById('curr-from').textContent = "USD";
        currTo.textContent = toISO;

        async function updateRate() {
            try {
                const res = await fetch(`https://api.frankfurter.app/latest?amount=${amountInput.value}&from=USD&to=${toISO}`);
                const data = await res.json();
                currVal.textContent = data.rates[toISO].toFixed(2);
            } catch(e) { currVal.textContent = "??"; }
        }

        amountInput.addEventListener('input', updateRate);
        updateRate();
    }

    async function initAQI(lat, lon) {
        const aqiEl = document.getElementById('intel-aqi');
        try {
            const res = await fetch(`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=us_aqi`);
            const data = await res.json();
            const aqi = data.current.us_aqi;
            let label = "Good";
            if (aqi > 50) label = "Fair";
            if (aqi > 100) label = "Poor";
            aqiEl.textContent = `${aqi} (${label})`;
        } catch(e) { aqiEl.textContent = "N/A"; }
    }

    function startTipsCarousel(tips) {
        const container = document.getElementById('tips-container');
        const dotsContainer = document.getElementById('tips-dots');
        container.innerHTML = '';
        dotsContainer.innerHTML = '';
        if (_tipsInterval) clearInterval(_tipsInterval);

        tips.forEach((tip, i) => {
            const slide = document.createElement('div');
            slide.className = `tip-slide ${i === 0 ? 'active' : ''}`;
            slide.textContent = `"${tip}"`;
            container.appendChild(slide);

            const dot = document.createElement('div');
            dot.className = `tip-dot ${i === 0 ? 'active' : ''}`;
            dot.addEventListener('click', () => showTip(i));
            dotsContainer.appendChild(dot);
        });

        let current = 0;
        function showTip(index) {
            const slides = document.querySelectorAll('.tip-slide');
            const dots = document.querySelectorAll('.tip-dot');
            slides[current].classList.remove('active');
            dots[current].classList.remove('active');
            current = index;
            slides[current].classList.add('active');
            dots[current].classList.add('active');
        }

        _tipsInterval = setInterval(() => {
            showTip((current + 1) % tips.length);
        }, 4000);
    }

    function renderItinerary(itinerary) {
        const timeline = document.getElementById('itinerary-timeline');
        timeline.innerHTML = '';

        itinerary.forEach(day => {
            let activitiesHtml = day.activities.map(act => `<li>${act}</li>`).join('');
            
            timeline.innerHTML += `
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <h4>Day ${day.day}</h4>
                        <ul>${activitiesHtml}</ul>
                    </div>
                </div>
            `;
        });
    }

    // Tabs Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    function switchTab(tabId) {
        tabBtns.forEach(btn => {
            if(btn.dataset.tab === tabId) btn.classList.add('active');
            else btn.classList.remove('active');
        });
        tabPanes.forEach(pane => {
            if(pane.id === `tab-${tabId}`) pane.classList.add('active');
            else pane.classList.remove('active');
        });
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchTab(btn.dataset.tab);
            if (btn.dataset.tab === 'map' && !_mapInitialised && _tripData) {
                setTimeout(() => initMap(_tripData), 80);
            }
        });
    });

    function generatePackingList(temp) {
        const packingList = document.getElementById('packing-list');
        packingList.innerHTML = '';
        let items = [
            '<i class="fa-solid fa-plug" style="width:20px; color:var(--text-secondary)"></i> Universal Power Adapter', 
            '<i class="fa-solid fa-passport" style="width:20px; color:var(--text-secondary)"></i> Passport & Docs', 
            '<i class="fa-solid fa-shoe-prints" style="width:20px; color:var(--text-secondary)"></i> Walking Shoes', 
            '<i class="fa-solid fa-battery-full" style="width:20px; color:var(--text-secondary)"></i> Power Bank'
        ];
        
        if (temp !== null) {
            if (temp < 10) {
                items.push('<i class="fa-solid fa-mitten" style="width:20px; color:var(--text-secondary)"></i> Heavy Winter Coat');
                items.push('<i class="fa-brands fa-redhat" style="width:20px; color:var(--text-secondary)"></i> Beanie & Gloves');
            } else if (temp > 25) {
                items.push('<i class="fa-solid fa-sun" style="width:20px; color:var(--text-secondary)"></i> Sunscreen (SPF 50+)');
                items.push('<i class="fa-solid fa-glasses" style="width:20px; color:var(--text-secondary)"></i> Sunglasses & Hat');
            } else {
                items.push('<i class="fa-solid fa-shirt" style="width:20px; color:var(--text-secondary)"></i> Light Jacket');
                items.push('<i class="fa-solid fa-layer-group" style="width:20px; color:var(--text-secondary)"></i> Layered Clothing');
            }
        }
        
        items.forEach(item => {
            packingList.innerHTML += `<li style="padding: 6px 0; font-size: 0.9rem;">${item}</li>`;
        });
    }

    // ─── Interactive Map (Leaflet + OpenStreetMap) ──────────────────
    function initMap(data) {
        if (_mapInitialised) return;
        _mapInitialised = true;

        const lat = data.lat || 35.6762;
        const lon = data.lon || 139.6503;

        if (_leafletMap) { _leafletMap.remove(); _leafletMap = null; }

        _leafletMap = L.map('leaflet-map', { zoomControl: true }).setView([lat, lon], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(_leafletMap);

        const goldIcon = L.divIcon({
            className: '',
            html: `<div style="font-size:2rem;filter:drop-shadow(0 0 8px #d4af37);line-height:1;">📍</div>`,
            iconAnchor: [14, 32], popupAnchor: [0, -34]
        });

        L.marker([lat, lon], { icon: goldIcon })
            .addTo(_leafletMap)
            .bindPopup(`<strong>${data.destination}</strong><br>Your destination`)
            .openPopup();

        const legend = document.getElementById('map-legend');
        if (legend) legend.innerHTML =
            `<span><span class="map-legend-dot" style="background:#d4af37"></span>Destination</span>` +
            `<span><span class="map-legend-dot" style="background:#888"></span>Attractions</span>`;

        if (data.mustVisits && data.mustVisits.length) {
            data.mustVisits.forEach((place, i) => {
                const offsetLat = lat + (Math.random() - 0.5) * 0.04;
                const offsetLon = lon + (Math.random() - 0.5) * 0.04;
                const attrIcon = L.divIcon({
                    className: '',
                    html: `<div style="width:12px;height:12px;border-radius:50%;background:#888;border:2px solid #555;"></div>`,
                    iconAnchor: [6, 6], popupAnchor: [0, -10]
                });
                L.marker([offsetLat, offsetLon], { icon: attrIcon })
                    .addTo(_leafletMap)
                    .bindPopup(`<strong>${place.name}</strong><br><em style="color:#d4af37">${place.category}</em><br>${place.desc}`);
            });
        }
    }

    // ─── Calendar Export ─────────────────────────────────────────────
    function exportToGoogleCalendar(data) {
        const today = new Date();
        data.packages[0].itinerary.forEach((day, i) => {
            const start = new Date(today);
            start.setDate(today.getDate() + i);
            const fmt = d => d.toISOString().replace(/[-:]/g,'').split('.')[0] + 'Z';
            const details = day.activities.join(' | ');
            const url = `https://calendar.google.com/calendar/render?action=TEMPLATE` +
                `&text=${encodeURIComponent(`Day ${day.day} – ${data.destination}`)}` +
                `&dates=${fmt(start)}/${fmt(start)}` +
                `&details=${encodeURIComponent(details)}`;
            setTimeout(() => window.open(url, '_blank'), i * 300);
        });
    }

    function exportToICS(data) {
        const today = new Date();
        let ics = `BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Dora Travel Agency//EN\r\n`;
        data.packages[0].itinerary.forEach((day, i) => {
            const d = new Date(today);
            d.setDate(today.getDate() + i);
            const fmt = date => date.toISOString().replace(/[-:]/g,'').split('.')[0] + 'Z';
            const uid = `day${day.day}-${Date.now()}@dora-travel`;
            ics += `BEGIN:VEVENT\r\n`;
            ics += `UID:${uid}\r\n`;
            ics += `SUMMARY:Day ${day.day} – ${data.destination}\r\n`;
            ics += `DTSTART:${fmt(d)}\r\n`;
            ics += `DTEND:${fmt(d)}\r\n`;
            ics += `DESCRIPTION:${day.activities.join('\\n')}\r\n`;
            ics += `END:VEVENT\r\n`;
        });
        ics += `END:VCALENDAR`;
        const blob = new Blob([ics], { type: 'text/calendar' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `${data.destination.replace(/\s+/g,'-')}-itinerary.ics`;
        a.click();
    }

    // ─── AI Chat Sidebar ─────────────────────────────────────────────
    const chatSidebar  = document.getElementById('chat-sidebar');
    const chatOverlay  = document.getElementById('chat-overlay');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput    = document.getElementById('chat-input');

    function openChat() { chatSidebar.classList.add('open'); chatOverlay.classList.add('active'); chatInput.focus(); }
    function closeChat() { chatSidebar.classList.remove('open'); chatOverlay.classList.remove('active'); }

    document.getElementById('chat-toggle-btn').addEventListener('click', openChat);
    document.getElementById('chat-close-btn').addEventListener('click', closeChat);
    chatOverlay.addEventListener('click', closeChat);

    document.getElementById('chat-send-btn').addEventListener('click', sendChat);
    chatInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendChat(); });

    async function sendChat() {
        const msg = chatInput.value.trim();
        if (!msg) return;
        chatInput.value = '';

        appendBubble(msg, 'user');
        const typingEl = appendTyping();

        const context = _tripData ? {
            destination: _tripData.destination,
            days: _tripData.days,
            food: _tripData.localGuide?.food,
            culture: _tripData.localGuide?.culture,
            safety: _tripData.localGuide?.safety,
            currency: _tripData.localGuide?.currency
        } : {};

        try {
            const res = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg, context })
            });
            const json = await res.json();
            typingEl.remove();
            appendBubble(json.reply || 'I could not process that. Please try again.', 'assistant');
        } catch(e) {
            typingEl.remove();
            appendBubble('Sorry, the AI assistant is currently unavailable. Please ensure the backend server is running.', 'assistant');
        }
    }

    function appendBubble(text, role) {
        const div = document.createElement('div');
        div.className = `chat-bubble ${role}`;
        div.textContent = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return div;
    }

    function appendTyping() {
        const div = document.createElement('div');
        div.className = 'chat-bubble typing';
        div.innerHTML = `<span class="chat-typing-dot"></span><span class="chat-typing-dot"></span><span class="chat-typing-dot"></span>`;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return div;
    }

});
