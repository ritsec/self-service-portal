/**
 * Checks a form element to make sure the password and confirm password fields
 * match each other.  This check is performed by checking if the values of the
 * child element with ID "password" matches the value of the child element with
 * ID "confirm-password".  If one of these child elements does not exist, or if
 * their contents do not match, this function returns false.  Otherwise, it
 * returns true.
 * 
 * @param {HTMLElement} formElement - the form whose password fields should be
 * checked
 */
function passwordsMatch(formElement) {
    let password = formElement.querySelector('#password');
    let confirm = formElement.querySelector('#password');
    if (password instanceof HTMLElement && confirm instanceof HTMLElement && 
        password.value === confirm.value) {
            return true;
    } else {
        return false;
    }
}

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
 * process "text", "password", and "hidden" input types.  Additionally, it will
 * not process unnamed inputs, because they would normally not be submitted.
 * 
 * @param {HTMLElement} formElement - The form element to serialize the
 * contents of
 */
function serializeForm(formElement) {
    let formValues = '';
    let VALID_TYPES = ['text', 'password', 'hidden'];
    for (let idx = 0, element; element = formElement.elements[idx++];) {
        if (element.name !== '' && VALID_TYPES.indexOf(element.type) > -1) {
            formValues += element.name + '=' + element.value + '&';
        }
    }
    // Remove trailing ampersand and encode properly
    formValues = formValues.substring(0, formValues.length - 1);
    // return encodeURIComponent(formValues);
    return formValues;
}

/**
 * Callback function for POST requests.  Checks the status code of the response
 * to determine the kind of message to flash, and then flashes it.  Requires
 * JSON responses with a 'status' attribute containing the message to be
 * flashed.  Also, if there is any sort of error, a 400 response should be
 * returned.
 */
function checkResponse() {
    response = JSON.parse(this.response);
    if (this.status == 200) {
        flash(response.status);
    } else {
        flash(response.status, true);
    }
}