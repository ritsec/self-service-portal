/**
 * Flashes a message to the user.
 * 
 * @param {string} message - the message to be flashed
 * @param {boolean} error - should be set to true if the message is an error
 */
function flash(message, error) {
    // TODO: don't use alerts, flash a pretty box to the user
    if (error) {
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
    let xhr = new XMLHttpRequest();
    xhr.open('POST', endpoint);
    xhr.onload = callback;
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(body);
}

/**
 * Serializes the contents of an HTML form element in the format of the
 * application/x-www-form-urlencoded MIME type.  This function will only
 * process "text", "password", and "hidden" input types.
 * 
 * @param {HTMLElement} formElement - The form element to serialize the
 * contents of
 */
function serializeForm(formElement) {
    let formValues = ''
    for (let idx = 0, element; element = formElement.elements[idx++];) {
        if (element.type === 'text' || 
            element.type === 'password' ||
            element.type === 'hidden') {
            formValues += element.name + '=' + element.value + '&';
        }
    }
    // Remove trailing ampersand and encode properly
    formValues = formValues.substring(0, formValues.length - 1);
    // return encodeURIComponent(formValues);
    return formValues;
}