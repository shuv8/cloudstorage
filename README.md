# -mephi-data-manage-system

Web application of "Documents storing system" <MEPhI course>

## Frontend

Корень: sud_frontend
Запуск: npm start

## Backend

🌐 - Работает Frontend
🟢 - Работает API

### Admin

🟡 1) `/department` - Get department list

🟡 2) `/department` - Add new department

🟡  3) `/department` - Delete department

🟡  4) `/department/users` - Get users in department

🟡  5) `/department/users` - Add users to department

🟡  6) `/department/users` - Remove users from department

🟡  7) `/users` - Get user list

🔴 8) `/all_workspaces` - All workspace for users

🔴 8) `/unarchive` - Unarchive workspace

🔴 9) `/delete` - Delete workspace forever

### User

#### User

🌐🟢 1) `/registration` - Registration

🌐🟢 2) `/login` - Login

🌐🟢 2) `/logout` - LogOut

🌐🟢 20) `/whoiam` - Who I am

#### Search

[NEED REFACTOR] 3) `/search_for` - Search [ACCESS: Show all, open only workspaces with access]

#### Workspaces

🌐🟢 4) `/get_workspaces` - Get workspaces

🌐🟢 5) `/get_workspace/<space_id>` - Get workspace [ACCESS: All access only]

🌐🟢 6) `/workspace/add` - Add new workspace

🟢 7) `/workspace/<space_id>/archive` - Archive workspace [ACCESS: Author]

#### Branches 

🟢 8) `/branch/branch_id` - View branch [ACCESS: Access to workspace needed]

🟢 9) `/branch/<space_id>` - Create branch [ACCESS: Access to workspace needed]

🟢 10) `/branch/branch_id` - Remove branch [ACCESS: Author]

🟢 11) `/branch/branch_id/request` - Create pull request [ACCESS: Author]

#### Requests

🟢 12) `/request/request_id` - View request

🟢 13) `/request/request_id` - Close request

🟢 14) `/request/request_id/merge` - Merge request

🟢 15) `/request/request_id` - Change status of Request

#### Files

🔴 16) `/file` - Add file

🔴 17) `/file/<file_id>/view` - View file

🔴 18) `/rename/<space_id>/<item_id>` - Rename file

🔴 19) `/download/<item_id>` - Download file

#### Accesses

🔴 21) `/accesses/<space_id>` - Get all accesses

🔴 22) `/set_access/<space_id>` - Set access

🔴 23) `/reset_access/<space_id>` - Remove access

🔴 24) `/add_access/<space_id>/email/<email>` - Add access

🔴 25) `/remove_access/<space_id>/email/<email>` - Remove access

🔴 26) `/add_access/<space_id>/department/<department>` - Add access

🔴 27) `/remove_access/<space_id>/department/<department>` - Remove access

