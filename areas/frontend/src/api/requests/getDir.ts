import { TRequest, TRequestParams, Item } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type GetDirRequestInput = {
    spaceId: string;
    dirId: string;
};

type GetDirRequestResult = {
    items: Item[]
};


const getDir: TRequest<TRequestParams<GetDirRequestInput>, GetDirRequestResult> = ({ input, config }) => {
    const spaceId = input?.spaceId
    const dirId = input?.dirId
    return instance.get(`get_dir/${spaceId}/${dirId}`, { ...config });
};

export function useGetDirLazy() {
    return useRequestLazy<TRequestParams<GetDirRequestInput>, {}>({
        request: getDir
    });
}

export function useGetDir(params: TRequestParams<GetDirRequestInput>) {
    return useRequest({ service: useGetDirLazy(), params });
}
