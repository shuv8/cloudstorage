import React, {useState, useEffect} from 'react';
import './Request.css';
import {add_request, add_branch, delete_branch} from "../api";
import {useParams} from "react-router-dom";

const API_BASE_URL = 'http://localhost:5000';

function Request() {
    const {space_id, branch_id, request_id} = useParams();

    const [branch, setBranch] = useState([]);
    const [request, setRequest] = useState([]);
    const [user, setUser] = useState("Anonim");
    const [error, setError] = useState(null);

    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const R_STATUS_MAP = {
        1: 'Открыт', 2: 'В ревью', 3: 'Принят', 4: 'Отклонён', 5: 'Закрыт',
    };

    const toggleDialog = () => {
        setIsDialogOpen(!isDialogOpen);
    };

    const toggleCreate = () => {
        setIsCreateOpen(!isCreateOpen);
    };

    const toggleConfirm = () => {
        setIsConfirmOpen(!isConfirmOpen);
    };

    useEffect(() => {
        fetch(`${API_BASE_URL}/workspace/${space_id}/request/${request_id}`, {
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
                setRequest(data);
            })
            .catch(error => {
                setError(error.message);
            });
    }, []);

    useEffect(() => {
        fetch(`${API_BASE_URL}/workspace/${space_id}/view/${branch_id}`, {
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
                setBranch(data);
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
                setUser(data);
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

            {/*/ ДИАЛОГ СОЗДАНИЯ  РЕКВКСТА /*/}

            {isDialogOpen && (
                <div className="dialog-container">
                    <h3>
                        Создать реквест
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
                            onClick={() => handleRequestAdding(space_id, title, description, branch.id, branch.parent)}>Сохранить
                    </button>
                    <button className="add-workspace-button-close" onClick={toggleDialog}>Закрыть</button>
                </div>
            )}

            {/*/ ДИАЛОГ СОЗДАНИЯ  ВЕТКИ /*/}

            {isCreateOpen && (
                <div className="dialog-container">
                    <h3>
                        Создать ветку
                    </h3>
                    <div className="form-group">
                        <label htmlFor="title">Название</label>
                        <input
                            type="text"
                            id="title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>
                    <button className="add-workspace-button"
                            onClick={() => handleBranchAdding(space_id, title, "-1", branch.id)}>Сохранить
                    </button>
                    <button className="add-workspace-button-close" onClick={toggleCreate}>Закрыть</button>
                </div>
            )}

            {/*/ ДИАЛОГ ПОДТВЕРЖЕНИЯ  АРХИВИРОВАНИЯ /*/}

            {isConfirmOpen && (
                <div className="dialog-container">
                    <h3>
                        Удалить ветку?
                    </h3>
                    <button className="branch-delete-button"
                            onClick={() => handleRequestDeletion(space_id, branch.id, branch.parent)}>Да
                    </button>
                    <button className="branch-delete-button-close" onClick={toggleConfirm}>Нет</button>
                </div>
            )}

            {/*/ ГЛАВНЫЙ ЭКРАН /*/}

            <div className="workspaces-container">

                {/*/ ЗАГОЛОВОК /*/}

                <div className="workspace-title-container">
                    <h2 className="workspace-title">
                        <span
                            onClick={() => goHome()}
                            style={{cursor:"pointer"}}
                        >🏠</span> Просмотр ветки
                    </h2>
                    <div className="username-info-right">
                        <div className="username" onClick={() => goToProfile()}>
                            <p className="request-content">{user.username}</p>
                        </div>
                    </div>
                </div>

                <div className="workspace-block">

                    {/*/ ТЕКУЩЕЕ ПРОСТРАНСТВО /*/}

                    <div className="all-files-branches">
                        {request !== "" ? (<div>
                            <div className="request-content-title-container">
                                <div>
                                    <h3 className="request-content-title">{request.title}</h3>
                                    <p className="request-content"><b>Описание: </b>{request.description}</p>
                                </div>
                                <div className="info-right">
                                    <div className="workspace-status"
                                            style={{backgroundColor: getStatusColor(request.status)}}>
                                            <p>{R_STATUS_MAP[request.status] || 'Неизвестно'}</p>
                                    </div>
                                </div>
                            </div> 
                            <div className="all-branches">      
                                <p className="request-content">
                                    <b>Исходная ветка: </b>
                                    <p
                                        className="original-branch-item"
                                        onClick={() => goToBranch(space_id, request.source_branch_id)}
                                    >
                                        {branch.name}
                                    </p>
                                </p>
                                <p className="request-content">
                                    <b>Целевая ветка: </b>
                                    <p
                                        className="original-branch-item"
                                        onClick={() => goToBranch(space_id, request.target_branch_id)}
                                    >
                                        {branch.parentName}
                                    </p>
                                </p>
                            </div>
                            
                            {(branch.author === user.id) && <button className="branch-add" onClick={toggleCreate}>Согласовать</button>}
                            {(branch.author === user.id) && <button className="branch-delete" onClick={toggleConfirm}>Удалить</button>}

                        </div>) : (<p>Нажмите на рабочее пространство для просмотра</p>)}
                    </div>
                </div>

            </div>
        </div>);
}


export async function handleBranchAdding(space_id, name, document_id, parent_branch_id) {
    try {
        const response = await add_branch({name, document_id, parent_branch_id}, space_id);

        if (response[1] === 200) {
            localStorage.setItem('authToken', response.token);

            goToBranch(space_id, response[0].id);
            console.error('Registration was successful, token provided in the response.');
        } else {
            console.error('Registration was unsuccessful, no token provided in the response.');
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
    }
}

export async function handleRequestAdding(space_id, title, description, source_branch_id, target_branch_id) {
    try {
        const response = await add_request({ title, description, source_branch_id, target_branch_id}, space_id);

        if (response === 200) {
            localStorage.setItem('authToken', response.token);

            goToBranch(space_id, source_branch_id);
            console.error('Registration was successful, token provided in the response.');
        } else {
            console.error('Registration was unsuccessful, no token provided in the response.');
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
    }
}

export async function handleRequestDeletion(space_id, branch_id, branch_parent) {
    try {
        const response = await delete_branch(space_id, branch_id);

        if (response === 200) {
            localStorage.setItem('authToken', response.token);

            goToBranch(space_id, branch_parent);
            console.error('Registration was successful, token provided in the response.');
        } else {
            console.error('Registration was unsuccessful, no token provided in the response.');
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
    }
}

function goToProfile() {
    window.location.href = '/me';
}

function goHome() {
    window.location.href = '/workspaces';
}

function goToBranch(space_id, branch_id) {
    window.location.href = `/branch/${space_id}/${branch_id}`;
}

function getStatusColor(status) {
    const statusColors = {
        1: 'blue',
        2: 'yellow',
        3: 'green',
        4: 'red',
        5: 'gray'
    };

    return statusColors[status] || 'white'; 
}

export default Request;