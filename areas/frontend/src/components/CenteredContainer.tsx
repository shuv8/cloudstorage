import Box from '@mui/material/Box';
import React from 'react';

function CenteredContainer(props: React.PropsWithChildren) {
    return (
        <Box
            height="100%"
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
            textAlign="center"
        >
            {props.children}
        </Box>
    );
}

const CenteredContainerMemoized = React.memo(CenteredContainer);
export { CenteredContainerMemoized as CenteredContainer };
