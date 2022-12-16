import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type CopyRequestInput = {
    spaceId: string;
    itemId: string;
    target_space: string;
    target_directory: string;
};

const copy: TRequest<TRequestParamsWithInput<CopyRequestInput>, {}> = ({ input, config }) => {
    const { spaceId, itemId } = input;
    return instance.post(`copy/${spaceId}/${itemId}`, { ...config });
};

export function useCopyLazy() {
    return useRequestLazy<TRequestParamsWithInput<CopyRequestInput>, {}>({
        request: copy,
    });
}

export function useCopy(params: TRequestParamsWithInput<CopyRequestInput>) {
    return useRequest({ service: useCopyLazy(), params });
}
