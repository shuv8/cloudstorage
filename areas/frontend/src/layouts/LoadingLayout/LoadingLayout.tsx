import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import type { ReactChild } from 'react';
import React from 'react';
import { UserContext } from 'context/UserContext';
import { useGetSpaces, useWhoAmI } from 'api';

type LoadingLayoutProps = {
    children: ReactChild;
};

export function LoadingLayout(props: LoadingLayoutProps) {
    const { setAuthorized, setRootSpaceId, setRootDirId, setSpaces } = React.useContext(UserContext);

    const whoAmIService = useWhoAmI({});
    const getSpacesService = useGetSpaces({});

    const loading = whoAmIService.loading || getSpacesService.loading;
    const fetched = whoAmIService.fetched || getSpacesService.fetch;

    React.useEffect(() => {
        if (whoAmIService.data) {
            setAuthorized(true);
            setRootSpaceId(whoAmIService.data.rootSpaceId);
            setRootDirId(whoAmIService.data.rootDirId);
        }
    }, [whoAmIService.data]);

    React.useEffect(() => {
        if (getSpacesService.data) {
            setSpaces(getSpacesService.data.spaces);
        }
    }, [getSpacesService.data]);

    if (loading || fetched) {
        return (
            <Box height="100%" display="flex" justifyContent="center" alignItems="center">
                <CircularProgress />
            </Box>
        );
    }

    return <>{props.children}</>;
}
