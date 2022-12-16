import type { TRequest, TRequestParamsWithInput } from '../types';
import { useRequest, useRequestLazy } from '../hooks/useRequest';
import { instance } from '../instance';
import { Department } from 'api';

export type GetDepartmentsRequestInput = {
    page: string;
    limit: string;
};

type GetSpacesRequestResult = {
    departments: Department[];
};

const getDepartment: TRequest<TRequestParamsWithInput<GetDepartmentsRequestInput>, GetSpacesRequestResult> = ({ config }) => {
    return instance.get('department', { ...config });
};

export function useGetDepartmentLazy() {
    return useRequestLazy<TRequestParamsWithInput<GetDepartmentsRequestInput>, GetSpacesRequestResult>({
        request: getDepartment,
    });
}

export function useGetDepartment(params: TRequestParamsWithInput<GetDepartmentsRequestInput>) {
    return useRequest({ service: useGetDepartmentLazy(), params });
}
