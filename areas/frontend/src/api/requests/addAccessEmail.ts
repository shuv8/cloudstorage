import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type AddAccessEmailRequestInput = {
    itemId: string;
    email: string;
    viewOnly: boolean;
};

const addAccessEmail: TRequest<TRequestParamsWithInput<AddAccessEmailRequestInput>, {}> = ({ input, config }) => {
    const { itemId, email, viewOnly } = input;

    return instance.put(`add_access/${itemId}/email/${email}?view_only=${viewOnly}`, { ...input }, { ...config });
};

export function useAddAccessEmailLazy() {
    return useRequestLazy<TRequestParamsWithInput<AddAccessEmailRequestInput>, {}>({
        request: addAccessEmail,
    });
}

export function useAddAccessEmail(params: TRequestParamsWithInput<AddAccessEmailRequestInput>) {
    return useRequest({ service: useAddAccessEmailLazy(), params });
}
