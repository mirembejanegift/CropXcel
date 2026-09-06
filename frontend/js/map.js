document.addEventListener('DOMContentLoaded', function () {

    const map = L.map('map').setView([1.3733, 32.2903], 7);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    setTimeout(function () {
        map.invalidateSize();
    }, 200);

    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    let currentCentroid = null;
    let currentFarmProfile = null;
    let selectedCrop = null;

    const analyseBtn = document.getElementById('analyseBtn');
    const analyseSpinner = document.getElementById('analyseSpinner');
    const analyseStatus = document.getElementById('analyseStatus');
    const cropResultsCard = document.getElementById('cropResultsCard');
    const cropResultsList = document.getElementById('cropResultsList');
    const generatePlanBtn = document.getElementById('generatePlanBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const userGreeting = document.getElementById('userGreeting');

    async function loadCurrentUser() {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/current-user", {
                credentials: "include"
            });
            const result = await response.json();

            if (result.success) {
                userGreeting.textContent = `Welcome, ${result.user.name}`;
            } else {
                window.location.href = "login.html";
            }
        } catch (err) {
            console.error("Could not load current user:", err);
        }
    }

    loadCurrentUser();

    logoutBtn.addEventListener('click', async function () {
        try {
            await fetch("http://127.0.0.1:5000/api/logout", {
                method: "POST",
                credentials: "include"
            });
            window.location.href = "login.html";
        } catch (err) {
            console.error("Logout error:", err);
            alert("Could not log out. Please try again.");
        }
    });

    function drawAutoBoundary(lat, lon) {
        drawnItems.clearLayers();

        const offset = 0.0015;

        const squarePoints = [
            [lat + offset, lon - offset],
            [lat + offset, lon + offset],
            [lat - offset, lon + offset],
            [lat - offset, lon - offset]
        ];

        const polygon = L.polygon(squarePoints, {
            color: '#1b5e20',
            fillOpacity: 0.3
        }).addTo(drawnItems);

        map.fitBounds(polygon.getBounds(), { maxZoom: 16 });
    }

    function fillProfileCard(farmProfile) {
        const soil = farmProfile.soil;
        const weather = farmProfile.weather;

        document.getElementById('val-ph').textContent = soil.ph;
        document.getElementById('val-nitrogen').textContent = `${soil.nitrogen_total.value} ${soil.nitrogen_total.unit}`;
        document.getElementById('val-phosphorus').textContent = `${soil.phosphorous_extractable.value} ${soil.phosphorous_extractable.unit}`;
        document.getElementById('val-potassium').textContent = `${soil.potassium_extractable.value} ${soil.potassium_extractable.unit}`;
        document.getElementById('val-temperature').textContent = `${weather.temperature} °C`;
        document.getElementById('val-humidity').textContent = `${weather.humidity} %`;
        document.getElementById('val-rainfall').textContent = `${weather.rainfall_last_30_days} mm`;
    }

    function fillCropResults(topCrops) {
        cropResultsList.innerHTML = "";
        selectedCrop = null;
        generatePlanBtn.style.display = "none";
        document.getElementById('farmPlanCard').style.display = "none";

        topCrops.forEach(item => {
            const row = document.createElement('div');
            row.className = 'crop-card';
            row.dataset.crop = item.crop;
            row.innerHTML = `
                <span class="crop-name">${item.crop}</span>
                <span class="crop-score">${Math.round(item.score * 100)}%</span>
            `;

            row.addEventListener('click', function () {
                document.querySelectorAll('.crop-card').forEach(card => card.classList.remove('selected'));
                row.classList.add('selected');
                selectedCrop = item.crop;
                generatePlanBtn.style.display = "block";
            });

            cropResultsList.appendChild(row);
        });

        cropResultsCard.style.display = "block";
    }

    async function analyseFarm() {
        if (!currentCentroid) {
            analyseStatus.textContent = "Please search for your farm's location first.";
            return;
        }

        analyseBtn.disabled = true;
        analyseSpinner.style.display = "inline-block";
        analyseStatus.textContent = "Analysing your farm... please wait.";
        cropResultsCard.style.display = "none";

        try {
            const response = await fetch("http://127.0.0.1:5000/api/analyse-farm", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(currentCentroid)
            });

            const result = await response.json();

            if (!result.success) {
                analyseStatus.textContent = result.error || "Analysis failed. Please try again.";
                return;
            }

            fillProfileCard(result.farm_profile);
            currentFarmProfile = result.farm_profile;
            fillCropResults(result.top_crops);

            analyseStatus.textContent = "Analysis complete.";

        } catch (err) {
            console.error("Analyse farm error:", err);
            analyseStatus.textContent = "Could not reach the server. Is the backend running?";
        } finally {
            analyseBtn.disabled = false;
            analyseSpinner.style.display = "none";
        }
    }

    analyseBtn.addEventListener('click', analyseFarm);

    function fillFarmPlanCard(plan) {
        document.getElementById('plan-crop').textContent = plan.crop;
        document.getElementById('plan-status').textContent = plan.planting_status;
        document.getElementById('plan-guidance').textContent = plan.guidance;
        document.getElementById('plan-harvest').textContent = plan.expected_harvest_range;
        document.getElementById('farmPlanCard').style.display = "block";
        document.getElementById('farmPlanCard').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    async function generateFarmPlan() {
        if (!selectedCrop || !currentFarmProfile) {
            alert("Please analyse your farm and select a crop first.");
            return;
        }

        generatePlanBtn.disabled = true;
        generatePlanBtn.textContent = "Generating...";

        try {
            const response = await fetch("http://127.0.0.1:5000/api/generate-plan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    crop: selectedCrop,
                    farm_profile: currentFarmProfile
                })
            });

            const result = await response.json();

            if (!result.success) {
                alert(result.error || "Could not generate farm plan.");
                return;
            }

            fillFarmPlanCard(result.farm_plan);

        } catch (err) {
            console.error("Generate plan error:", err);
            alert("Could not reach the server. Is the backend running?");
        } finally {
            generatePlanBtn.disabled = false;
            generatePlanBtn.textContent = "Generate Farm Plan";
        }
    }

    generatePlanBtn.addEventListener('click', generateFarmPlan);

    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('locationSearch');

    async function searchLocation() {
        const query = searchInput.value.trim();
        if (!query) return;

        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&countrycodes=ug&limit=1`
            );
            const results = await response.json();

            if (results.length === 0) {
                alert("Location not found. Try a different search term.");
                return;
            }

            const { lat, lon } = results[0];
            const latitude = parseFloat(lat);
            const longitude = parseFloat(lon);

            currentCentroid = { latitude, longitude };
            drawAutoBoundary(latitude, longitude);

            analyseStatus.textContent = 'Location found. Click "Analyse Farm" to continue.';

        } catch (err) {
            console.error("Search error:", err);
            alert("Something went wrong searching for that location.");
        }
    }

    searchBtn.addEventListener('click', searchLocation);
    searchInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            searchLocation();
        }
    });

});