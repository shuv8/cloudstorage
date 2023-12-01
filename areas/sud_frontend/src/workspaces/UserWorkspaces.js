import React, {useState, useEffect} from 'react';
import './UserWorkspaces.css';

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
        <div className="workspaces-container">
            <h2>Рабочие пространства</h2>
            {workspaces.length > 0 ? (
                <ul className="all-workspaces-container">
                    {workspaces.map(workspace => (
                        <li className="workspace-item" key={workspace.id}>{workspace.title}</li> // Assuming workspace object has id and name
                    ))}
                </ul>
            ) : (
                <p>No workspaces found.</p>
            )}
        </div>
    );
}

export default UserWorkspaces;
