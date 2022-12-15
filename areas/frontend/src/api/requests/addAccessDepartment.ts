import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type AddAccessDepartmentRequestInput = {
    itemId: string;
    department: string;
    viewOnly: boolean;
};

const addAccessDepartment: TRequest<TRequestParamsWithInput<AddAccessDepartmentRequestInput>, {}> = ({
    input,
    config,
}) => {
    const { itemId, department, viewOnly } = input;

    return instance.put(
        `add_access/${itemId}/department/${department}?view_only=${viewOnly}`,
        { ...input },
        { ...config }
    );
};

export function useAddAccessDepartmentLazy() {
    return useRequestLazy<TRequestParamsWithInput<AddAccessDepartmentRequestInput>, {}>({
        request: addAccessDepartment,
    });
}

export function useAddAccessDepartment(params: TRequestParamsWithInput<AddAccessDepartmentRequestInput>) {
    return useRequest({ service: useAddAccessDepartmentLazy(), params });
}
