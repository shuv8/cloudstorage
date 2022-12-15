import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';
import { useGetSpaceByIdLazy } from 'api';

export type AccessesRequestInput = {
    itemId: string;
};

type AccessesRequestResult = {
    accesses: Access[]
};


const accesses: TRequest<TRequestParams<AccessesRequestInput>, AccessesRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    return instance.get(`accesses/${itemId}`,  { ...config });
};

export function useAccessesLazy() {
    return useRequestLazy<TRequestParams<AccessesRequestInput>, {}>({
        request: accesses
    });
}

export function useAccesses(params: TRequestParams<AccessesRequestInput>) {
    return useRequest({ service: useAccessesLazy(), params });
}
