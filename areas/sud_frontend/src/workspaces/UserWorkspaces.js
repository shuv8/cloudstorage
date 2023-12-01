import React, {useState, useEffect} from 'react';
import './UserWorkspaces.css';

const API_BASE_URL = 'http://localhost:5000';

function UserWorkspaces() {
    const [workspace, setWorkspace] = useState("");
    const [workspaces, setWorkspaces] = useState([]);
    const [username, setUsername] = useState("Anonim");
    const [error, setError] = useState(null);
    const STATUS_MAP = {
        1: 'Активно', 2: 'В архиве', 3: 'Удалено'
    };

    const R_STATUS_MAP = {
        1: 'Открыт', 2: 'В ревью', 3: 'Принят', 4: 'Отклонён', 5: 'Закрыт',
    };

    const handleWorkspaceClick = (workspaceId) => {
        fetch(`${API_BASE_URL}/get_workspace/${workspaceId}`, {
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
                setWorkspace(data);
            })
            .catch(error => {
                setError(error.message);
            });
    };

    useEffect(() => {
        fetch(`${API_BASE_URL}/get_workspaces`, {
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
            })
            .catch(error => {
                setError(error.message);
            });
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (<div className="workspaces-container">
        <div className="workspace-title-container">
            <h2 className="workspace-title">Рабочие пространства</h2>
            <div className="username-info-right">
                <div className="username" onClick={() => goToProfile()}>
                    <p className="request-content">{username}</p>
                </div>
            </div>
        </div>

        <div className="workspace-block">
            <div className="all-workspaces">
                {workspaces.length > 0 ? (<ul className="all-workspaces-container">
                    {workspaces.map(workspace => (
                        <li onClick={() => handleWorkspaceClick(workspace.id)} className="workspace-item"
                            key={workspace.id}>{workspace.title}</li>))}
                </ul>) : (<p>No workspaces found.</p>)}
            </div>


            <div className="all-files-branches">
                {workspace !== "" ? (<div>
                    <div className="request-content-title-container">
                        <div>
                            <h3 className="request-content-title">{workspace.title}</h3>
                            <p className="request-content">{workspace.description}</p>
                        </div>
                        <div className="info-right">
                            <div className="branches-number">
                                <p><b>Ветки:</b> {workspace.branches_num}</p>
                            </div>

                            <div className="workspace-status"
                                 style={{backgroundColor: getStatusColor(workspace.status)}}>
                                <p>{STATUS_MAP[workspace.status] || 'Неизвестно'}</p>
                            </div>
                        </div>
                    </div>

                    <h3>Все ветки</h3>
                    <div className="all-branches">
                        {workspace.branches.length > 0 ? (<ul className="all-branches-container">
                            {workspace.branches.map(branch => (<li className="branch-item" key={branch.id}>
                                {branch.id === workspace.main_branch &&
                                    <span><b>🏠</b> </span>}{branch.name}
                            </li>))}
                        </ul>) : (<p>Нет веток</p>)}
                    </div>

                    <h3>Все реквесты</h3>
                    <div className="all-request">
                        {workspace.requests.length > 0 ? (<ul className="all-requests-container">
                            {workspace.requests.map(request => (
                                <li className="request-item" key={request.id}>
                                    <div>{request.title}</div>
                                    <div>{request.description}</div>
                                    <div>Статус: {R_STATUS_MAP[workspace.status] || 'Неизвестный статус'}</div>
                                </li>))}
                        </ul>) : (<p>Нет реквестов.</p>)}
                    </div>
                </div>) : (<p>Нажмите на рабочее пространство для просмотра</p>)}
            </div>
        </div>

    </div>);
}

function getStatusColor(status) {
    const statusColors = {
        1: 'green',
        2: 'gray',
        3: 'red'
    };

    return statusColors[status] || 'white'; // Set your default color here.
}

function goToProfile() {
    window.location.href = '/me';
}

export default UserWorkspaces;
