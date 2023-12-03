import React, {useEffect, useState} from 'react';
import './Admin.css';
import {add_department} from "../api";

const API_BASE_URL = 'http://localhost:5000';


function Admin() {
    const [workspaces, setWorkspaces] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [users, setUsers] = useState([]);
    const [error, setError] = useState(null);
    const [name, setName] = useState(null);

    const [username, setUsername] = useState("Аноним");
    const [userDepartments, setUserDepartments] = useState([]);
    const [isAddDepartmentOpen, setDepartmentOpen] = useState(false);
    const [isUserDepartmentOpen, setUserDepartmentOpen] = useState(false);

    const toggleDepartmentDialog = () => {
        setDepartmentOpen(!isAddDepartmentOpen);
    };


    const toggleUserDepartmentDialog = () => {
        setUserDepartmentOpen(!isUserDepartmentOpen);
    };

    const handleUserDepartmentClick = (name) => {
        fetch(`${API_BASE_URL}/department/users?name=${name}`, {
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
                setUserDepartments(data["users"]);
                toggleUserDepartmentDialog()
            })
            .catch(error => {
                setError(error.message);
            });
    };

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

            {/*/ ДИАЛОГ СОЗДАНИЯ ОТДЕЛА /*/}

            {isAddDepartmentOpen && (
                <div className="dialog-container">
                    <h3>
                        Создать отдел
                    </h3>
                    <div className="form-group">
                        <label htmlFor="name">Заголовок</label>
                        <input
                            type="text"
                            id="name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <button className="add-workspace-button"
                            onClick={() => handleDepartmentAdding(name)}>Сохранить
                    </button>
                    <button className="add-workspace-button-close" onClick={toggleDepartmentDialog}>Закрыть</button>
                </div>
            )}


            {/*/ ДИАЛОГ ПОЛЬЗОВАТЕЛЕЙ В ОТДЕЛЕ /*/}

            {isUserDepartmentOpen && (
                <div className="dialog-container">
                    <h3>
                        Пользователи в отделе
                    </h3>

                    {userDepartments.length > 0 ? (<ul className="all-workspaces-container">
                        {userDepartments.map(user_department => (
                            <div>
                                <li
                                    className="remove-action-button"
                                >Удалить доступ для отдела {userDepartments.email}
                                </li>
                            </div>
                        ))}

                    </ul>) : (<p></p>)}
                    <button className="workspace-archive-button-close" onClick={() => toggleUserDepartmentDialog()}>
                        Закрыть
                    </button>
                </div>
            )}

            <div className="workspaces-container">

                {/*/ ЗАГОЛОВОК /*/}

                <div className="workspace-title-container">
                    <h2 className="workspace-title"><span
                        onClick={() => goHome()}
                        style={{cursor: "pointer"}}
                    >🏠</span> Панель администратора</h2>
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
                            <h4>Рабочие пространства</h4>
                            {workspaces != null && workspaces.length > 0 ? (<ul className="all-workspaces-container">
                                {workspaces.map(workspace => (
                                    <li onClick={() => {
                                    }} className="workspace-item"
                                        key={workspace.id}>{workspace.title}</li>))}
                            </ul>) : (<p className="workspace-item-p">Не найдено рабочих пространств</p>)}
                        </div>
                    </div>

                    {/*/ ОТДЕЛЫ /*/}

                    <div className="all-workspaces-secondary">
                        <div>
                            <h4>Отделы</h4>
                            {departments != null && departments.length > 0 ? (<ul className="all-workspaces-container">
                                {departments.map(department => (
                                    <li onClick={() => {
                                        handleUserDepartmentClick(department.department_name)
                                    }} className="workspace-item">{department.department_name}</li>))}
                            </ul>) : (<p className="workspace-item-p">Не найдено отделов</p>)}
                        </div>

                        <button className="add-workspace" onClick={toggleDepartmentDialog}><p>+</p></button>
                    </div>

                    {/*/ ЮЗВЕРЫ /*/}

                    <div className="all-workspaces-secondary">
                        <div>
                            <h4>Пользователи</h4>
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

export async function handleDepartmentAdding(department_name) {
    try {
        const response = await add_department({department_name});

        if (response === 200) {
            localStorage.setItem('authToken', response.token);

            reload();
            console.error('Registration was successful, token provided in the response.');
        } else {
            console.error('Registration was unsuccessful, no token provided in the response.');
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
    }
}

function goHome() {
    window.location.href = '/workspaces';
}


function reload() {
    window.location.href = '/admin';
}

function goToProfile() {
    window.location.href = '/me';
}


export default Admin;