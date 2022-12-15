import React from 'react';
import { useLoginLazy, useRegistrationLazy } from 'api';

export function App() {
    const registrationService = useRegistrationLazy();
    console.log({ registrationService });
    const loginService = useLoginLazy();
    console.log({ loginService });

    React.useEffect(() => {
        registrationService.fetch({
            input: {
                email: 'chocho@mail.ru',
                password: 'chochopass',
                role: 2,
                username: 'chocho',
            },
        });

        loginService.fetch({
            input: {
                email: 'chocho@mail.ru',
                password: 'chochopass',
            },
        });
    }, []);

    return <React.Fragment />;
}
