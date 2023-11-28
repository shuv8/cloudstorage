# -mephi-data-manage-system
Web application of "Documents storing system" <MEPhI course>

## Backend API

### Admin

[CHECK] 1) `/department` - Get department list
[CHECK] 2) `/department` - Add new department
[CHECK] 3) `/department` - Delete department
[CHECK] 4) `/department/users` - Get users in department
[CHECK] 5) `/department/users` - Add users to department
[CHECK] 6) `/department/users` - Remove users from department
[CHECK] 7) `/user` - Get user list
[TODO] 8) `/unarchive` - Unarchive workspace
[TODO] 9) `/delete` - Delete workspace forever

### User

* Common *
  
[CHECK] 1) `/registration` - Registration

[CHECK] 2) `/login` - Login

[NEED REFACTOR] 3) `/search_for` - Search [ACCESS: Show all, open only workspaces with access]


* Workspaces *
  
[NEED REVIEW] 4) `/get_workspaces` - Get workspaces

[NEED REVIEW] 5) `/get_workspace/<space_id>` - Get workspace [ACCESS: All access only]

[TODO] 6) `/workspace/add` - Add new workspace

[TODO] 7) `/workspace/<space_id>/archive` - Archive workspace [ACCESS: Author]

* Branches *
  
[TODO] 8) `/branch/branch_id` - View branch [ACCESS: Access to workspace needed]

[TODO] 9) `/branch/<space_id>` - Create branch [ACCESS: Access to workspace needed]

[TODO] 10) `/branch/branch_id` - Remove branch [ACCESS: Author]

[TODO] 11) `/branch/branch_id/request` - Create pull request [ACCESS: Author]

* Requests *
  
[TODO] 12) `/request/request_id` - View request

[TODO] 13) `/request/request_id` - Close request

[TODO] 14) `/request/request_id/merge` - Merge request

[TODO] 15) `/request/request_id` - Change status of Request

* Files *
  
[NEED REFACTOR] 16) `/file` - Add file

[NEED REFACTOR] 17) `/file/<file_id>/view` - View file

[NEED REFACTOR] 18) `/rename/<space_id>/<item_id>` - Rename file

[NEED REFACTOR] 19) `/download/<item_id>` - Download file

[NEED REFACTOR] 20) `/whoiam` - Who am I

* Accesses *
[NEED REFACTOR] 21) `/accesses/<space_id>` - Get all accesses

[NEED REFACTOR] 22) `/set_access/<space_id>` - Set access

[NEED REFACTOR] 23) `/reset_access/<space_id>` - Remove access

[NEED REFACTOR] 24) `/add_access/<space_id>/email/<email>` - Add access

[NEED REFACTOR] 25) `/remove_access/<space_id>/email/<email>` - Remove access

[NEED REFACTOR] 26) `/add_access/<space_id>/department/<department>` - Add access

[NEED REFACTOR] 27) `/remove_access/<space_id>/department/<department>` - Remove access
