import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import type { ReactChild } from 'react';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useGetSpaceByIdLazy } from 'api';
import { SpacesList } from './components/SpacesList';

type SessionLayoutProps = {
    children: ReactChild;
};

export function SessionLayout(props: SessionLayoutProps) {
    const navigate = useNavigate();
    const { data, fetch, fetched } = useGetSpaceByIdLazy();

    React.useEffect(() => {
        if (fetched) {
            navigate(`/dirs/${data?.items[0].id || 'error'}`);
        }
    }, [data?.items]);

    const handleSpaceClick = React.useCallback(
        (event: React.MouseEvent<HTMLButtonElement>) => {
            const { id } = event.currentTarget;
            fetch({ input: { spaceId: id } });
        },
        [fetch]
    );

    return (
        <Stack height="100%" direction="row" divider={<Divider orientation="vertical" />}>
            <Box width="100%" maxWidth="212px">
                <SpacesList onSpaceClick={handleSpaceClick} />
            </Box>
            <Box flex={1}>{props.children}</Box>
        </Stack>
    );
}
