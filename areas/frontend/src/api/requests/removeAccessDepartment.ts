import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RemoveAccessDepartmentRequestInput = {
    itemId: string;
    department: string;
};

const removeAccessDepartment: TRequest<TRequestParamsWithInput<RemoveAccessDepartmentRequestInput>, {}> = ({
    input,
    config,
}) => {
    const { itemId, department } = input;
    return instance.delete(`remove_access/${itemId}/department/${department}`, { ...config });
};

export function useRemoveAccessDepartmentLazy() {
    return useRequestLazy<TRequestParamsWithInput<RemoveAccessDepartmentRequestInput>, {}>({
        request: removeAccessDepartment,
    });
}

export function useRemoveAccessDepartment(params: TRequestParamsWithInput<RemoveAccessDepartmentRequestInput>) {
    return useRequest({ service: useRemoveAccessDepartmentLazy(), params });
}
