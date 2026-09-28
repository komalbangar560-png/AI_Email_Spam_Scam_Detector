async function checkEmail() {
    const emailText = document.getElementById("emailText").value;
    const result = document.getElementById("result");

    if (emailText.trim() === "") {
        result.innerHTML = "Please enter an email message.";
        return;
    }

    result.innerHTML = "Checking email...";

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: emailText
            })
        });

        const data = await response.json();

        if (!response.ok) {
            result.innerHTML = data.error || "Something went wrong.";
            return;
        }

        result.innerHTML = `
            <p>Result: ${data.prediction}</p>
            <p>Confidence: ${data.confidence}%</p>
            <p>Risk Level: ${data.risk}</p>
            <p>Scam Score: ${data.scam_score}</p>
        `;

    } catch (error) {
        result.innerHTML = "Unable to connect to the backend.";
        console.error(error);
    }
}
