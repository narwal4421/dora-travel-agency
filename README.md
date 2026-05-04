<p align="center">
  <img src="https://img.shields.io/badge/✈️_DORA-Travel_Intelligence_Hub-d4af37?style=for-the-badge&labelColor=1a1a2e" alt="Dora Travel Intelligence Hub" />
</p>

<h3 align="center">
  <em>Your AI-Powered Travel Intelligence Engine</em>
</h3>

<p align="center">
  <strong>40+ Destinations · 11 Intelligence Widgets · 4 Languages · Real-Time Data</strong>
</p>

<p align="center">
  <a href="https://dora-0027-agency.vercel.app"><img src="https://img.shields.io/badge/🌐_Live_Demo-Visit_Now-22c55e?style=for-the-badge" alt="Live Demo" /></a>
  &nbsp;
  <a href="https://github.com/narwal4421/dora-travel-agency/issues"><img src="https://img.shields.io/badge/🐛_Report-Bug-ef4444?style=for-the-badge" alt="Report Bug" /></a>
  &nbsp;
  <a href="https://github.com/narwal4421/dora-travel-agency/issues"><img src="https://img.shields.io/badge/💡_Request-Feature-8b5cf6?style=for-the-badge" alt="Request Feature" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-2.2-000000?style=flat-square&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Three.js-Globe.gl-000000?style=flat-square&logo=threedotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/Vercel-Deployed-000000?style=flat-square&logo=vercel&logoColor=white" />
  <img src="https://img.shields.io/github/license/narwal4421/dora-travel-agency?style=flat-square&color=22c55e" />
  <img src="https://img.shields.io/github/last-commit/narwal4421/dora-travel-agency?style=flat-square&color=d4af37" />
</p>

---

## 🎯 What is Dora?

**Dora** is not another travel website. It is a **full-stack Travel Intelligence Engine** that transforms a simple destination search into a comprehensive, data-rich travel briefing — powered by real-time APIs, a curated global database, and a cinematic 3D experience.

> Enter a city. Get back a complete intelligence report: structured itineraries, dynamic pricing, live weather, local scam warnings, emergency contacts, currency conversion, air quality, and cultural protocols — all in under 5 seconds.

---

## ⚡ Key Highlights

<table>
  <tr>
    <td align="center" width="25%">
      <h3>🌍</h3>
      <strong>40+ Countries</strong><br/>
      <sub>Deep intelligence data across Europe, Americas, Asia, Middle East & Africa</sub>
    </td>
    <td align="center" width="25%">
      <h3>📊</h3>
      <strong>11 Intel Widgets</strong><br/>
      <sub>Live time, AQI, currency, scams, emergency numbers, apps & more</sub>
    </td>
    <td align="center" width="25%">
      <h3>🤖</h3>
      <strong>AI Chat Assistant</strong><br/>
      <sub>Context-aware travel companion that knows your destination</sub>
    </td>
    <td align="center" width="25%">
      <h3>🌐</h3>
      <strong>4 Languages</strong><br/>
      <sub>English · Hindi · Spanish · French with full UI localization</sub>
    </td>
  </tr>
</table>

---

## 🧠 The Intelligence Suite

When you generate a trip, Dora doesn't just give you a list of places. It builds a **complete travel briefing** across three layers:

### Layer 1 — Planning Engine

| Feature | What It Does |
| --- | --- |
| 🌐 **Cinematic 3D Globe** | Three.js + Globe.gl with animated flight arcs, pin drops, and cinematic zoom-to-destination |
| 📋 **Smart Itinerary** | Structured daily flow — Arrival → Deep Exploration → Farewell Day — ranked by your interests |
| 💰 **Dynamic Pricing** | Three tiers (Essential / Signature / Royal Prestige) priced from real-world spend data |
| ☁️ **Live Weather** | Real-time conditions via Open-Meteo with contextual activity and clothing tips |
| 🗺️ **Interactive Map** | Leaflet-powered map with gold destination pins and grey attraction markers |
| 🤖 **AI Chat** | Ask follow-up questions — the AI knows your destination, culture, safety, and food data |
| 📅 **Calendar Export** | One-click Google Calendar integration or `.ics` download for Apple Calendar |

### Layer 2 — Travel Intelligence Dashboard

Accessible from the **Travel Intel** tab — these 11 widgets turn raw data into actionable travel awareness:

| Widget | Data Source | What You Get |
| --- | --- | --- |
| 🕐 **Local Time** | IANA Timezone DB | Live clock synced to destination |
| 🌬️ **Air Quality** | Open-Meteo AQI API | Real-time US AQI with Good/Fair/Poor label |
| 💱 **Currency Converter** | Frankfurter API | Live USD → Local currency with editable amount |
| 📆 **Best Time to Visit** | Curated DB | Optimal months + seasonal travel advice |
| 💵 **Daily Spend** | Curated DB | Budget / Mid-Range / Luxury per-day estimates |
| ⚠️ **Scam Encyclopedia** | Curated DB | Country-specific scams with avoidance tactics |
| 📱 **Must-Download Apps** | Curated DB | Essential local apps with use-case descriptions |
| 🚨 **Emergency Numbers** | Curated DB | Police, ambulance, fire, tourist helpline |
| 🔌 **Power & Water** | Curated DB | Plug type, voltage, tap water safety |
| 📡 **SIM Card Guide** | Curated DB | Local SIM recommendations and connectivity tips |
| 💬 **Traveler Tips** | Curated DB | Auto-rotating carousel of cultural and logistical tips |

### Layer 3 — Local Culture Guide

| Feature | What It Covers |
| --- | --- |
| 🏛️ **Must-Visit Attractions** | Real POIs from OpenStreetMap with categories and descriptions |
| 🗣️ **Language Basics** | Key phrases, greeting customs, communication tips |
| 🍜 **Food Scene** | Signature dishes, street food recommendations, dining etiquette |
| 🛡️ **Safety Advisory** | Area-specific safety notes and common precautions |
| 🎭 **Cultural Protocol** | Tipping norms, dress codes, religious site etiquette |
| 🧳 **Smart Packing List** | Weather-adaptive — switches between cold gear, sun protection, and layers |

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                          BROWSER                                 │
│                                                                  │
│   index.html ──▶ script.js ──▶ style.css                        │
│                     │                                            │
│          ┌──────────┼──────────┬────────────┐                    │
│          ▼          ▼          ▼            ▼                    │
│     ┌─────────┐ ┌────────┐ ┌────────┐ ┌─────────┐              │
│     │Globe.gl │ │Leaflet │ │  i18n  │ │AI Chat  │              │
│     │3D Globe │ │Map View│ │4 Langs │ │Sidebar  │              │
│     └─────────┘ └────────┘ └────────┘ └─────────┘              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP (fetch)
            ┌──────────────▼────────────────┐
            │      Flask REST API           │
            │       api/index.py            │
            │                               │
            │  ┌─────────────────────────┐  │
            │  │  9 Intelligence DBs     │  │
            │  │  Dynamic Pricing Engine │  │
            │  │  Interest-Based Ranker  │  │
            │  │  Itinerary Generator    │  │
            │  └─────────────────────────┘  │
            └──┬──────────┬──────────┬──────┘
               │          │          │
     ┌─────────▼───┐ ┌───▼────────┐ ┌▼────────────┐
     │  Open-Meteo │ │  Overpass  │ │ Frankfurter │
     │Weather, Geo │ │ OSM Places │ │  Currency   │
     │  & AQI      │ │            │ │  Exchange   │
     └─────────────┘ └────────────┘ └─────────────┘
```

---

## 🌍 Global Coverage

<table>
  <tr>
    <td><strong>🇪🇺 Europe</strong></td>
    <td>Italy · France · UK · Germany · Spain · Greece · Netherlands · Turkey · Norway · Sweden · Denmark · Poland · Czech Republic · Hungary · Austria</td>
  </tr>
  <tr>
    <td><strong>🌎 Americas</strong></td>
    <td>USA · Canada · Mexico · Brazil · Argentina · Chile · Peru · Colombia</td>
  </tr>
  <tr>
    <td><strong>🌏 Asia & Pacific</strong></td>
    <td>Japan · China · South Korea · Thailand · India · Vietnam · Singapore · Australia · New Zealand · Taiwan</td>
  </tr>
  <tr>
    <td><strong>🌍 Middle East & Africa</strong></td>
    <td>UAE · Saudi Arabia · Egypt · Kenya · South Africa · Morocco</td>
  </tr>
</table>

> **Fallback Coverage:** For unlisted destinations, Dora generates contextual guidance from geocoding and weather data — every city on Earth is supported at the basic level.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| --- | --- |
| **Frontend** | HTML5 · Vanilla CSS · JavaScript ES6+ · Three.js · Globe.gl · Leaflet.js · Font Awesome 6 · Google Fonts |
| **Backend** | Python 3.8+ · Flask 2.2 · Flask-CORS · Requests |
| **APIs** | Open-Meteo (Weather + Geocoding + AQI) · Overpass/OSM · Frankfurter (Currency) |
| **Databases** | 9 curated Python dictionaries covering culture, scams, apps, emergency, utilities, spend, tips, timezone, best-time |
| **Deployment** | Vercel (zero-config serverless with Python runtime) |

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/narwal4421/dora-travel-agency.git
cd dora-travel-agency

# 2. Install
pip install -r requirements.txt

# 3. Run backend
cd api && python index.py
# API starts at http://127.0.0.1:5000

# 4. Run frontend (separate terminal)
cd .. && python -m http.server 8080
# Open http://localhost:8080
```

> The frontend auto-detects `localhost` and routes API requests accordingly. No `.env` file or API keys required.

---

## 📡 API Reference

### `POST /api/plan-trip`

Generate a complete travel intelligence report.

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

**Returns:** Packages (3 tiers), itinerary (day-by-day), local guide, and full intel object (11 widgets).

### `GET /api/weather?dest=Tokyo`

Real-time weather with contextual travel tips.

### `POST /api/chat`

Context-aware AI travel assistant. Receives `message` and `context` (trip data).

---

## 📊 Project Stats

| Metric | Value |
| --- | --- |
| **Total Lines of Code** | ~1,700+ |
| **Intelligence Databases** | 9 curated datasets |
| **Countries Covered** | 40+ with full intelligence |
| **API Integrations** | 5 real-time external APIs |
| **UI Languages** | 4 (EN, HI, ES, FR) |
| **Travel Packages** | 3 dynamic tiers per destination |
| **Intel Widgets** | 11 real-time dashboard components |

---

## 🗺️ Roadmap

- [x] Cinematic 3D globe with flight arc animations
- [x] AI-powered interest-ranked itineraries
- [x] Three-tier dynamic pricing engine
- [x] Live weather with contextual packing tips
- [x] Interactive Leaflet map with attraction markers
- [x] AI Chat Assistant with destination context
- [x] Google Calendar & Apple .ics export
- [x] 11-widget Travel Intelligence dashboard
- [x] Multi-language UI (English, Hindi, Spanish, French)
- [x] 40+ country curated intelligence database
- [ ] PDF itinerary export with branded design
- [ ] Deep-link hotel & flight booking integration
- [ ] User accounts with saved trips & wishlists
- [ ] Real-time collaborative trip planning
- [ ] Mobile-native app (React Native)

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss proposed changes. PRs should target the `main` branch.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://github.com/narwal4421">Pranjal</a></strong>
  <br/>
  <sub>Travel Intelligence Engine v2.0 — Flask · Three.js · Leaflet · Open Geospatial Data</sub>
  <br/><br/>
  <a href="https://github.com/narwal4421/dora-travel-agency">
    <img src="https://img.shields.io/badge/⭐_Star_this_repo-If_you_found_it_useful-d4af37?style=for-the-badge" alt="Star this repo" />
  </a>
</p>
   
 