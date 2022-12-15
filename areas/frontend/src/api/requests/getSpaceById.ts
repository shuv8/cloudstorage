import { TRequest, TRequestParams, Item } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type GetSpaceByIdRequestInput = {
    spaceId: string;
};

type GetSpaceByIdRequestResult = {
    items: Item[]
};


const getSpaceById: TRequest<TRequestParams<GetSpaceByIdRequestInput>, GetSpaceByIdRequestResult> = ({ input, config }) => {
    const spaceId = input?.spaceId
    return instance.get(`get_space/${spaceId}`, { ...config });
};

export function useGetSpaceByIdLazy() {
    return useRequestLazy<TRequestParams<GetSpaceByIdRequestInput>, {}>({
        request: getSpaceById
    });
}

export function useGetSpaceById(params: TRequestParams<GetSpaceByIdRequestInput>) {
    return useRequest({ service: useGetSpaceByIdLazy(), params });
}
