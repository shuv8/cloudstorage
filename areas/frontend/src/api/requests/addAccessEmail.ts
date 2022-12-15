import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type AddAccessEmailRequestInput = {
    itemId: string;
    email: string;
    viewOnly: boolean;
};

type AddAccessEmailRequestResult = { };


const addAccessEmail: TRequest<TRequestParams<AddAccessEmailRequestInput>, AddAccessEmailRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    const email = input?.email
    const viewOnly = input?.viewOnly
    return instance.put(`add_access/${itemId}/email/${email}?view_only=${viewOnly}`, { ...input }, { ...config });
};

export function useAddAccessEmailLazy() {
    return useRequestLazy<TRequestParams<AddAccessEmailRequestInput>, {}>({
        request: addAccessEmail
    });
}

export function useAddAccessEmail(params: TRequestParams<AddAccessEmailRequestInput>) {
    return useRequest({ service: useAddAccessEmailLazy(), params });
}
