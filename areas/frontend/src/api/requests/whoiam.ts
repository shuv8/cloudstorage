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

const who: TRequest<TRequestParams<{}>, WhoAmIRequestResult> = ({ config, }) => {
    return instance.get(`whoiam`, { ...config });
};

export function useWhoAmILazy() {
    return useRequestLazy<TRequestParams<{}>, {}>({
        request: who,
    });
}

export function useWhoAmI(params: TRequestParams<{}>) {
    return useRequest({ service: useWhoAmILazy(), params });
}
