This app is live at https://dice4000spring2019group2final.herokuapp.com/

Contains the following feature set:

Register:
- Self-serve account creation as either a student, faculty or admin
- Currently all permission levels are selectable at registration time for testing, obviously change this for production usage.

Login:
- Required for all features except Register. 
- Maybe allow anonymous users to search orgs in the future?

Search:
- Both orgs and users searches just return the whole table, paginated with 5 per page. 
- Future ideas: Advanced filtering, sortable columns, etc.

CRUD Users:
- Restricted to Admins only

CRUD Orgs:
- Restricted to Admins and faculty only
- Students may search and view orgs

Viewing records: 
- Accessible from Search Results UI

Editing records:
- Accessible from the View UI, if user has permissions

Deleting records:
- Accessible from the Edit UI, if user has permissions
- User is prompted to confirm deletion
