export const USER_ROLES = {
    admin: 1,
    client: 2,
} as const;

export type UserRolesKeys = keyof typeof USER_ROLES;
export type UserRolesValues = typeof USER_ROLES[UserRolesKeys];
