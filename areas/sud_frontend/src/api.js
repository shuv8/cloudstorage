const API_BASE_URL = 'http://localhost:5000';

export async function loginUser(credentials) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(credentials), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }


    return response.status;
}

export async function registerUser(credentials) {
    const response = await fetch(`${API_BASE_URL}/registration`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(credentials), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }


    return response.status;
}


export async function add_workspace(content) {
    const response = await fetch(`${API_BASE_URL}/workspace/add`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(content), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Adding failed');
    }


    return response.status;
}

export async function archive_workspace(id) {
    const response = await fetch(`${API_BASE_URL}/workspace/${id}/archive`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(id), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Archiving failed');
    }


    return response.status;
}

export async function add_request(content, id) {
    const response = await fetch(`${API_BASE_URL}/workspace/${id}/request`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(content), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Adding failed');
    }


    return response.status;
}
