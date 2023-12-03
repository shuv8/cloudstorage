import React, {useEffect, useState} from 'react';
import './Admin.css';

const API_BASE_URL = 'http://localhost:5000';


function Admin() {
    const [workspaces, setWorkspaces] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [users, setUsers] = useState([]);
    const [error, setError] = useState(null);

    const [username, setUsername] = useState("Аноним");

    useEffect(() => {
        fetch(`${API_BASE_URL}/all_workspaces`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
            }, credentials: 'include',
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

    useEffect(() => {
        fetch(`${API_BASE_URL}/department`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
            }, credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setDepartments(data["departments"]);
            })
            .catch(error => {
                setError(error.message);
            });
    }, []);

    useEffect(() => {
        fetch(`${API_BASE_URL}/user`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
            }, credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setUsers(data["users"]);
            })
            .catch(error => {
                setError(error.message);
            });
    }, []);

    useEffect(() => {
        fetch(`${API_BASE_URL}/whoiam`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
            }, credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setUsername(data["username"]);
            });
    }, []);

    return (
        <div className="page">
            <div className="workspaces-container">

                {/*/ ЗАГОЛОВОК /*/}

                <div className="workspace-title-container">
                    <h2 className="workspace-title"><span
                        onClick={() => goHome()}
                        style={{cursor: "pointer"}}
                    >🏠</span>Рабочие пространства</h2>
                    <div className="username-info-right">
                        <div className="username" onClick={() => goToProfile()}>
                            <p className="request-content">{username}</p>
                        </div>
                    </div>
                </div>

                <div className="workspace-block">

                    {/*/ ВСЕ ПРОСТРАНСТВА /*/}

                    <div className="all-workspaces">
                        <div>
                            {workspaces != null && workspaces.length > 0 ? (<ul className="all-workspaces-container">
                                {workspaces.map(workspace => (
                                    <li onClick={() => {}} className="workspace-item"
                                        key={workspace.id}>{workspace.title}</li>))}
                            </ul>) : (<p className="workspace-item-p">Не найдено рабочих пространств</p>)}
                        </div>
                    </div>

                    {/*/ ОТДЕЛЫ /*/}

                    <div className="all-workspaces">
                        <div>
                            {departments != null && departments.length > 0 ? (<ul className="all-workspaces-container">
                                {departments.map(department => (
                                    <li onClick={() => {}} className="workspace-item">{department.department_name}</li>))}
                            </ul>) : (<p className="workspace-item-p">Не найдено отделов</p>)}
                        </div>
                    </div>

                    {/*/ ЮЗВЕРЫ /*/}

                    <div className="all-workspaces">
                        <div>
                            {users != null && users.length > 0 ? (<ul className="all-workspaces-container">
                                {users.map(user => (
                                    <li className="workspace-item" key={user.id}>{user.username}</li>))}
                            </ul>) : (<p className="workspace-item-p">Не найдено пользователей</p>)}
                        </div>
                    </div>
                </div>
            </div>
        </div>);
}

function goHome() {
    window.location.href = '/workspaces';
}

function goToProfile() {
    window.location.href = '/me';
}


export default Admin;