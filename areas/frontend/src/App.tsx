import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { UserContext } from 'context/UserContext';
import { SessionLayout } from 'layouts/SessionLayout';
import { SpacePage } from 'pages/SpacePage';
import { NotFoundPage } from 'pages/NotFoundPage';
import { Overlay } from 'layouts/Overlay';
import { LoadingLayout } from 'layouts/LoadingLayout';
import { withUserContext } from 'hocs/withUserContext';
import { compose } from 'utils/helpers';

function App() {
    const { authorized, rootDirId } = React.useContext(UserContext);

    return (
        <Overlay>
            <LoadingLayout>
                <BrowserRouter>
                    {authorized && (
                        <SessionLayout>
                            <Routes>
                                <Route path="/" element={<Navigate to={`dirs/${rootDirId}`} />} />
                                <Route path="dirs/:dirId" element={<SpacePage />} />
                                <Route path="*" element={<NotFoundPage />} />
                            </Routes>
                        </SessionLayout>
                    )}
                </BrowserRouter>
            </LoadingLayout>
        </Overlay>
    );
}

const _App = compose(withUserContext)(App);
export { _App as App };
