import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { SpaceContext, SpaceProvider } from './context/SpaceContext';
import { ItemsGrid } from './components/ItemsGrid';

type SpacePageProps = {
    dirId: string;
};

function SpacePage(props: SpacePageProps) {
    const { dirId } = props;

    const navigate = useNavigate();
    const { activeDirectory, path, items } = React.useContext(SpaceContext);

    const handlePathClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        const { id } = event.currentTarget;
        navigate({ pathname: `/dirs/${id}` });
    };

    const handleItemClick = React.useCallback(
        (event: React.MouseEvent<HTMLButtonElement>) => {
            const { id } = event.currentTarget;

            const item = items.find((_item) => _item.id === id);
            if (!item) {
                // TODO: ALERT CALL
                return;
            }

            if (item.entity === 'Directory') {
                navigate({ pathname: `/dirs/${id}` });
            }

            if (item.entity === 'File') {
                // TODO: нада думать
            }
        },
        [items, navigate]
    );

    return (
        <Stack height="100%" divider={<Divider />}>
            {(path.length || activeDirectory) && (
                <Stack direction="row" divider={<Divider orientation="vertical" flexItem />}>
                    {path.map(({ id, name }) => (
                        <Button key={id} id={id} onClick={handlePathClick} color="primary">
                            {name}
                        </Button>
                    ))}
                    {activeDirectory && <Button color="inherit">{activeDirectory.name}</Button>}
                </Stack>
            )}

            <Box height="100%">
                <ItemsGrid dirId={dirId} onItemClick={handleItemClick} />
            </Box>
        </Stack>
    );
}

function SpacePageWithContext(props: SpacePageProps) {
    return (
        <SpaceProvider>
            <SpacePage {...props} />
        </SpaceProvider>
    );
}

function SpacePageMediator() {
    const { dirId } = useParams<'dirId'>();
    const navigate = useNavigate();

    if (!dirId) {
        navigate('/404');
        return null;
    }

    return <SpacePageWithContext dirId={dirId} />;
}

export { SpacePageMediator as SpacePage };
