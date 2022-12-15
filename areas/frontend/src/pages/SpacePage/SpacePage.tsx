import { AxiosError } from 'axios';
import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ITEM_ENTITY, useGetDir } from 'api';

type SpacePageProps = {
    dirId: string;
};

function SpacePage(props: SpacePageProps) {
    const { dirId } = props;

    const navigate = useNavigate();
    const { data, loading, error, fetch } = useGetDir({ input: { dirId } });

    React.useEffect(() => {
        fetch({ input: { dirId } });
    }, [fetch, dirId]);

    const handleOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
        const { id } = event.currentTarget;
        navigate({ pathname: `/dirs/${id}` });
    };

    if (loading) {
        return <>Загрузка...</>;
    }

    if (error) {
        if (error instanceof AxiosError) {
            return <>{error.response?.data.error}</>;
        }
    }

    return (
        <>
            {!!data?.path.length && (
                <div style={{ display: 'flex', marginBottom: '24px' }}>
                    {data.path.map(({ id, name }) => (
                        <>
                            <button role="button" id={id} onClick={handleOpen}>
                                {name}
                            </button>{' '}
                            /
                        </>
                    ))}
                </div>
            )}

            {data?.items.length ? (
                <>
                    {data?.items.map(({ id, entity, name }) => (
                        <React.Fragment key={id}>
                            <div>
                                {entity === ITEM_ENTITY.directory && (
                                    <button id={id} onClick={handleOpen}>
                                        Открыть
                                    </button>
                                )}{' '}
                                Entity: {entity} - Name: {name} - Id: {id}
                            </div>
                            <hr />
                        </React.Fragment>
                    ))}
                </>
            ) : (
                <>Папка пуста!</>
            )}
        </>
    );
}

function Mediator() {
    const { dirId } = useParams<'dirId'>();
    const navigate = useNavigate();

    if (!dirId) {
        navigate('/404');
        return null;
    }

    return <SpacePage dirId={dirId} />;
}

export { Mediator as SpacePage };
