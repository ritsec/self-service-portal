window.onload = function() {
    document.getElementById('register').addEventListener('submit',
    function(event) {
        event.preventDefault();
        if (passwordsMatch(event.target)) {
            post(
                '/account/register',
                serializeForm(event.target),
                checkResponse
            );
        } else {
            flash('Passwords must match!', true);
        }
    }, false);
}