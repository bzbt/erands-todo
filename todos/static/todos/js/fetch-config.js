/**
 * Returns a configuration object for the fetch API.
 *
 * @param method - The HTTP method to use for the request.
 *
 * @returns {RequestInit}
 */
window.fetchConfig = function(method = 'POST') {
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        method: method,
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    }
};
