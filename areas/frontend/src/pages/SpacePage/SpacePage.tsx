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

    const handleItemClick = (event: React.MouseEvent<HTMLButtonElement>) => {
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
    };

    return (
        <>
            <Box>
                <Stack direction="row" spacing="8px" divider={<Divider orientation="vertical" flexItem />}>
                    {path.map(({ id, name }) => (
                        <Button key={id} id={id} onClick={handlePathClick} color="primary">
                            {name}
                        </Button>
                    ))}
                    <Button color="inherit">{activeDirectory?.name}</Button>
                </Stack>
                <Divider />
            </Box>

            <Box height="100%">
                <ItemsGrid dirId={dirId} onItemClick={handleItemClick} />
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
