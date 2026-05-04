# Dora Travel Agency

**An intelligent, full-stack travel planning application powered by real-world geospatial APIs and a cinematic 3D globe experience.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Three.js](https://img.shields.io/badge/Three.js-Globe.gl-black?style=flat-square&logo=threedotjs&logoColor=white)](https://globe.gl/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[View Repository](https://github.com/narwal4421/dora-travel-agency) · [Report a Bug](https://github.com/narwal4421/dora-travel-agency/issues) · [Request a Feature](https://github.com/narwal4421/dora-travel-agency/issues)

---

## Overview

Dora Travel Agency is a full-stack web application that enables users to generate personalized travel itineraries in seconds. Users input a destination, trip duration, budget tier, and personal interests — the application then orchestrates multiple real-world APIs to produce a complete travel package: live weather data, real tourist attractions sourced from OpenStreetMap, curated cultural guides, and a day-by-day itinerary, all presented through a premium glassmorphism UI with a cinematic 3D globe loading experience.

---

## Features

| Feature | Description |
| Feature | Description |
| --- | --- |
| **Cinematic 3D Globe** | Interactive globe powered by Three.js and Globe.gl with animated flight paths, destination pin drop, and a dramatic cinematic zoom sequence |
| **AI Itinerary Generator** | Generates a full day-by-day travel itinerary tailored to destination, trip duration, and user interests |
| **3-Tier Travel Packages** | Budget, Balanced, and Luxury packages with estimated costs, accommodation tier, flight class, and transport recommendations |
| **Live Weather Widget** | Real-time weather conditions via Open-Meteo API with contextual travel tips based on temperature and forecast |
| **Local Culture Guide** | Language essentials, local currency, signature dishes, safety advisories, and cultural etiquette for 15+ countries |
| **Smart Packing List** | Dynamically generated packing checklist that adapts to destination weather conditions |
| **Real Attraction Data** | Live tourist attractions queried from OpenStreetMap's Overpass API using destination geocoordinates |
| **Dark / Light Mode** | Seamless theme switching with a fully responsive, glassmorphism-based design system |

---

## Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| HTML5 | Semantic application structure |
| Vanilla CSS | Custom design system — CSS variables, glassmorphism, animations |
| JavaScript (ES6+) | Async data fetching, DOM rendering, application state management |
| Three.js + Globe.gl | 3D interactive globe with arc animations, rings, and HTML pins |
| Font Awesome 6 | Icon library |
| Google Fonts (Playfair Display, Inter) | Premium typography |

### Backend

| Technology | Purpose |
|---|---|
| Python 3.8+ | Runtime |
| Flask 2.2 | REST API framework |
| Flask-CORS | Cross-origin request handling |
| Requests | HTTP client for external API integration |

### External APIs

| API | Usage | Authentication |
|---|---|---|
| [Open-Meteo](https://open-meteo.com/) | Real-time weather forecasts | None required |
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | City name → latitude/longitude resolution | None required |
| [Overpass API (OpenStreetMap)](https://overpass-api.de/) | Tourist attractions near destination coordinates | None required |

### Deployment

- **Vercel** — Serverless deployment with Python runtime via `vercel.json` API rewrites

---

## Project Structure

```text
dora-travel-agency/
├── index.html           # Single-page application shell (search view + results dashboard)
├── style.css            # Full design system — theming, glassmorphism, animations, layout
├── script.js            # Frontend logic — globe orchestration, API calls, UI rendering
├── index.py             # Flask REST API — /api/plan-trip, /api/weather endpoints
├── requirements.txt     # Python package dependencies
├── vercel.json          # Vercel serverless routing configuration
└── test_overpass.py     # Standalone script to validate Overpass API connectivity
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- A modern web browser (Chrome, Firefox, Edge)

### Installation

### 1. Clone the repository

```bash
git clone https://github.com/narwal4421/dora-travel-agency.git
cd dora-travel-agency
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend server

```bash
python index.py
```

The Flask API will be available at `http://127.0.0.1:5000`.

### 4. Open the frontend

Open `index.html` in your browser, or serve it with any static file server:

```bash
python -m http.server 8080
# Navigate to http://localhost:8080
```

> **Note:** The frontend automatically detects `localhost` and routes all API requests to `http://127.0.0.1:5000/api`. No additional configuration is required.

---

## Deployment

This project is preconfigured for **zero-configuration deployment on Vercel**.

1. Import the repository at [vercel.com/new](https://vercel.com/new)
2. Vercel automatically detects `vercel.json` and routes `/api/*` requests to the Python serverless function

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" }
  ]
}
```

> **Important:** For Vercel's Python runtime, the backend entry point must be located at `api/index.py`.

---

## API Reference

### `POST /api/plan-trip`

Generates a complete travel plan for a given destination.

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

**Response**

```json
{
  "destination": "Tokyo",
  "days": 5,
  "lat": 35.6762,
  "lon": 139.6503,
  "packages": [...],
  "mustVisits": [...],
  "localGuide": {
    "culture": "...",
    "food": "...",
    "safety": "...",
    "language": "...",
    "currency": "..."
  }
}
```

---

### `GET /api/weather`

Returns current weather conditions for a given city.

**Query Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `dest` | `string` | City name (e.g. `Tokyo`) |
| `lat` | `float` | Optional — latitude coordinate |
| `lon` | `float` | Optional — longitude coordinate |

**Response**

```json
{
  "temperature": 22,
  "condition": "Partly cloudy",
  "tips": "Perfect travel weather."
}
```

---

## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│  ┌───────────┐   ┌──────────────┐   ┌───────────────┐  │
│  │ index.html│   │  script.js   │   │   style.css   │  │
│  │  (Shell)  │──▶│ (App Logic)  │   │ (Design Sys.) │  │
│  └───────────┘   └──────┬───────┘   └───────────────┘  │
│                         │                               │
│              ┌──────────▼──────────┐                    │
│              │   Globe.gl / Three  │                    │
│              │  (3D Visualization) │                    │
│              └─────────────────────┘                    │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP
         ┌─────────────▼──────────────┐
         │      Flask REST API        │
         │        (index.py)          │
         └──┬─────────────────────┬───┘
            │                     │
  ┌─────────▼────────┐   ┌────────▼────────────────┐
  │   Open-Meteo     │   │  Overpass API           │
  │ (Weather + Geo)  │   │  (OpenStreetMap Places) │
  └──────────────────┘   └─────────────────────────┘
```

---

## Supported Destinations (Global Intelligence Hub)

The backend includes a curated, high-fidelity dataset for **40+ countries** with deep regional insights:

**Europe:** Italy · France · UK · Germany · Spain · Greece · Netherlands · Turkey · Norway · Sweden · Denmark · Poland · Czech Republic · Hungary · Austria  
**Americas:** USA · Canada · Mexico · Brazil · Argentina · Chile · Peru · Colombia  
**Asia/Pacific:** Japan · China · South Korea · Thailand · India · Vietnam · Singapore · Australia · New Zealand · Taiwan  
**Middle East & Africa:** UAE · Saudi Arabia · Egypt · Kenya · South Africa · Morocco

For all other destinations, the application falls back to generic contextual travel guidance derived from geocoding data.

---

## Roadmap

- [ ] PDF Export — Downloadable, styled itinerary document
- [ ] Interactive Map — Embedded live map with attraction markers and routing
- [ ] Live Booking Integration — Deep-link integration with hotel and flight providers
- [ ] AI Chat Companion — Natural language trip refinement interface
- [ ] Calendar Sync — Export itinerary directly to Google or Apple Calendar

---

## Contributing

Contributions are welcome. Please open an issue first to discuss any changes you wish to make. Pull requests should target the `main` branch.

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

*Built with Flask, Three.js, and open geospatial data.*
