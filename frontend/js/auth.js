const API_BASE = "http://127.0.0.1:5000";

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(`${API_BASE}/api/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();

            if (result.success) {
                window.location.href = "map.html";
            } else {
                alert(result.error || "Login failed. Please try again.");
            }
        } catch (err) {
            console.error("Login error:", err);
            alert("Could not reach the server. Is the backend running?");
        }
    });
}

if (registerForm) {
    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const fullname = document.getElementById("fullname").value;
        const email = document.getElementById("email").value;
        const role = document.getElementById("role").value;
        const location = document.getElementById("location").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/api/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ fullname, email, role, location, password })
            });

            const result = await response.json();

            if (result.success) {
                window.location.href = "map.html";
            } else {
                alert(result.error || "Registration failed. Please try again.");
            }
        } catch (err) {
            console.error("Registration error:", err);
            alert("Could not reach the server. Is the backend running?");
        }
    });
}