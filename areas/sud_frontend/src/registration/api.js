const API_BASE_URL = 'http://localhost:5000';

export async function RegisterUser(credentials) {
    const response = await fetch(`${API_BASE_URL}/registration`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
        credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }



    return response.status;
}