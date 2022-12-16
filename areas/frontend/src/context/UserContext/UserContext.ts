import React from 'react';
import type { Space } from 'api';
import type { TRootDirId, TRootSpaceId } from './types';

export type TUserContext = {
    authorized: boolean;
    setAuthorized(authorized: boolean): void;
    rootSpaceId: TRootSpaceId;
    setRootSpaceId(id: TRootSpaceId): void;
    rootDirId: TRootDirId;
    setRootDirId(id: TRootDirId): void;
    spaces: Space[];
    setSpaces(spaces: Space[]): void;
};

export const UserContext = React.createContext({} as TUserContext);
