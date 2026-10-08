document.addEventListener("DOMContentLoaded", () => {
    // 1. Tab / Slide Switching Logic
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const target = document.getElementById(btn.getAttribute("data-tab"));
            if (target) target.classList.add("active");
        });
    });

    // 2. Crop market pricing benchmark (INR/Tonne)
    const cropPrices = {
        "Rice": 22000,
        "Wheat": 23800,
        "Maize": 21000,
        "Sugarcane": 3500,
        "Cotton": 68000,
        "Chilli": 103000,
        "Pulses": 71500,
        "Groundnut": 56000
    };

    // 3. Form Prediction & Dynamic Economic Update
    const form = document.getElementById("prediction-form");
    const submitBtn = document.getElementById("submit-btn");
    const yieldValue = document.getElementById("yield-value");
    const productionValue = document.getElementById("production-value");
    const recommendationsList = document.getElementById("recommendations-list");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        submitBtn.querySelector("span").textContent = "Processing...";
        submitBtn.disabled = true;

        const crop = document.getElementById("crop").value;
        const season = document.getElementById("season").value;
        const area = parseFloat(document.getElementById("farm_area").value) || 1.0;

        const payload = {
            crop: crop,
            season: season,
            irrigation_method: document.getElementById("irrigation_method").value,
            farm_area: area
        };

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                yieldValue.textContent = data.yield.toFixed(2);
                productionValue.textContent = data.total_production.toFixed(1);

                // Update Slide 2 (Economics) based on new prediction
                const pricePerTonne = cropPrices[crop] || 25000;
                const grossRevenue = Math.round(data.total_production * pricePerTonne);
                const estimatedCost = Math.round(area * 35000); // estimated ₹35,000 cost/ha
                const netProfit = grossRevenue - estimatedCost;

                document.getElementById("econ-price").textContent = "₹" + pricePerTonne.toLocaleString("en-IN");
                document.getElementById("econ-revenue").textContent = "₹" + grossRevenue.toLocaleString("en-IN");
                document.getElementById("econ-profit").textContent = (netProfit >= 0 ? "₹" : "-₹") + Math.abs(netProfit).toLocaleString("en-IN");

                // Populate farmer recommendations
                recommendationsList.innerHTML = "";
                data.recommendations.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = item;
                    recommendationsList.appendChild(li);
                });
            }
        } catch (err) {
            console.error(err);
            alert("Error connecting to server.");
        } finally {
            submitBtn.querySelector("span").textContent = "Generate Forecast";
            submitBtn.disabled = false;
        }
    });
});
