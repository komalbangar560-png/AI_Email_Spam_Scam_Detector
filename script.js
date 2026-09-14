async function checkEmail() {
    const emailText = document.getElementById("emailText").value;
    const result = document.getElementById("result");

    if (emailText.trim() === "") {
        result.innerText = "Please enter an email.";
        return;
    }

    result.innerText = "Checking email...";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: emailText
            })
        });

        const data = await response.json();

        result.innerText = "Result: " + data.prediction;
    } catch (error) {
        result.innerText = "Unable to connect to the backend.";
    }
}