import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type RemoveAccessDepartmentRequestInput = {
    itemId: string;
    department: string;
};

type RemoveAccessDepartmentRequestResult = { };


const removeAccessDepartment: TRequest<TRequestParams<RemoveAccessDepartmentRequestInput>, RemoveAccessDepartmentRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    const department = input?.department
    return instance.delete(`remove_access/${itemId}/department/${department}`, { ...config });
};

export function useRemoveAccessDepartmentLazy() {
    return useRequestLazy<TRequestParams<RemoveAccessDepartmentRequestInput>, {}>({
        request: removeAccessDepartment
    });
}

export function useRemoveAccessDepartment(params: TRequestParams<RemoveAccessDepartmentRequestInput>) {
    return useRequest({ service: useRemoveAccessDepartmentLazy(), params });
}
