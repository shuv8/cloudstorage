import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type MoveRequestInput = {
    spaceId: string;
    itemId: string;
    target_space: string;
    target_directory: string;
};

const move: TRequest<TRequestParamsWithInput<MoveRequestInput>, {}> = ({ input, config }) => {
    const { spaceId, itemId } = input;
    return instance.put(`move/${spaceId}/${itemId}`, { ...config });
};

export function useMoveLazy() {
    return useRequestLazy<TRequestParamsWithInput<MoveRequestInput>, {}>({
        request: move,
    });
}

export function useMove(params: TRequestParamsWithInput<MoveRequestInput>) {
    return useRequest({ service: useMoveLazy(), params });
}
