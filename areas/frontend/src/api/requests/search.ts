import type { Directory, File } from '../schema';
import type { TRequest, TRequestParams } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

type SearchRequestResult = {
    items: (Directory | File)[];
};

const search: TRequest<TRequestParams<{}>, SearchRequestResult> = ({ config }) => {
    return instance.get(`search`, { ...config });
};

export function useSearchLazy() {
    return useRequestLazy<TRequestParams<{}>, {}>({
        request: search,
    });
}

export function useSearch(params: TRequestParams<{}>) {
    return useRequest({ service: useSearchLazy(), params });
}
