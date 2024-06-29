# Flourish: Backend

This is the codebase for the backend of Flourish project. Flourish is a vibrant community hub connecting event organizers and participants, fostering a space for unforgettable local experiences. The users cab discover a diverse range of upcoming events, filter them based on their interests, and register with just a tap. Organizers can seamlessly create and manage their events, track registrations, and connect with attendees, all within one convenient platform.

## File Structure

- This `Django` project has one application named `events` which is the entirety of this project
- The root `urls.py` file in `/community_event_board/urls.py` includes `events.urls` in its urlpatterns for path `''` to make sure all the urls made in this project will be redirected to the `events` application
- The `events` application is installed in the project by including it in the `INSTALLED_APPS` list inside `/community_event_board/settings.py` file
- The overall data model is defined in `events/models.py` file
- All the view handler functions are defined in `events/views.py` file. This is the most important file and almost the entirety of the backend logic is defined in this file

## How to Run the Application ?

1. Make sure that `Python` (v3.0+) and `Django` is already installed in your system
2. Clone this repository to your local by using the following command in your system terminal:
   `git clone git@github.com:basuabhirup/flourish_backend.git`
3. Go to the root directory of project using `cd flourish_backend`
4. Make the migration files for the db model if required: `python manage.py makemigrations events`
5. Migrate the databse: `python manage.py migrate`
6. Run the Django server in local by executing the following command: `python manage.py runserver`

