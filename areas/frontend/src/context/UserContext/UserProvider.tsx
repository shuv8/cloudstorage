import type { ReactChild } from 'react';
import React from 'react';
import type { TUserContext } from './UserContext';
import { UserContext } from './UserContext';

type UserProviderProps = {
    children: ReactChild;
};

export function UserProvider(props: UserProviderProps) {
    const [rootSpaceId, setRootSpaceId] = React.useState<TUserContext['rootSpaceId']>(null);
    const [rootDirId, setRootDirId] = React.useState<TUserContext['rootDirId']>(null);
    const [spaces, setSpaces] = React.useState<TUserContext['spaces']>([]);

    return (
        <UserContext.Provider
            value={{
                rootDirId,
                rootSpaceId,
                setRootDirId,
                setRootSpaceId,
                setSpaces,
                spaces,
            }}
        >
            {props.children}
        </UserContext.Provider>
    );
}
