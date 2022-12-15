import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RemoveAccessEmailRequestInput = {
    itemId: string;
    email: string;
};

const removeAccessEmail: TRequest<TRequestParamsWithInput<RemoveAccessEmailRequestInput>, {}> = ({ input, config }) => {
    const { email, itemId } = input;
    return instance.delete(`remove_access/${itemId}/email/${email}`, { ...config });
};

export function useRemoveAccessEmailLazy() {
    return useRequestLazy<TRequestParamsWithInput<RemoveAccessEmailRequestInput>, {}>({
        request: removeAccessEmail,
    });
}

export function useRemoveAccessEmail(params: TRequestParamsWithInput<RemoveAccessEmailRequestInput>) {
    return useRequest({ service: useRemoveAccessEmailLazy(), params });
}
