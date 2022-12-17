import { AxiosResponse } from 'axios';
import type { User } from '../schema';
import type { TRequest, TRequestParams } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

type WhoAmIRequestResult = {
    id: string;
    email: string;
    departments: string;
    root_space_id: string;
    root_dir_id: string;
};

const who: TRequest<TRequestParams<{}>, User> = async ({ config }) => {
    const result = await instance.get<{}, AxiosResponse<WhoAmIRequestResult>, {}>(`whoiam`, { ...config });
    const { root_dir_id, root_space_id } = result.data;
    const adaptedData = { rootDirId: root_dir_id, rootSpaceId: root_space_id };
    return { ...result, data: adaptedData };
};

export function useWhoAmILazy() {
    return useRequestLazy<TRequestParams<{}>, User>({
        request: who,
    });
}

export function useWhoAmI(params: TRequestParams<{}>) {
    return useRequest({ service: useWhoAmILazy(), params });
}
