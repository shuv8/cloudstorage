import ErrorIcon from '@mui/icons-material/Error';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import CircularProgress from '@mui/material/CircularProgress';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import type { ReactChild } from 'react';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useGetSpaceByIdLazy } from 'api';
import { CenteredContainer } from 'components/CenteredContainer';
import { SpacesList } from './components/SpacesList';

type SessionLayoutProps = {
    children: ReactChild;
};

export function SessionLayout(props: SessionLayoutProps) {
    const navigate = useNavigate();
    const { data, loading, error, fetch, fetched, called } = useGetSpaceByIdLazy();

    React.useEffect(() => {
        if (data?.items.length) {
            navigate(`/dirs/${data.items[0].id}`);
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
            <Box flex={1}>
                {called && (loading || !fetched) ? (
                    <CenteredContainer>
                        <CircularProgress />
                    </CenteredContainer>
                ) : error ? (
                    <CenteredContainer>
                        <ErrorIcon sx={{ fontSize: 168, color: 'red' }} />
                        <Typography>
                            Не удалось загрузить
                            <br />
                            содержимое
                        </Typography>
                    </CenteredContainer>
                ) : (
                    props.children
                )}
            </Box>
        </Stack>
    );
}
