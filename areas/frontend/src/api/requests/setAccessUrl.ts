import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type SetAccessUrlRequestInput = {
    itemId: string;
    viewOnly: boolean;
};

type SetAccessUrlRequestResult = { };


const setAccessUrl: TRequest<TRequestParams<SetAccessUrlRequestInput>, SetAccessUrlRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    const viewOnly = input?.viewOnly
    return instance.put(`set_access/${itemId}?view_only=${viewOnly}`,  { ...input }, { ...config });
};

export function useSetAccessUrlLazy() {
    return useRequestLazy<TRequestParams<SetAccessUrlRequestInput>, {}>({
        request: setAccessUrl
    });
}

export function useSetAccessUrl(params: TRequestParams<SetAccessUrlRequestInput>) {
    return useRequest({ service: useSetAccessUrlLazy(), params });
}
