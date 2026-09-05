const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        console.log("Login attempt:", {
            email,
            password
        });

        alert("Frontend login form works. Backend integration comes next.");
    });
}

if (registerForm) {
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const fullname = document.getElementById("fullname").value;
        const email = document.getElementById("email").value;
        const role = document.getElementById("role").value;
        const location = document.getElementById("location").value;
        const password = document.getElementById("password").value;
        const confirmPassword =
            document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        console.log("Registration:", {
            fullname,
            email,
            role,
            location
        });

        alert("Registration frontend works. Backend integration comes next.");
    });
}