window.onload = function() {
    document.getElementById('change-password').addEventListener('submit',
    function(event) {
        event.preventDefault();
        if (passwordsMatch(event.target)) {
            post(
                '/account/change-password',
                serializeForm(event.target),
                checkResponse
            );
        } else {
            flash('Passwords must match!', true);
        }
    }, false);
}