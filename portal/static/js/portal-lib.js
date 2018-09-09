/**
 * Flashes a message to the user.
 * 
 * @param {string} message - the message to be flashed
 * @param {boolean} error - should be set to true if the message is an error
 */
function flash(message, error) {
    // TODO: don't use alerts, flash a pretty box to the user
    if(error) {
        alert('Error:' + message);
    } else {
        alert(message);
    }
}

/**
 * Performs an AJAX query and passes the response to a callback.
 * 
 * @param {string} endpoint - the endpoint to which the AJAX request will be
 * sent
 * @param {string} body - the body of the AJAX request
 * @param {function} callback - the function that will be called to handle the
 * response data
 */
function post(endpoint, body, callback) {
    let xhr = XMLHttpRequest();
    xhr.open('POST', endpoint);
    xhr.onload = callback;
    xhr.send(body);
}