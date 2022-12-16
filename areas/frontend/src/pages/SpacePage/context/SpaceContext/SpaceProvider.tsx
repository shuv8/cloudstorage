import type { ReactChild } from 'react';
import React from 'react';
import { SpaceContext } from './SpaceContext';
import { TActiveDirectory } from './types';

type SpaceProviderProps = {
    children: ReactChild;
};

export function SpaceProvider(props: SpaceProviderProps) {
    const [activeDirectory, setActiveDirectory] = React.useState<TActiveDirectory>(null);

    return (
        <SpaceContext.Provider
            value={{
                activeDirectory,
                setActiveDirectory,
            }}
        >
            {props.children}
        </SpaceContext.Provider>
    );
}
