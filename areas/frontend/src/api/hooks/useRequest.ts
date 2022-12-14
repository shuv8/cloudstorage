import { AxiosError } from 'axios';
import React from 'react';
import { TRequestParams } from '../types';

type UseRequestLazyProps<P extends TRequestParams<{}>, R> = {
    request(params: P): Promise<R>;
};

export function useRequestLazy<P extends TRequestParams<{}>, R>({ request }: UseRequestLazyProps<P, R>) {
    const [data, setData] = React.useState<R | null>();
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState<AxiosError | Error | null>(null);

    const fetch = React.useCallback(async (params: P) => {
        try {
            setLoading(true);
            setData(await request(params));
        } catch (error) {
            if (error instanceof AxiosError) {
                setError(error);
            } else {
                setError(new Error('Произошла непредвиденная ошибка'));
            }
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        data,
        loading,
        error,
        fetch,
    };
}

type UseRequestProps<P, R> = {
    state: {
        data: R | null | undefined;
        loading: boolean;
        error: AxiosError<unknown, any> | Error | null;
        fetch: (params: P) => Promise<void>;
    };
    params: P;
};

export function useRequest<P extends TRequestParams<{}>, R>({ state, params }: UseRequestProps<P, R>) {
    React.useEffect(() => {
        async function fetch() {
            await state.fetch(params);
        }

        fetch();
    }, []);

    return state;
}
