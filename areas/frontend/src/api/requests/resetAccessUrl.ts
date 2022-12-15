import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type ResetAccessUrlRequestInput = {
    itemId: string;
};

type ResetAccessUrlRequestResult = { };


const resetAccessUrl: TRequest<TRequestParams<ResetAccessUrlRequestInput>, ResetAccessUrlRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    return instance.delete(`reset_access/${itemId}`, { ...config });
};

export function useResetAccessUrlLazy() {
    return useRequestLazy<TRequestParams<ResetAccessUrlRequestInput>, {}>({
        request: resetAccessUrl
    });
}

export function useResetAccessUrl(params: TRequestParams<ResetAccessUrlRequestInput>) {
    return useRequest({ service: useResetAccessUrlLazy(), params });
}
