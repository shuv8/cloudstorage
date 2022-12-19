import React from 'react';
import { CenteredContainer } from 'components/CenteredContainer';
import { TextField } from '@mui/material';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import { useLoginLazy, useWhoAmI, useWhoAmILazy } from 'api';

export function LoginPage() {

    let state = {
        email: 'Enter text',
        password: 'Enter text'
    };

    let handleChangeEmail = (event: any) => {
        state.email = event.target.value;
    };

    let handleChangePassword = (event: any) => {
        state.password = event.target.value;
    };

    const navigate = useNavigate();
    const { data, fetch, fetched } = useLoginLazy();

    const handleClick = React.useCallback(
        (event: React.MouseEvent<HTMLButtonElement>) => {
            fetch({
                input: {
                    email: state.email,
                    password: state.password
                }
             }).then(r => {navigate(`/`);});
        },[fetch]
    );


    React.useEffect(() => {
        if (fetched) {
            navigate(`/`);
        }
    }, []);


    return (
        <CenteredContainer>
            <TextField id='email' label='email' variant='outlined' onChange={handleChangeEmail} />
            <TextField id='password' label='password' variant='outlined' onChange={handleChangePassword}
                       margin='normal' />
            <Button variant='contained' onClick={handleClick}>Login</Button>
        </CenteredContainer>
    );
}
