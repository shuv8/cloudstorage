import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { UserContext } from 'context/UserContext';
import { SessionLayout } from 'layouts/SessionLayout';
import { SpacePage } from 'pages/SpacePage';
import { Overlay } from 'layouts/Overlay';
import { LoadingLayout } from 'layouts/LoadingLayout';

export function App() {
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
                                <Route path="*" element={<div>404</div>} />
                            </Routes>
                        </SessionLayout>
                    )}
                </BrowserRouter>
            </LoadingLayout>
        </Overlay>
    );
}
