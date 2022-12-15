import { TRequest, TRequestParams, Space } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type GetSpacesRequestInput = {};

type GetSpacesRequestResult = {
    spaces: Space[]
};


const getSpaces: TRequest<TRequestParams<GetSpacesRequestInput>, GetSpacesRequestResult> = ({ config }) => {
    return instance.get('get_spaces', { ...config });
};

export function useGetSpacesLazy() {
    return useRequestLazy<TRequestParams<GetSpacesRequestInput>, {}>({
        request: getSpaces
    });
}

export function useGetSpaces(params: TRequestParams<GetSpacesRequestInput>) {
    return useRequest({ service: useGetSpacesLazy(), params });
}
