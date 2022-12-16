import { AxiosError } from 'axios';
import React from 'react';
import { TRequest, TRequestParams, TRequestService } from '../types';

type UseRequestLazyProps<P extends TRequestParams<{}>, R> = {
    request: TRequest<P, R>;
};

export function useRequestLazy<P extends TRequestParams<{}>, R>({ request }: UseRequestLazyProps<P, R>) {
    const [data, setData] = React.useState<TRequestService<P, R>['data']>(null);
    const [loading, setLoading] = React.useState<TRequestService<P, R>['loading']>(false);
    const [error, setError] = React.useState<TRequestService<P, R>['error']>(null);
    const [fetched, setFetched] = React.useState<boolean>(false);
    const [called, setCalled] = React.useState<boolean>(false);

    const fetch: TRequestService<P, R>['fetch'] = React.useCallback(
        async (params: P) => {
            try {
                setFetched(false);
                setCalled(true);
                setLoading(true);
                setData((await request(params)).data);
            } catch (error) {
                if (error instanceof AxiosError) {
                    setError(error);
                } else {
                    setError(new Error('Произошла непредвиденная ошибка'));
                }
            } finally {
                setLoading(false);
                setFetched(true);
            }
        },
        [request]
    );

    return {
        data,
        loading,
        error,
        fetch,
        fetched,
        called,
    };
}

type UseRequestProps<P extends TRequestParams<{}>, R> = {
    service: TRequestService<P, R>;
    params: P;
};

export function useRequest<P extends TRequestParams<{}>, R>({ service, params }: UseRequestProps<P, R>) {
    React.useEffect(() => {
        async function fetch() {
            await service.fetch(params);
        }

        fetch();
    }, []);

    return service;
}
