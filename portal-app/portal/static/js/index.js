/*
Submit a form containing an email address, and verify that the email associated
with the form was sent successfully.
*/
function emailFormSubmit(event) {
    event.preventDefault();
    post(
        '/email',
        serializeForm(event.target),
        checkResponse
    );
}

window.onload = function() {
    // Registration form submission
    document.getElementById('account_register').addEventListener('submit', emailFormSubmit, false);
    
    // Password reset form submission
    document.getElementById('account_change-password').addEventListener('submit', emailFormSubmit, false);
}