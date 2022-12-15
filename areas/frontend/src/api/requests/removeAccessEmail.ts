import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RemoveAccessEmailRequestInput = {
    itemId: string;
    email: string;
};

type RemoveAccessEmailRequestResult = { };


const removeAccessEmail: TRequest<TRequestParams<RemoveAccessEmailRequestInput>, RemoveAccessEmailRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    const email = input?.email
    return instance.delete(`remove_access/${itemId}/email/${email}`, { ...config });
};

export function useRemoveAccessEmailLazy() {
    return useRequestLazy<TRequestParams<RemoveAccessEmailRequestInput>, {}>({
        request: removeAccessEmail
    });
}

export function useRemoveAccessEmail(params: TRequestParams<RemoveAccessEmailRequestInput>) {
    return useRequest({ service: useRemoveAccessEmailLazy(), params });
}
