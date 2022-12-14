import { TRequest, TRequestParamsWithPayload } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type LoginRequestInput = {
    email: string;
    password: string;
};

const login: TRequest<TRequestParamsWithPayload<LoginRequestInput>, {}> = ({ input, config }) => {
    return instance.put('login', { ...input }, { ...config });
};

export function useLoginLazy() {
    return useRequestLazy<TRequestParamsWithPayload<LoginRequestInput>, {}>({
        request: login,
    });
}

export function useLogin(params: TRequestParamsWithPayload<LoginRequestInput>) {
    return useRequest({ state: useLoginLazy(), params });
}
