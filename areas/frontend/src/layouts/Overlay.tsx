import Box from '@mui/material/Box';
import type { ReactChild } from 'react';
import React from 'react';

type OverlayProps = {
    children: ReactChild;
};

export function Overlay(props: OverlayProps) {
    return <Box height="100vh">{props.children}</Box>;
}
