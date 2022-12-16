import React from 'react';
import { TActiveDirectory } from './types';

type TSpaceContext = {
    activeDirectory: TActiveDirectory;
    setActiveDirectory(dir: TActiveDirectory): void;
};

export const SpaceContext = React.createContext({} as TSpaceContext);
