import React, {useState, useEffect} from 'react';
import './UserWorkspaces.css';
import {add_workspace} from "../api";

const API_BASE_URL = 'http://localhost:5000';

function UserWorkspaces() {
    const [workspace, setWorkspace] = useState("");
    const [workspaces, setWorkspaces] = useState([]);
    const [workspaces_access, setWorkspaces_access] = useState([]);
    const [workspaces_open, setWorkspaces_open] = useState([]);
    const [username, setUsername] = useState("Anonim");
    const [error, setError] = useState(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const STATUS_MAP = {
        1: 'Активно', 2: 'В архиве', 3: 'Удалено'
    };

    const R_STATUS_MAP = {
        1: 'Открыт', 2: 'В ревью', 3: 'Принят', 4: 'Отклонён', 5: 'Закрыт',
    };

    const toggleDialog = () => {
        setIsDialogOpen(!isDialogOpen);
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
        fetch(`${API_BASE_URL}/get_workspaces_access`, {
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
                setWorkspaces_access(data["workspaces"]);
            })
            .catch(error => {
                setError(error.message);
            });
    }, []);

    useEffect(() => {
        fetch(`${API_BASE_URL}/get_workspaces_open`, {
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
                setWorkspaces_open(data["workspaces"]);
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

    return (
        <div className="page">

            {/*/ ДИАЛОГ СОЗДАНИЯ  ВОРКСПЕЙСА /*/}

            {isDialogOpen && (
                <div className="dialog-container">
                    <h3>
                        Создать рабочее пространство
                    </h3>
                    <div className="form-group">
                        <label htmlFor="title">Заголовок</label>
                        <input
                            type="text"
                            id="title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="description">Описание</label>
                        <input
                            type="description"
                            id="description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            required
                        />
                    </div>
                    <button className="add-workspace-button"
                            onClick={() => handleWorkspaceAdding(title, description)}>Сохранить
                    </button>
                    <button className="add-workspace-button-close" onClick={toggleDialog}>Закрыть</button>
                </div>
            )}

            {/*/ ГЛАВНЫЙ ЭКРАН /*/}

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
                            {workspaces.length > 0 ? (<ul className="all-workspaces-container">
                                {workspaces.map(workspace => (
                                    <li onClick={() => handleWorkspaceClick(workspace.id)} className="workspace-item"
                                        key={workspace.id}>{workspace.title}</li>))}
                            </ul>) : (<p className="workspace-item">Не найдено рабочих пространств</p>)}

                            {workspaces_access.length > 0 ? (
                                <ul className="all-workspaces-container">
                                    <p className="workspace-item-title">Пространства, к которым предоставлен доступ</p>
                                    {workspaces_access.map(workspace => (
                                        <li onClick={() => handleWorkspaceClick(workspace.id)}
                                            className="workspace-item"
                                            key={workspace.id}>
                                            {1 === workspace.access_type && <span><b>🔗</b> </span>}
                                            {2 === workspace.access_type && <span><b>👤</b> </span>}
                                            {3 === workspace.access_type && <span><b>👥</b> </span>}
                                            {workspace.title}
                                        </li>))}
                                </ul>) : (<p></p>)}

                            {workspaces_open.length > 0 ? (
                                <ul className="all-workspaces-container">
                                    <p className="workspace-item-title">Общедоступные пространства</p>
                                    {workspaces_open.map(workspace => (
                                        <li onClick={() => handleWorkspaceClick(workspace.id)}
                                            className="workspace-item"
                                            key={workspace.id}>
                                            {1 === workspace.access_type && <span><b>🔗</b> </span>}
                                            {2 === workspace.access_type && <span><b>👤</b> </span>}
                                            {3 === workspace.access_type && <span><b>👥</b> </span>}
                                            {workspace.title}
                                        </li>))}
                                </ul>) : (<p></p>)}

                            <button className="add-workspace" onClick={toggleDialog}><p>+</p></button>
                        </div>
                    </div>

                    {/*/ ТЕКУЩЕЕ ПРОСТРАНСТВО /*/}

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
                                    {workspace.branches.map(branch => (
                                        <li
                                            className="branch-item"
                                            key={branch.id}
                                            onClick={() => goToBranch(workspace.id, branch.id)}
                                        >
                                            {branch.id === workspace.main_branch && <span><b>🏠</b> </span>}{branch.name}
                                        </li>
                                    ))}
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

                            <div className="workspace-archive">
                                <p>Архивировать (TODO)</p>
                            </div>

                        </div>) : (<p>Нажмите на рабочее пространство для просмотра</p>)}
                    </div>
                </div>

            </div>
        </div>);
}

export async function handleWorkspaceAdding(title, description) {
    try {
        const response = await add_workspace({title, description});

        if (response === 200) {
            localStorage.setItem('authToken', response.token);

            window.location.href = '/workspaces';
            console.error('Registration was successful, token provided in the response.');
        } else {
            console.error('Registration was unsuccessful, no token provided in the response.');
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
    }
}

function getStatusColor(status) {
    const statusColors = {
        1: 'green',
        2: 'gray',
        3: 'red'
    };

    return statusColors[status] || 'white'; // Set your default color here.
}

function goHome() {
    window.location.href = '/workspaces';
}

function goToProfile() {
    window.location.href = '/me';
}

function goToBranch(spaceId, branchId) {
    window.location.href = `/branch/${spaceId}/${branchId}`;
}

export default UserWorkspaces;
