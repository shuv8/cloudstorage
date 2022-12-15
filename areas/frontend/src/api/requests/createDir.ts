import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type CreateDirRequestInput = {
    space_id: string;
    parent_id: string;
    new_directory_name: string;
};

type CreateDirRequestResult = {
    id: string;
};

const createDir: TRequest<TRequestParamsWithInput<CreateDirRequestInput>, CreateDirRequestResult> = ({
    input,
    config,
}) => {
    return instance.post(`directory`, { ...input }, { ...config });
};

export function useCreateDirLazy() {
    return useRequestLazy<TRequestParamsWithInput<CreateDirRequestInput>, {}>({
        request: createDir,
    });
}

export function useCreateDir(params: TRequestParamsWithInput<CreateDirRequestInput>) {
    return useRequest({ service: useCreateDirLazy(), params });
}
