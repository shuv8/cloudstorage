import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import type { ReactChild } from 'react';
import React from 'react';

type SessionLayoutProps = {
    children: ReactChild;
};

export function SessionLayout(props: SessionLayoutProps) {
    return (
        <Box display="flex" flexDirection="column" height="100vh">
            <Stack flex={1} direction="row" divider={<Divider orientation="vertical" />}>
                <Box width="100%" maxWidth="175px">
                    <Typography textAlign="center">ТУТ БУДУТ СПЕЙСЫ</Typography>
                </Box>
                <Box flex={1}>{props.children}</Box>
            </Stack>
        </Box>
    );
}
