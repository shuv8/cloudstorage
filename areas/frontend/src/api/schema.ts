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

export type Item = {
    id: string;
    name: string;
    type: string;
    entity: string;
};

export type Access = {
    class: string;
    type: string;
    content: string;
};
