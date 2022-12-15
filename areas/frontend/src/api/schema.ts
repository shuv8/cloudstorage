export const USER_ROLES = {
    admin: 1,
    client: 2,
} as const;

export type UserRolesKeys = keyof typeof USER_ROLES;
export type UserRolesValues = typeof USER_ROLES[UserRolesKeys];

export type Space = {
    id: string;
    name: string;
    type: string;
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
    entity: typeof ITEM_ENTITY['file'];
};

export type File = Item & {
    entity: typeof ITEM_ENTITY['directory'];
    type: string;
};

export type Access = {
    class: string;
    type: string;
    content: string;
};
