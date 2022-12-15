import { TRequest, TRequestParams } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type LoginRequestInput = {
    email: string;
    password: string;
};

const login: TRequest<TRequestParams<LoginRequestInput>, {}> = ({ input, config }) => {
    return instance.put('login', { ...input }, { ...config });
};

export function useLoginLazy() {
    return useRequestLazy<TRequestParams<LoginRequestInput>, {}>({
        request: login,
    });
}

export function useLogin(params: TRequestParams<LoginRequestInput>) {
    return useRequest({ service: useLoginLazy(), params });
}
