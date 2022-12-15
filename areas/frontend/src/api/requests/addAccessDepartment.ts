import { TRequest, TRequestParams, Access } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';

export type AddAccessDepartmentRequestInput = {
    itemId: string;
    department: string;
    viewOnly: boolean;
};

type AddAccessDepartmentRequestResult = { };


const addAccessDepartment: TRequest<TRequestParams<AddAccessDepartmentRequestInput>, AddAccessDepartmentRequestResult> = ({ input, config }) => {
    const itemId = input?.itemId
    const department = input?.department
    const viewOnly = input?.viewOnly
    return instance.put(`add_access/${itemId}/department/${department}?view_only=${viewOnly}`, { ...input }, { ...config });
};

export function useAddAccessDepartmentLazy() {
    return useRequestLazy<TRequestParams<AddAccessDepartmentRequestInput>, {}>({
        request: addAccessDepartment
    });
}

export function useAddAccessDepartment(params: TRequestParams<AddAccessDepartmentRequestInput>) {
    return useRequest({ service: useAddAccessDepartmentLazy(), params });
}
