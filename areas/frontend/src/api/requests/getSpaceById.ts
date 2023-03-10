import type { Directory, File } from '../schema';
import { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type GetSpaceByIdRequestInput = {
    spaceId: string;
};

type GetSpaceByIdRequestResult = {
    items: (Directory | File)[];
};

const getSpaceById: TRequest<TRequestParamsWithInput<GetSpaceByIdRequestInput>, GetSpaceByIdRequestResult> = ({
    input,
    config,
}) => {
    const { spaceId } = input;
    return instance.get(`get_space/${spaceId}`, { ...config });
};

export function useGetSpaceByIdLazy() {
    return useRequestLazy<TRequestParamsWithInput<GetSpaceByIdRequestInput>, GetSpaceByIdRequestResult>({
        request: getSpaceById,
    });
}

export function useGetSpaceById(params: TRequestParamsWithInput<GetSpaceByIdRequestInput>) {
    return useRequest({ service: useGetSpaceByIdLazy(), params });
}
