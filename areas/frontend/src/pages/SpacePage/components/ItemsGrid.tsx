import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ErrorIcon from '@mui/icons-material/Error';
import Folder from '@mui/icons-material/Folder';
import InsertDriveFile from '@mui/icons-material/InsertDriveFile';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import type { ButtonProps } from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import React from 'react';
import { ITEM_ENTITY, useGetDir } from 'api';
import { CenteredContainer } from 'components/CenteredContainer';
import { SpaceContext } from '../context/SpaceContext';

type ItemsGridProps = {
    dirId: string;
    onItemClick: ButtonProps['onClick'];
};

function ItemsGrid(props: ItemsGridProps) {
    const { dirId, onItemClick } = props;

    const { setActiveDirectory, setPath, setItems } = React.useContext(SpaceContext);
    const { data, loading, error, fetch, fetched } = useGetDir({ input: { dirId } });

    React.useEffect(() => {
        fetch({ input: { dirId } });
    }, [fetch, dirId]);

    React.useEffect(() => {
        if (data) {
            setActiveDirectory({
                entity: 'Directory',
                id: dirId,
                name: data.name,
            });

            setPath(data.path);
            setItems(data.items);
        }
    }, [dirId, data]);

    if (loading || !fetched) {
        return (
            <CenteredContainer>
                <CircularProgress />
            </CenteredContainer>
        );
    }

    if (error) {
        return (
            <CenteredContainer>
                <ErrorIcon sx={{ fontSize: 168, color: 'red' }} />
                <Typography>
                    Не удалось загрузить
                    <br />
                    содержимое
                </Typography>
            </CenteredContainer>
        );
    }

    if (!data?.items.length) {
        return (
            <CenteredContainer>
                <AutoAwesomeIcon sx={{ fontSize: 168, color: 'yellow' }} />
                <Typography>Папка пуста</Typography>
            </CenteredContainer>
        );
    }

    return (
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
                        onClick={entity === ITEM_ENTITY.directory ? onItemClick : undefined}
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
    );
}

const ItemsGridMemoized = React.memo(ItemsGrid);
export { ItemsGridMemoized as ItemsGrid };
