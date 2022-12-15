import type { Access } from '../schema';
import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type AccessesRequestInput = {
    itemId: string;
};

type AccessesRequestResult = {
    accesses: Access[];
};

const accesses: TRequest<TRequestParamsWithInput<AccessesRequestInput>, AccessesRequestResult> = ({
    input,
    config,
}) => {
    const { itemId } = input;

    return instance.get(`accesses/${itemId}`, { ...config });
};

export function useAccessesLazy() {
    return useRequestLazy<TRequestParamsWithInput<AccessesRequestInput>, {}>({
        request: accesses,
    });
}

export function useAccesses(params: TRequestParamsWithInput<AccessesRequestInput>) {
    return useRequest({ service: useAccessesLazy(), params });
}
