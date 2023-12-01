import React, {useState, useEffect} from 'react';
const API_BASE_URL = 'http://localhost:5000';

function UserWorkspaces() {
    const [workspaces, setWorkspaces] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`${API_BASE_URL}/get_workspaces`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setWorkspaces(data["workspaces"]);
            })
            .catch(error => {
                setError(error.message);
            });
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>User Workspaces</h1>
            {workspaces.length > 0 ? (
                <ul>
                    {workspaces.map(workspace => (
                        <li key={workspace.id}>{workspace.title}</li> // Assuming workspace object has id and name
                    ))}
                </ul>
            ) : (
                <p>No workspaces found.</p>
            )}
        </div>
    );
}

export default UserWorkspaces;
