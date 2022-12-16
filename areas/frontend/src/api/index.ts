export * from './schema';

// Authentication
export * from './requests/registration';
export * from './requests/login';
export * from './requests/whoiam';

// Base
export * from './requests/getSpaces';
export * from './requests/getSpaceById';
export * from './requests/search';
export * from './requests/getDir';

// Accesses
export * from './requests/accesses';
export * from './requests/setAccessUrl';
export * from './requests/resetAccessUrl';
export * from './requests/addAccessEmail';
export * from './requests/removeAccessEmail';
export * from './requests/addAccessDepartment';
export * from './requests/removeAccessDepartment';

// Creation and View
export * from './requests/createDir';
// TODO: export * from './requests/createFile';
// TODO: export * from './requests/viewFile';
// TODO: export * from './requests/download';

// Manipulation
export * from './requests/rename';
export * from './requests/move';
export * from './requests/delete';
export * from './requests/copy';

// Departments
export * from './requests/getDepartment';
// TODO: export * from './requests/createDepartment';
// TODO: export * from './requests/deleteDepartment';
// TODO: export * from './requests/getDepartmentUsers';
// TODO: export * from './requests/createDepartmentUsers';
// TODO: export * from './requests/deleteDepartmentUsers';
// TODO: export * from './requests/getUser';