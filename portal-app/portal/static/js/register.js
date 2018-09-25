window.onload = function() {
    document.getElementById('register').addEventListener('submit',
    function(event) {
        event.preventDefault();
        let matched = passwordsMatch(event.target);
        let valid = validPassword(event.target);
        if (matched && valid) {
            post(
                '/account/register',
                serializeForm(event.target),
                checkResponse
            );
        } else if (valid) {
            flash('Passwords must match!', true);
        } else {
            flash('Password must be at least 8 characters long.', true);
        }
    }, false);
}