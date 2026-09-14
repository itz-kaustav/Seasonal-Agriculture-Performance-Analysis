document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");
    const submitBtn = document.getElementById("submit-btn");
    const yieldValue = document.getElementById("yield-value");
    const productionValue = document.getElementById("production-value");
    const recommendationsList = document.getElementById("recommendations-list");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        submitBtn.querySelector("span").textContent = "Processing...";
        submitBtn.disabled = true;

        const payload = {
            crop: document.getElementById("crop").value,
            season: document.getElementById("season").value,
            irrigation_method: document.getElementById("irrigation_method").value,
            farm_area: parseFloat(document.getElementById("farm_area").value) || 1.0
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

               
                recommendationsList.innerHTML = "";
                const filteredInsights = data.recommendations.filter(
                    item => !item.toLowerCase().includes("predicted unit yield") &&
                            !item.toLowerCase().includes("estimated total harvest")
                );

                filteredInsights.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = item;
                    recommendationsList.appendChild(li);
                });
            } else {
                alert("Prediction Error: " + (data.error || "Unknown error"));
            }
        } catch (err) {
            console.error(err);
            alert("Failed to connect to the prediction server.");
        } finally {
            submitBtn.querySelector("span").textContent = "Generate Analysis";
            submitBtn.disabled = false;
        }
    });
});
