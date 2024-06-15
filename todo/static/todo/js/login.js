document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("login-form");
    const errorContainer = document.getElementById("error-container");
    const inputs = form.querySelectorAll("input[type=text], input[type=password]");

    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            // Clear the specific field's error messages on focus
            clearErrorMessages();
        });
    });

    function clearErrorMessages() {
        const errorMessages = errorContainer.querySelectorAll(".error_message");
        errorMessages.forEach(error => error.remove());
    }
});