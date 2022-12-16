import type { Directory, File, DirectoryPath} from '../schema';
import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type GetDirRequestInput = {
    dirId: string;
};

type GetDirRequestResult = {
    items: (Directory | File)[];
    path: DirectoryPath[];
    name: string
};

const getDir: TRequest<TRequestParamsWithInput<GetDirRequestInput>, GetDirRequestResult> = ({ input, config }) => {
    const { dirId } = input;
    return instance.get(`get_dir/${dirId}`, { ...config });
};

export function useGetDirLazy() {
    return useRequestLazy<TRequestParamsWithInput<GetDirRequestInput>, GetDirRequestResult>({
        request: getDir,
    });
}

export function useGetDir(params: TRequestParamsWithInput<GetDirRequestInput>) {
    return useRequest({ service: useGetDirLazy(), params });
}
