import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RenameRequestInput = {
    spaceId: string;
    itemId: string;
    new_name: string;
};

const rename: TRequest<TRequestParamsWithInput<RenameRequestInput>, {}> = ({ input, config }) => {
    const { spaceId, itemId } = input;
    return instance.put(`rename/${spaceId}/${itemId}`, { ...config });
};

export function useRenameLazy() {
    return useRequestLazy<TRequestParamsWithInput<RenameRequestInput>, {}>({
        request: rename,
    });
}

export function useRename(params: TRequestParamsWithInput<RenameRequestInput>) {
    return useRequest({ service: useRenameLazy(), params });
}
