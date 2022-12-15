import type { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

export type TRequestParams<I> = { input?: I; config?: AxiosRequestConfig<I> };
export type TRequestParamsWithInput<I> = TRequestParams<I> & { input: I };
export type TRequest<P extends TRequestParams<{}>, R> = (params: P) => Promise<AxiosResponse<R, P['input']>>;
export type TRequestError = { error: string };

export type TRequestService<P extends TRequestParams<{}>, R> = {
    data?: R | null;
    loading: boolean;
    error?: AxiosError<TRequestError, P['input']> | Error | null;
    fetch: (params: P) => Promise<void>;
};
