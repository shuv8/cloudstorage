import React from 'react';
import { useLogin, useRegistration } from 'api';

export function App() {
    useRegistration({
        input: {
            email: 'chocho@mail.ru',
            password: 'chochopass',
            role: 2,
            username: 'chocho',
        },
    });

    useLogin({
        input: {
            email: 'chocho@mail.ru',
            password: 'chochopass',
        },
    });

    return <React.Fragment />;
}
