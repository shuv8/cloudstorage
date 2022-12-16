import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import {
    useLoginLazy,
    useRegistrationLazy,
    useGetSpacesLazy,
    useGetSpaceByIdLazy,
    useSearchLazy,
    useGetDirLazy,
    useAccessesLazy,
    useSetAccessUrlLazy,
    useResetAccessUrlLazy,
    useAddAccessEmailLazy,
    useRemoveAccessEmailLazy,
    useAddAccessDepartmentLazy,
    useRemoveAccessDepartmentLazy,
    useCreateDirLazy,
    useWhoAmILazy,
} from 'api';
import { SessionLayout } from 'layouts/SessionLayout';
import { SpacePage } from 'pages/SpacePage';

export function App() {
    // Authentication part
    const registrationService = useRegistrationLazy();
    console.log({ registrationService });
    const loginService = useLoginLazy();
    console.log({ loginService });
    const whoAmIService = useWhoAmILazy();
    console.log({ whoAmIService });

    // Base part
    const getSpacesService = useGetSpacesLazy();
    console.log({ getSpacesService });
    const getSpaceByIdService = useGetSpaceByIdLazy();
    console.log({ getSpaceByIdService });
    const searchService = useSearchLazy();
    console.log({ searchService });
    const getDirService = useGetDirLazy();
    console.log({ getDirService });

    // Accesses part
    const accessesService = useAccessesLazy();
    console.log({ accessesService });
    const setAccessUrlService = useSetAccessUrlLazy();
    console.log({ setAccessUrlService });
    const resetAccessUrlService = useResetAccessUrlLazy();
    console.log({ resetAccessUrlService });
    const addAccessEmailService = useAddAccessEmailLazy();
    console.log({ addAccessEmailService });
    const removeAccessEmailService = useRemoveAccessEmailLazy();
    console.log({ removeAccessEmailService });
    const addAccessDepartmentService = useAddAccessDepartmentLazy();
    console.log({ addAccessDepartmentService });
    const removeAccessDepartmentService = useRemoveAccessDepartmentLazy();
    console.log({ removeAccessDepartmentService });

    // Creation
    const createDirectoryService = useCreateDirLazy();
    console.log({ createDirectoryService });

    React.useEffect(() => {
        registrationService.fetch({
            input: {
                email: 'chocho@mail.ru',
                password: 'chochopass',
                role: 2,
                username: 'chocho',
            },
        });

        loginService.fetch({
            input: {
                email: 'chocho@mail.ru',
                password: 'chochopass',
            },
        });

        getSpacesService.fetch({
            input: {},
        });

        getSpaceByIdService.fetch({
            input: {
                spaceId: '3abd4de3-bcfe-47c6-ab49-fdf416406037',
            },
        });

        getDirService.fetch({
            input: {
                dirId: '44e85d06-b760-4698-ab0a-c9bb326cbb28',
            },
        });

        searchService.fetch({
            config: {
                params: {
                    query: 'dir',
                },
            },
        });

        addAccessDepartmentService.fetch({
            input: {
                itemId: '44e85d06-b760-4698-ab0a-c9bb326cbb28',
                department: 'club',
                viewOnly: false,
            },
        });

        accessesService.fetch({
            input: {
                itemId: '44e85d06-b760-4698-ab0a-c9bb326cbb28',
            },
        });

        createDirectoryService.fetch({
            input: {
                space_id: '3abd4de3-bcfe-47c6-ab49-fdf416406037',
                parent_id: '44e85d06-b760-4698-ab0a-c9bb326cbb28',
                new_directory_name: 'New name',
            },
        });

        whoAmIService.fetch({});
    }, []);

    if (whoAmIService.loading) {
        return null;
    }

    return (
        <BrowserRouter>
            {!!whoAmIService.data && (
                <SessionLayout>
                    <Routes>
                        <Route path="/" element={<Navigate to={`dirs/${whoAmIService.data.root_dir_id}`} />} />
                        <Route path="dirs/:dirId" element={<SpacePage />} />
                        <Route path="*" element={<div>404</div>} />
                    </Routes>
                </SessionLayout>
            )}
        </BrowserRouter>
    );
}
