import type { Space } from '../schema';
import type { TRequest, TRequestParams } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

type GetSpacesRequestResult = {
    spaces: Space[];
};

const getSpaces: TRequest<TRequestParams<{}>, GetSpacesRequestResult> = ({ config }) => {
    return instance.get('get_spaces', { ...config });
};

export function useGetSpacesLazy() {
    return useRequestLazy<TRequestParams<{}>, {}>({
        request: getSpaces,
    });
}

export function useGetSpaces(params: TRequestParams<{}>) {
    return useRequest({ service: useGetSpacesLazy(), params });
}
