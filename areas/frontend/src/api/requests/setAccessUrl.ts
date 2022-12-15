import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type SetAccessUrlRequestInput = {
    itemId: string;
    viewOnly: boolean;
};

const setAccessUrl: TRequest<TRequestParamsWithInput<SetAccessUrlRequestInput>, {}> = ({ input, config }) => {
    const { itemId, viewOnly } = input;
    return instance.put(`set_access/${itemId}?view_only=${viewOnly}`, { ...input }, { ...config });
};

export function useSetAccessUrlLazy() {
    return useRequestLazy<TRequestParamsWithInput<SetAccessUrlRequestInput>, {}>({
        request: setAccessUrl,
    });
}

export function useSetAccessUrl(params: TRequestParamsWithInput<SetAccessUrlRequestInput>) {
    return useRequest({ service: useSetAccessUrlLazy(), params });
}
