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

export async function add_department(content) {
    const response = await fetch(`${API_BASE_URL}/department`, {
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

export async function add_branch(content, id) {
    const response = await fetch(`${API_BASE_URL}/workspace/${id}/add_branch`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(content), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Adding failed');
    }
    else {
        let json = await response.json();
        return [json, response.status];
    }

}

export async function delete_branch(space_id, branch_id) {
    const response = await fetch(`${API_BASE_URL}/workspace/${space_id}/branch/${branch_id}`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(branch_id), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Deletion failed');
    }


    return response.status;
}

export async function add_url_access(space_id) {
    const response = await fetch(`${API_BASE_URL}/accesses/${space_id}/url?view_only=true`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Url adding error');
    }


    return response.status;
}


export async function delete_url_access(space_id) {
    const response = await fetch(`${API_BASE_URL}/accesses/${space_id}/url?view_only=true`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Url deleting error');
    }


    return response.status;
}

export async function add_department_access(space_id, department) {
    const response = await fetch(`${API_BASE_URL}/accesses/${space_id}/department/${department}?view_only=true`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Department adding error');
    }

    return response.status;
}

export async function delete_department_access(space_id, department) {
    const response = await fetch(`${API_BASE_URL}/accesses/${space_id}/department/${department}?view_only=true`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Department deleting error');
    }

    return response.status;
}


export async function add_email_access(space_id, email) {
    const response = await fetch(`${API_BASE_URL}/accesses/${space_id}/email/${email}?view_only=true`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Email adding error');
    }

    return response.status;
}

export async function delete_email_access(space_id, email) {
    const response = await fetch(`${API_BASE_URL}/accesses/${space_id}/email/${email}?view_only=true`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Email deleting error');
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

export async function get_request(content, id) {
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
