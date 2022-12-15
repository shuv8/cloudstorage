import type { Item } from '../schema';
import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type GetDirRequestInput = {
    spaceId: string;
    dirId: string;
};

type GetDirRequestResult = {
    items: Item[];
};

const getDir: TRequest<TRequestParamsWithInput<GetDirRequestInput>, GetDirRequestResult> = ({ input, config }) => {
    const { spaceId, dirId } = input;
    return instance.get(`get_dir/${spaceId}/${dirId}`, { ...config });
};

export function useGetDirLazy() {
    return useRequestLazy<TRequestParamsWithInput<GetDirRequestInput>, {}>({
        request: getDir,
    });
}

export function useGetDir(params: TRequestParamsWithInput<GetDirRequestInput>) {
    return useRequest({ service: useGetDirLazy(), params });
}
