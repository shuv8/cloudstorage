import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type DeleteRequestInput = {
    spaceId: string;
    itemId: string;
};

const deleteItem: TRequest<TRequestParamsWithInput<DeleteRequestInput>, {}> = ({ input, config }) => {
    const { spaceId, itemId } = input;
    return instance.delete(`delete/${spaceId}/${itemId}`, { ...config });
};

export function useDeleteLazy() {
    return useRequestLazy<TRequestParamsWithInput<DeleteRequestInput>, {}>({
        request: deleteItem,
    });
}

export function useDelete(params: TRequestParamsWithInput<DeleteRequestInput>) {
    return useRequest({ service: useDeleteLazy(), params });
}
