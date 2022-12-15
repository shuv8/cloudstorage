import { TRequest, TRequestParams, Item } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type CreateDirRequestInput = {
    space_id: string;
    parent_id: string;
    new_directory_name: string;
};

type CreateDirRequestResult = {
    id: string
};


const createDir: TRequest<TRequestParams<CreateDirRequestInput>, CreateDirRequestResult> = ({ input, config }) => {
    return instance.post(`directory`, { ...input }, { ...config });
};

export function useCreateDirLazy() {
    return useRequestLazy<TRequestParams<CreateDirRequestInput>, {}>({
        request: createDir
    });
}

export function useCreateDir(params: TRequestParams<CreateDirRequestInput>) {
    return useRequest({ service: useCreateDirLazy(), params });
}
