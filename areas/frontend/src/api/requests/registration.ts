import { TRequest, TRequestParamsWithPayload } from '../types';
import type { UserRolesValues } from '../schema';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RegistrationRequestInput = {
    email: string;
    password: string;
    role: UserRolesValues;
    username: string;
};

const registration: TRequest<TRequestParamsWithPayload<RegistrationRequestInput>, {}> = ({ input, config }) => {
    return instance.post('registration', { ...input }, { ...config });
};

export function useRegistrationLazy() {
    return useRequestLazy<TRequestParamsWithPayload<RegistrationRequestInput>, {}>({
        request: registration,
    });
}

export function useRegistration(params: TRequestParamsWithPayload<RegistrationRequestInput>) {
    return useRequest({ state: useRegistrationLazy(), params });
}
