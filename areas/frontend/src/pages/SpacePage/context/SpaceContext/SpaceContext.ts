import React from 'react';
import { DirectoryPath } from 'api';
import { TActiveDirectory, TItems } from './types';

type TSpaceContext = {
    activeDirectory: TActiveDirectory;
    setActiveDirectory(dir: TActiveDirectory): void;
    path: DirectoryPath;
    setPath(path: DirectoryPath): void;
    items: TItems;
    setItems(items: TItems): void;
};

export const SpaceContext = React.createContext({} as TSpaceContext);
