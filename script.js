// script.js - Application Logic for AI Travel Assistant

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
const API_BASE_URL = isLocal ? 'http://127.0.0.1:5000/api' : '/api';

document.addEventListener('DOMContentLoaded', () => {

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
        // A slight delay to allow smooth fade out/in
        setTimeout(() => searchView.classList.add('active'), 50);
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

        // Show 3D globe wrapper
        loadingOverlay.classList.remove('hidden');
        destReveal.classList.add('hidden');
        destName.textContent = destination;
        
        // Scene 1: Initialize Globe in 3D Space & Global Network Activity
        globeViz.innerHTML = '';
        const world = Globe()
            (globeViz)
            .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
            .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
            .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
            .backgroundColor('#000000')
            .atmosphereColor('#d4af37')
            .atmosphereAltitude(0.25);
            
        // Generate a random "Neural Network" of luxury flight paths fetching data globally
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
        world.controls().autoRotateSpeed = 4; // Fast rotation while searching
        world.controls().enableZoom = false;

        try {
            // Fetch Travel Plan
            const planResponse = await fetch(`${API_BASE_URL}/plan-trip`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ destination, days, budget, interests, flightOption, hotelChoice })
            });

            if (!planResponse.ok) throw new Error('Failed to generate trip');
            const planData = await planResponse.json();

            // Fetch Weather independently
            fetchWeather(destination);

            // Render Results behind the scenes
            renderResults(planData, budget);

            // Scene 2: Stop rotation, Add FX, Drop Pin, and Trigger Cinematic Zoom
            world.controls().autoRotate = false;
            
            // Generate nested ripples
            world.ringsData([
                { lat: planData.lat, lng: planData.lon, maxR: 4, speed: 2 },
                { lat: planData.lat, lng: planData.lon, maxR: 8, speed: 1.5 },
                { lat: planData.lat, lng: planData.lon, maxR: 15, speed: 1 }
            ])
            .ringColor(() => '#d4af37')
            .ringMaxRadius('maxR')
            .ringPropagationSpeed('speed')
            .ringRepeatPeriod(800);
            
            // Delete neural network, launch ONE massive glowing arc to the target
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
                    // Add a CSS pulsating animation to the pin
                    el.innerHTML = `
                      <div style="animation: bounce 1s infinite alternate; filter: drop-shadow(0 0 30px #e5c558);">
                          <i class="fa-solid fa-location-dot" style="color: #d4af37; font-size: 3.5rem;"></i>
                      </div>
                      <style>@keyframes bounce { 0% { transform: translateY(0); } 100% { transform: translateY(-20px); } }</style>
                    `;
                    return el;
                });
                
            world.pointOfView({ lat: planData.lat, lng: planData.lon, altitude: 0.04 }, 4500); // Extreme 4.5s cinematic zoom for precise location

            // Scene 3: Elegant Reveal
            setTimeout(() => {
                destReveal.classList.remove('hidden');
                
                // Final Scene: Crossfade to loaded dashboard
                setTimeout(() => {
                    loadingOverlay.classList.add('hidden');
                    searchView.classList.remove('active');
                    searchView.classList.add('hidden');
                    resultsView.classList.remove('hidden');
                    setTimeout(() => resultsView.classList.add('active'), 50);
                }, 3500); // Admire the typography for 3.5s
            }, 4000); // Starts smoothly near the end of the zoom

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
        wIcon.className = 'fa-solid fa-cloud-sun'; // default

        try {
            const resp = await fetch(`${API_BASE_URL}/weather?dest=${encodeURIComponent(destination)}`);
            if(!resp.ok) throw new Error('Weather fetch failed');
            
            const data = await resp.json();
            wTemp.textContent = `${data.temperature}°C`;
            wCond.textContent = data.condition;
            wTips.textContent = data.tips;
            generatePackingList(data.temperature);

            // Simple icon logic based on condition string
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

        // 1. Render Packages
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

        // Add event listeners to package buttons to switch to itinerary tab
        document.querySelectorAll('.select-pkg-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const pkgId = e.target.getAttribute('data-id');
                const selectedPkg = data.packages.find(p => p.id === pkgId);
                renderItinerary(selectedPkg.itinerary);
                // switch tab
                switchTab('itinerary');
            });
        });

        // Initially render itinerary for the preferred budget package
        const defaultPkg = data.packages.find(p => p.id === preferredBudget) || data.packages[0];
        renderItinerary(defaultPkg.itinerary);

        // 2. Render Must Visits
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

        // 3. Render Guides
        document.getElementById('guide-culture').textContent = data.localGuide.culture;
        document.getElementById('guide-food').textContent = data.localGuide.food;
        document.getElementById('guide-safety').textContent = data.localGuide.safety;
        document.getElementById('guide-language').textContent = data.localGuide.language;
        document.getElementById('guide-currency').textContent = data.localGuide.currency;
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

});
