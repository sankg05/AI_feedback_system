async function fetchReviews() {
    try {
        const response = await fetch("/api/admin/reviews");
        const data = await response.json();

        const tableBody = document.querySelector("#reviews-table tbody");
        tableBody.innerHTML = "";

        data.reviews.forEach(review => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${review.id}</td>
                <td>${review.rating}</td>
                <td>${review.review_text}</td>
                <td>${review.ai_summary || "-"}</td>
                <td>${review.ai_recommended_actions || "-"}</td>
                <td>${review.status}</td>
            `;

            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error("Failed to fetch admin reviews:", error);
    }
}

// Initial load
fetchReviews();

// Auto-refresh every 10 seconds
setInterval(fetchReviews, 10000);
