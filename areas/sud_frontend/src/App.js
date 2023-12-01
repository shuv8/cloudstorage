import React, {Fragment} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import LoginForm from './LoginForm';

import {handleLogin} from './LoginForm';
import UserWorkspaces from "./UserWorkspaces";

function App() {
    return (
        <div className="App">
            <Router>
                <Fragment>
                    <Routes>
                        <Route exact path="/login" element={<LoginForm onLogin={handleLogin}/>}/>
                        <Route exact path="/workspaces" element={<UserWorkspaces/>}/>
                    </Routes>
                </Fragment>
            </Router>
        </div>
    );
}

export default App;