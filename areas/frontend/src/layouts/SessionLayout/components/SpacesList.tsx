import PersonIcon from '@mui/icons-material/Person';
import type { ButtonProps } from '@mui/material/Button';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import React from 'react';
import { UserContext } from 'context/UserContext';

type SpacesListProps = {
    onSpaceClick: ButtonProps['onClick'];
};

function SpacesList(props: SpacesListProps) {
    const { onSpaceClick } = props;
    const { spaces } = React.useContext(UserContext);

    return (
        <Stack divider={<Divider />}>
            {spaces.map((space) => (
                <Button
                    key={space.id}
                    id={space.id}
                    onClick={onSpaceClick}
                    fullWidth
                    sx={{ justifyContent: 'flex-start', paddingLeft: '12px' }}
                    startIcon={<PersonIcon />}
                >
                    {space.name}
                </Button>
            ))}
        </Stack>
    );
}

const SpaceListMemoized = React.memo(SpacesList);
export { SpaceListMemoized as SpacesList };
