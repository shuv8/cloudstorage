import { TRequest, TRequestParams, Item } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type SearchRequestConfig = {
    query: string;
};

type SearchRequestResult = {
    items: Item[]
};


const search: TRequest<TRequestParams<SearchRequestConfig>, SearchRequestResult> = ({ config }) => {
    return instance.get(`search`,  { ...config });
};

export function useSearchLazy() {
    return useRequestLazy<TRequestParams<SearchRequestConfig>, {}>({
        request: search
    });
}

export function useSearch(params: TRequestParams<SearchRequestConfig>) {
    return useRequest({ service: useSearchLazy(), params });
}
