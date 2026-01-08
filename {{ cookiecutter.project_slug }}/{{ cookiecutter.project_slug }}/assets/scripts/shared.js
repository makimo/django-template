// Shared utilities (e.g. CSRF token injector).

/**
 * Helper function to make fetch requests with Django CSRF token.
 *
 * Usage:
 *   const data = await apiRequest('/api/endpoint/');
 *   const result = await apiRequest('/api/endpoint/', {
 *     method: 'POST',
 *     body: JSON.stringify({ key: 'value' })
 *   });
 *
 * @param {string} url - The URL to fetch
 * @param {Object} options - Fetch options (method, body, headers, etc.)
 * @returns {Promise<any>} - Parsed JSON response
 */
export const apiRequest = async (url, options = {}) => {
    const token = document.body.querySelector('[name=csrfmiddlewaretoken]');
    const defaultHeaders = {
        'X-CSRFToken': token ? token.value : '',
        'Content-Type': 'application/json',
        ...options.headers
    };

    const response = await fetch(url, {
        ...options,
        headers: defaultHeaders
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
};
