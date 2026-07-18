// RESTful API Fetch Client Wrapper

const API = {
    async request(url, options = {}) {
        // Ensure credentials are sent with requests for cookies session sharing
        options.credentials = 'same-origin';
        
        // Setup default headers if not uploading files (multipart)
        if (!options.headers) {
            options.headers = {};
        }
        
        if (!(options.body instanceof FormData) && !options.headers['Content-Type']) {
            options.headers['Content-Type'] = 'application/json';
        }
        
        try {
            const response = await fetch(url, options);
            const data = await response.json().catch(() => ({}));
            
            if (!response.ok) {
                // If unauthorized and not on login page, redirect to login
                if (response.status === 401 && !window.location.pathname.includes('/login')) {
                    // Let the page handle redirect if it wants, or handle here
                    window.location.href = `/login?next=${encodeURIComponent(window.location.pathname)}`;
                    return { error: 'Unauthorized. Redirecting to login...' };
                }
                
                return { 
                    error: data.error || `HTTP error! Status: ${response.status}`,
                    status: response.status 
                };
            }
            
            return { data, status: response.status };
        } catch (err) {
            console.error('API Fetch Error:', err);
            return { error: 'Network error or connection lost. Please try again.' };
        }
    },
    
    async get(url) {
        return this.request(url, { method: 'GET' });
    },
    
    async post(url, body) {
        return this.request(url, {
            method: 'POST',
            body: typeof body === 'object' && !(body instanceof FormData) ? JSON.stringify(body) : body
        });
    },
    
    async put(url, body) {
        return this.request(url, {
            method: 'PUT',
            body: typeof body === 'object' && !(body instanceof FormData) ? JSON.stringify(body) : body
        });
    },
    
    async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
};

window.API = API;
