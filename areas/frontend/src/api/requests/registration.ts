import { TRequest, TRequestParams } from '../types';
import type { UserRolesValues } from '../schema';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RegistrationRequestInput = {
    email: string;
    password: string;
    role: UserRolesValues;
    username: string;
};

const registration: TRequest<TRequestParams<RegistrationRequestInput>, {}> = ({ input, config }) => {
    return instance.post('registration', { ...input }, { ...config });
};

export function useRegistrationLazy() {
    return useRequestLazy<TRequestParams<RegistrationRequestInput>, {}>({
        request: registration,
    });
}

export function useRegistration(params: TRequestParams<RegistrationRequestInput>) {
    return useRequest({ service: useRegistrationLazy(), params });
}
