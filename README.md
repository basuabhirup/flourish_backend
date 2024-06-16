# Flourish: Capstone project for CS50W-2024

Flourish is more than just an event board. It's a vibrant community hub connecting event organizers and participants, fostering a space for unforgettable local experiences. Discover a diverse range of upcoming events, filter them based on your interests, and register with just a tap. Organizers can seamlessly create and manage their events, track registrations, and connect with attendees, all within one convenient platform.

## Technology Stack

This project was developed using Python's `Django` framework in the backend and `HTML`, `CSS` and `JavaScript (Vanilla)` on the frontend. For styling purpose, `Bootstrap (v5)` is also on most of the UI elements. To store the data, I have used `sqlite3` database for its simplicity and light-weight nature.

## Distinctiveness and Complexity
This capstone project (`Flourish`) transcends the limitations of past CS50 projects like "network" and "commerce" by delving deeper into user interactionand data-manipulation. Here's how Flourish stands out technically:
- Flourish incorporates a complex event model with detailed descriptions, categories, and registration functionality. This requires advanced data validation and manipulation on the backend using Django models and forms.
- There are 5 Data Models implementing an intricate relationships between users, events, categories, and registrations. This complexity surpasses the simpler models used in "network" or "commerce" projects, demanding a deeper understanding of data management and relational databases in Django.
- A special emphasis was given on enhancing the user experience (UX) of this platform. In most of the frontend, several custom modal components are implemented and most of the CRUD operations on the database is performed asynchronously using vanilla JavaScript in the frontend to ensure a smoother user experience limiting the number of page reloads
- The overall colour consistency, fonts and overall UI layout was designed as professionally as possible to make the platform appealling to new-age internet users
- The user authentication was implemented robustly in such a manner so that only very limited information is available publicy (for unauthenticated users). Also, the user sensitive information like event attendees mobile number is made visible only to the event host in order to protect their privacy
- Role based conditional UI rendering was implemented to make sure only previeleged users (like the owner of a group or the host of an event) can make edits and view some specific informations related to a particular event or group and the same checks are implemented in frontend as well as backend to make sure no unauthorized users can view any sensitive information
- The application is designed keeping mobile-first design in mind and most of the UI layout is implemented using CSS Flex and Grid via relevant bootstrap classes to make sure a wide range of users from devices with any size can access to all the information seamlessly

## File Structure
- This project has one application named `events` which is the entirety of this project
- The root `urls.py` file in `/community_event_board/urls.py` includes `events.urls` in its urlpatterns agains path `''` to make sure all the urls made in this prohect will be redirected to the `events` application
- The `events` application is installed in the project by including it in the `INSTALLED_APPS` list inside `/community_event_board/settings.py` file
- All the url paths are defined inside `events/urls.py` file and the paths specific to API responses are distinguished separately
- The overall data model is defined in `events/models.py` file
- All the view handler functions are defined in `events/views.py` file. This is the most important file and almost the entirety of the backend logic is defined in this file
- All the frontend jinja templates and `.html` UI files are defined in `/events/templates/events/` directory. The `layout.html` file is the base file and all other templates are extending this base layout.
- All the static assets like icons, images, stylesheets (CSS) and scripts (JavaScript) are defined in `/events/static/events/` directory which are getting fetched by the frontend as and when required