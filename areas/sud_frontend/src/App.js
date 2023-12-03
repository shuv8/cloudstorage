import React, {Fragment} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import LoginForm from './login/LoginForm';
import RegistrationForm from './registration/RegistrationForm';

import {handleLogin} from './login/LoginForm';
import {handleRegistration} from './registration/RegistrationForm';
import UserWorkspaces from "./workspaces/UserWorkspaces";
import WhoIAm from "./whoiam/WhoIAm";
import Branch from "./branch/Branch";
import Admin from "./admin/Admin";

function App() {
    return (
        <div className="App">
            <Router>
                <Fragment>
                    <Routes>
                        <Route exact path="/login" element={<LoginForm onLogin={handleLogin}/>}/>
                        <Route exact path="/workspaces" element={<UserWorkspaces/>}/>
                        <Route exact path="/me" element={<WhoIAm/>}/>
                        <Route exact path="/admin" element={<Admin/>}/>
                        <Route exact path="/branch/:space_id/:branch_id" element={<Branch/>}/>
                        <Route exact path="/registration"
                               element={<RegistrationForm onRegistration={handleRegistration}/>}
                        />
                    </Routes>
                </Fragment>
            </Router>
        </div>
    );
}

export default App;