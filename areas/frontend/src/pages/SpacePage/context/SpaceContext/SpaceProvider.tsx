import { DirectoryPath } from 'api';
import type { ReactChild } from 'react';
import React from 'react';
import { SpaceContext } from './SpaceContext';
import { TActiveDirectory, TItems } from './types';

type SpaceProviderProps = {
    children: ReactChild;
};

export function SpaceProvider(props: SpaceProviderProps) {
    const [activeDirectory, setActiveDirectory] = React.useState<TActiveDirectory>(null);
    const [path, setPath] = React.useState<DirectoryPath>([]);
    const [items, setItems] = React.useState<TItems>([]);

    return (
        <SpaceContext.Provider
            value={{
                activeDirectory,
                setActiveDirectory,
                path,
                setPath,
                items,
                setItems,
            }}
        >
            {props.children}
        </SpaceContext.Provider>
    );
}
