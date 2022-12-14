import { AxiosRequestConfig, AxiosResponse } from 'axios';

export type TRequestParams<I> = { config?: AxiosRequestConfig<I> };
export type TRequestParamsWithPayload<I> = TRequestParams<I> & { input: I };
export type TRequestResult<R> = R & { error?: string };
export type TRequest<P extends TRequestParams<{}>, R extends TRequestResult<{}>> = (
    params: P
) => Promise<AxiosResponse<TRequestResult<R>, AxiosRequestConfig<R>>>;
