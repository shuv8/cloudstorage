import type { ComponentType } from 'react';
import React from 'react';
import { UserProvider } from 'context/UserContext';

export function withUserContext(Component: ComponentType) {
    return () => (
        <UserProvider>
            <Component />
        </UserProvider>
    );
}
