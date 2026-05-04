# Dora Travel Intelligence Hub

**A professional-grade, AI-powered travel planning engine with real-time intelligence, dynamic pricing, and a cinematic 3D globe experience.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Three.js](https://img.shields.io/badge/Three.js-Globe.gl-black?style=for-the-badge&logo=threedotjs&logoColor=white)](https://globe.gl/)
[![Vercel](https://img.shields.io/badge/Live%20on-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

[View Live Demo](https://dora-travel-agency.vercel.app) · [Report a Bug](https://github.com/narwal4421/dora-travel-agency/issues) · [Request a Feature](https://github.com/narwal4421/dora-travel-agency/issues)

---

## Overview

Dora is not just a travel planner — it is a **Travel Intelligence Engine**. Users enter a destination, trip duration, budget, and personal interests, and the platform orchestrates multiple real-world APIs and a curated intelligence database to produce:

- A **structured, day-by-day itinerary** with interest-based ranking of real attractions
- **Three dynamic travel packages** (Essential, Signature, Royal Prestige) with realistic pricing
- A **full Travel Intelligence dashboard** covering safety, logistics, culture, and local essentials
- An **AI Chat Assistant** for real-time trip advice
- A **cinematic 3D globe** loading experience with animated flight arcs

All of this is presented through a premium glassmorphism UI with dark/light theme support and **multi-language localization** (English, Hindi, Spanish, French).

---

## Feature Suite

### Core Planning Engine

| Feature | Description |
| --- | --- |
| **Cinematic 3D Globe** | Interactive globe (Three.js + Globe.gl) with animated flight arcs, destination pin drops, and dramatic cinematic zoom |
| **AI Itinerary Generator** | Structured day-by-day plans: Arrival Day → Deep Exploration → Farewell Day, ranked by user interests |
| **Dynamic Pricing Engine** | Three-tier packages with real-world cost calculations based on destination spend data, flight class, and hotel quality |
| **Live Weather Widget** | Real-time weather via Open-Meteo API with contextual packing and activity tips |
| **Interactive Map** | Leaflet-powered map with attraction markers, destination pins, and a legend overlay |
| **AI Chat Assistant** | Context-aware trip companion that answers questions about your destination using trip data |
| **Calendar Export** | One-click export to Google Calendar or downloadable `.ics` file for Apple Calendar |

### Travel Intelligence Dashboard

All 11 intelligence features are accessible from the **Travel Intel** tab after generating a trip:

| Widget | What It Does |
| --- | --- |
| **Live Local Time** | Real-time clock synced to destination timezone (IANA-based) |
| **Air Quality Index** | Live AQI data from Open-Meteo Air Quality API with Good/Fair/Poor labels |
| **Live Currency Converter** | Real-time USD-to-local conversion via the Frankfurter API |
| **Best Time to Visit** | Optimal travel months with seasonal advice for each destination |
| **Daily Spend Estimator** | Budget / Mid-Range / Luxury daily cost breakdown per destination |
| **Scam Encyclopedia** | Country-specific scam warnings with descriptions and avoidance tactics |
| **Must-Download Apps** | Essential local apps (transport, maps, translation) with usage descriptions |
| **Emergency Numbers** | Police, ambulance, fire, and tourist helpline numbers per country |
| **Power Plug & Water Guide** | Plug type, voltage, and tap water safety information |
| **SIM Card Guide** | Local SIM recommendations and connectivity advice |
| **Traveler Tips Feed** | Auto-rotating carousel of curated cultural and logistical tips |

### User Experience

| Feature | Description |
| --- | --- |
| **Dark / Light Mode** | Full theme system with CSS variables and smooth transitions |
| **Multi-Language UI** | Complete interface localization — English, Hindi (हिन्दी), Spanish (Español), French (Français) |
| **Smart Packing List** | Weather-adaptive packing checklist (cold gear, sun protection, etc.) |
| **Local Culture Guide** | Language basics, currency info, food scene, cultural etiquette, and safety advisories |

---

## Tech Stack

### Frontend

| Technology | Purpose |
| --- | --- |
| HTML5 | Semantic single-page application shell |
| Vanilla CSS | Custom design system — CSS variables, glassmorphism, micro-animations |
| JavaScript (ES6+) | Async API orchestration, DOM rendering, state management |
| Three.js + Globe.gl | Cinematic 3D globe with arc animations and HTML pin overlays |
| Leaflet.js | Interactive attraction map with custom markers |
| Font Awesome 6 | Icon library (400+ icons used across intel widgets) |
| Google Fonts | Playfair Display (headings) + Inter (body) for premium typography |

### Backend

| Technology | Purpose |
| --- | --- |
| Python 3.8+ | Runtime |
| Flask 2.2 | REST API framework with CORS support |
| 9 Intelligence Databases | `CULTURE_DB`, `BEST_TIME_DB`, `TIMEZONE_DB`, `SCAM_DB`, `APPS_DB`, `EMERGENCY_DB`, `UTILITIES_DB`, `SPEND_DB`, `TIPS_DB` |
| Dynamic Pricing Engine | Multi-tier cost calculator using real spend data + flight/hotel preferences |

### External APIs

| API | Usage | Auth |
| --- | --- | --- |
| [Open-Meteo Weather](https://open-meteo.com/) | Real-time weather forecasts | None |
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | City → lat/lon resolution | None |
| [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api) | Live AQI data | None |
| [Overpass API (OSM)](https://overpass-api.de/) | Real tourist attractions near coordinates | None |
| [Frankfurter API](https://www.frankfurter.app/) | Live currency exchange rates | None |

### Deployment

| Platform | Configuration |
| --- | --- |
| Vercel | Zero-config serverless deployment via `vercel.json` API rewrites |

---

## Project Structure

```text
dora-travel-agency/
├── index.html             # Single-page app shell — search form + results dashboard
├── style.css              # Full design system — theming, glassmorphism, animations
├── script.js              # Frontend logic — globe, API calls, intel rendering, chat, i18n
├── api/
│   └── index.py           # Flask REST API — trip planning, weather, chat, intelligence
├── requirements.txt       # Python dependencies (Flask, requests, flask-cors)
├── vercel.json            # Vercel serverless routing configuration
└── README.md              # This file
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- A modern browser (Chrome, Firefox, Edge)

### 1. Clone the repository

```bash
git clone https://github.com/narwal4421/dora-travel-agency.git
cd dora-travel-agency
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
cd api
python index.py
```

The Flask API will start at `http://127.0.0.1:5000`.

### 4. Open the frontend

Open `index.html` in your browser, or serve it locally:

```bash
python -m http.server 8080
```

Then navigate to `http://localhost:8080`.

> **Note:** The frontend auto-detects localhost and routes API requests to `http://127.0.0.1:5000/api`. No additional configuration needed.

---

## Deployment on Vercel

This project is preconfigured for **zero-configuration deployment**:

1. Push to your GitHub repository
2. Import the repo at [vercel.com/new](https://vercel.com/new)
3. Vercel detects `vercel.json` and deploys automatically

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ]
}
```

> **Important:** The backend entry point must remain at `api/index.py` for Vercel's Python runtime.

---

## API Reference

### `POST /api/plan-trip`

Generates a complete travel plan with packages, itinerary, and intelligence data.

**Request Body**

```json
{
  "destination": "Tokyo",
  "days": 5,
  "budget": "medium",
  "interests": "Food, History",
  "flightOption": "economy",
  "hotelChoice": "Hilton"
}
```

**Response** (abbreviated)

```json
{
  "destination": "Tokyo",
  "days": 5,
  "lat": 35.6762,
  "lon": 139.6503,
  "packages": [
    {
      "id": "low",
      "name": "Essential Explorer",
      "estimatedCost": "$1,250 - $1,750",
      "hotel": "Budget hotels & hostels",
      "flights": "Economy class",
      "itinerary": [...]
    }
  ],
  "mustVisits": [...],
  "localGuide": {
    "culture": "Bow when greeting...",
    "food": "Sushi, Ramen, Tempura...",
    "safety": "Extremely safe...",
    "language": "Japanese (日本語)...",
    "currency": "Japanese Yen (¥)"
  },
  "intel": {
    "bestTime": { "months": "Mar-May, Oct-Nov", "advice": "Cherry blossom season..." },
    "timezone": "Asia/Tokyo",
    "spend": { "low": "$50-70/day", "mid": "$120-180/day", "high": "$300+/day" },
    "scams": [...],
    "apps": [...],
    "emergency": { "police": "110", "ambulance": "119", "fire": "119" },
    "utilities": { "power": "Type A/B, 100V", "water": "Safe to drink", "sim": "..." },
    "tips": [...]
  }
}
```

### `GET /api/weather`

Returns current weather for a city.

| Parameter | Type | Description |
| --- | --- | --- |
| `dest` | `string` | City name (e.g. `Tokyo`) |
| `lat` | `float` | Optional latitude |
| `lon` | `float` | Optional longitude |

### `POST /api/chat`

AI-powered travel assistant with destination context.

| Field | Type | Description |
| --- | --- | --- |
| `message` | `string` | User's question |
| `context` | `object` | Trip data (destination, culture, safety, etc.) |

---

## Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                         Browser                               │
│  ┌───────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │index.html │  │  script.js   │  │      style.css         │ │
│  │  (Shell)  │─▶│  (App Logic) │  │   (Design System)      │ │
│  └───────────┘  └──────┬───────┘  └────────────────────────┘ │
│                        │                                      │
│         ┌──────────────┼──────────────┐                       │
│         ▼              ▼              ▼                       │
│   ┌──────────┐  ┌───────────┐  ┌──────────┐                  │
│   │Globe.gl  │  │ Leaflet   │  │   i18n   │                  │
│   │(3D Globe)│  │(Map View) │  │(4 langs) │                  │
│   └──────────┘  └───────────┘  └──────────┘                  │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP (fetch)
          ┌──────────────▼───────────────┐
          │       Flask REST API         │
          │        (api/index.py)        │
          │                              │
          │  ┌────────────────────────┐  │
          │  │ 9 Intelligence DBs    │  │
          │  │ Dynamic Pricing Engine│  │
          │  │ Itinerary Generator   │  │
          │  └────────────────────────┘  │
          └──┬──────────┬──────────┬─────┘
             │          │          │
   ┌─────────▼───┐ ┌───▼───────┐ ┌▼────────────┐
   │ Open-Meteo  │ │ Overpass  │ │ Frankfurter │
   │Weather + Geo│ │OSM Places │ │  Currency   │
   │ + AQI       │ │           │ │  Rates      │
   └─────────────┘ └───────────┘ └─────────────┘
```

---

## Global Destination Coverage

The backend includes curated, high-fidelity intelligence for **40+ countries** across all 9 databases:

| Region | Countries |
| --- | --- |
| **Europe** | Italy · France · UK · Germany · Spain · Greece · Netherlands · Turkey · Norway · Sweden · Denmark · Poland · Czech Republic · Hungary · Austria |
| **Americas** | USA · Canada · Mexico · Brazil · Argentina · Chile · Peru · Colombia |
| **Asia & Pacific** | Japan · China · South Korea · Thailand · India · Vietnam · Singapore · Australia · New Zealand · Taiwan |
| **Middle East & Africa** | UAE · Saudi Arabia · Egypt · Kenya · South Africa · Morocco |

For unlisted destinations, the platform provides generic travel guidance derived from geocoding and weather data.

---

## Roadmap

- [x] Cinematic 3D globe loading experience
- [x] AI-powered itinerary generation
- [x] Three-tier dynamic pricing engine
- [x] Live weather with contextual tips
- [x] Interactive Leaflet map with attraction markers
- [x] AI Chat Assistant
- [x] Google Calendar & .ics export
- [x] 11-widget Travel Intelligence dashboard
- [x] Multi-language UI (EN, HI, ES, FR)
- [x] 40+ country intelligence database
- [ ] PDF itinerary export with branded design
- [ ] Deep-link hotel and flight booking integration
- [ ] User accounts with saved trips and wishlists
- [ ] Real-time collaborative trip planning

---

## Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes. Pull requests should target the `main` branch.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built with Flask, Three.js, Leaflet, and open geospatial data by Pranjal.*
*Travel Intelligence Engine v2.0*
