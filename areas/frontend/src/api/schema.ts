export const USER_ROLES = {
    admin: 1,
    client: 2,
} as const;

export type UserRolesKeys = keyof typeof USER_ROLES;
export type UserRolesValues = typeof USER_ROLES[UserRolesKeys];

export const SPACE_TYPES = {
    regular: 1,
    complaint: 2,
    shared: 3,
} as const;

export type SpaceTypesKeys = keyof typeof SPACE_TYPES;
export type SpaceTypesValues = typeof SPACE_TYPES[SpaceTypesKeys];

export type Space = {
    id: string;
    name: string;
    type: SpaceTypesValues;
};

export const ITEM_ENTITY = {
    directory: 'Directory',
    file: 'File',
} as const;

export type ItemEntityKeys = keyof typeof ITEM_ENTITY;
export type ItemEntityValues = typeof ITEM_ENTITY[ItemEntityKeys];

type Item = {
    id: string;
    name: string;
};

export type Directory = Item & {
    entity: typeof ITEM_ENTITY['directory'];
};

export type File = Item & {
    entity: typeof ITEM_ENTITY['file'];
    type: string;
};

export type DirectoryPath = Item[];

export type Access = {
    class: string;
    type: string;
    content: string;
};

export type Department = {
    department_name: string;
};

export type User = {
    rootSpaceId: Space['id'];
    rootDirId: Directory['id'];
};

