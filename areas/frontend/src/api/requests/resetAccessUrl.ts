import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type ResetAccessUrlRequestInput = {
    itemId: string;
};

const resetAccessUrl: TRequest<TRequestParamsWithInput<ResetAccessUrlRequestInput>, {}> = ({ input, config }) => {
    const { itemId } = input;
    return instance.delete(`reset_access/${itemId}`, { ...config });
};

export function useResetAccessUrlLazy() {
    return useRequestLazy<TRequestParamsWithInput<ResetAccessUrlRequestInput>, {}>({
        request: resetAccessUrl,
    });
}

export function useResetAccessUrl(params: TRequestParamsWithInput<ResetAccessUrlRequestInput>) {
    return useRequest({ service: useResetAccessUrlLazy(), params });
}
