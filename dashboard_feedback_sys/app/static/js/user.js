async function submitReview() {
    const rating = document.getElementById("rating").value;
    const review = document.getElementById("review").value;

    document.getElementById("status").innerText = "Submitting...";
    document.getElementById("ai-response").innerText = "";

    try {
        const response = await fetch("/api/review", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                rating: Number(rating),
                review: review
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Submission failed");
        }

        document.getElementById("status").innerText = "Submitted successfully!";
        document.getElementById("ai-response").innerText =
            "Thank you! Your feedback has been processed.";

    } catch (err) {
        document.getElementById("status").innerText = err.message;
    }
}
