import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import Folder from '@mui/icons-material/Folder';
import InsertDriveFile from '@mui/icons-material/InsertDriveFile';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { AxiosError } from 'axios';
import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ITEM_ENTITY, useGetDir } from 'api';
import { SpaceProvider } from './context/SpaceContext';

type SpacePageProps = {
    dirId: string;
};

function SpacePage(props: SpacePageProps) {
    const { dirId } = props;

    const navigate = useNavigate();
    const { data, loading, error, fetch } = useGetDir({ input: { dirId } });

    React.useEffect(() => {
        fetch({ input: { dirId } });
    }, [fetch, dirId]);

    const handleOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
        const { id } = event.currentTarget;
        navigate({ pathname: `/dirs/${id}` });
    };

    if (loading) {
        return <>Загрузка...</>;
    }

    if (error) {
        if (error instanceof AxiosError) {
            return <>{error.response?.data.error}</>;
        }
    }

    return (
        <>
            <Box>
                <Stack direction="row" spacing="8px" divider={<Divider orientation="vertical" flexItem />}>
                    {data?.path.map(({ id, name }) => (
                        <Button id={id} onClick={handleOpen} color="primary">
                            {name}
                        </Button>
                    ))}
                    <Button color="inherit">Имя текущей папки</Button>
                </Stack>
                <Divider />
            </Box>

            <Box padding="24px">
                {data?.items.length ? (
                    <Grid
                        container
                        columns={12}
                        direction="row"
                        justifyContent="flex-start"
                        alignItems="center"
                        columnSpacing="12px"
                    >
                        {data?.items.map(({ id, entity, name }) => (
                            <Grid key={id} item>
                                <Button
                                    id={id}
                                    onClick={entity === ITEM_ENTITY.directory ? handleOpen : undefined}
                                    color="primary"
                                >
                                    <Stack spacing="4px" sx={{ width: 108, overflow: 'hidden' }}>
                                        <Box component="div" display="flex" justifyContent="center">
                                            {entity === ITEM_ENTITY.directory && <Folder sx={{ fontSize: 92 }} />}
                                            {entity === ITEM_ENTITY.file && <InsertDriveFile sx={{ fontSize: 92 }} />}
                                        </Box>
                                        <Typography
                                            sx={{
                                                whiteSpace: 'nowrap',
                                                overflow: 'hidden',
                                                textOverflow: 'ellipsis',
                                            }}
                                        >
                                            {name}
                                        </Typography>
                                    </Stack>
                                </Button>
                            </Grid>
                        ))}
                    </Grid>
                ) : (
                    <Box
                        component="div"
                        display="flex"
                        flexDirection="column"
                        justifyContent="center"
                        alignItems="center"
                    >
                        <AutoAwesomeIcon sx={{ fontSize: 92 }} />
                        <Typography>НИХУЯ НЕТ</Typography>
                    </Box>
                )}
            </Box>
        </>
    );
}

function SpacePageWithContext(props: SpacePageProps) {
    return (
        <SpaceProvider>
            <SpacePage {...props} />
        </SpaceProvider>
    );
}

function Mediator() {
    const { dirId } = useParams<'dirId'>();
    const navigate = useNavigate();

    if (!dirId) {
        navigate('/404');
        return null;
    }

    return <SpacePageWithContext dirId={dirId} />;
}

export { Mediator as SpacePage };
