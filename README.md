# Flourish: Capstone Project for CS50W-2024

Flourish is more than just an event board. It's a vibrant community hub connecting event organizers and participants, fostering a space for unforgettable local experiences. Discover a diverse range of upcoming events, filter them based on your interests, and register with just a tap. Organizers can seamlessly create and manage their events, track registrations, and connect with attendees, all within one convenient platform.

## Technology Stack

This project was developed using Python's `Django` framework in the backend and `HTML`, `CSS` and `JavaScript` on the frontend. For styling purpose, `Bootstrap` (v5) is also on most of the UI elements. To store the data, I have used `sqlite3` database for its simplicity and light-weight nature.

## Distinctiveness and Complexity

Here is what I have implemented in the `Fluorish` appplication to ensure it is distinct from the other CS50 Projects in this course:

**Complex Event Model:** Flourish utilizes a robust Django data model with intricate relationships between users, events, categories, and registrations. This surpasses the simpler models used in "network" or "commerce" projects. It demands a thorough understanding of data normalization, relational database design principles, and proper implementation of Django Models and ForeignKey relationships.

![image](https://github.com/basuabhirup/flourish/assets/69730155/29b3d610-579e-4773-8d43-b6ecdbd9babb)

![image](https://github.com/basuabhirup/flourish/assets/69730155/111fe251-69d3-4c5c-9207-c2a24c812cc3)

<p align="center"><i>Data Model of the Application</i></p>


**Asynchronous User Experience:** Flourish prioritizes a smooth and responsive user experience by incorporating asynchronous operations on the frontend. This means minimizing page reloads and creating a more interactive feel. Techniques like the `fetch` API is used to achieve asynchronous data fetching and manipulation. This approach reduces latency and improves user interaction, making Flourish feel more dynamic and engaging.

**Role-Based Access Control (RBAC):** Flourish takes user privacy seriously. It implements robust user authentication with granular control over data access.  This ensures that unauthenticated users have limited access to information. Importantly, sensitive data like event attendee phone numbers is only accessible to event organizers.

**Mobile-First Design for All Devices:** Flourish prioritizes mobile responsiveness by adopting a mobile-first design approach. This means the UI is optimized for smaller screens first and then adapts to larger displays. CSS `Flexbox` and `Grid` layouts are utilized extensively, often leveraging Bootstrap classes, to ensure seamless UI rendering across a wide range of devices and screen sizes.  This approach ensures optimal user experience for all users regardless of the device they're using.

These features elevate Flourish from a simple event board to a comprehensive and user-centric platform and I believe that it showcases a deeper understanding of Django, JavaScript, and web development best practices as compared to the previous CS50 projects.

## File Structure

- This project has one application named `events` which is the entirety of this project
- The root `urls.py` file in `/community_event_board/urls.py` includes `events.urls` in its urlpatterns agains path `''` to make sure all the urls made in this prohect will be redirected to the `events` application
- The `events` application is installed in the project by including it in the `INSTALLED_APPS` list inside `/community_event_board/settings.py` file
- All the url paths are defined inside `events/urls.py` file and the paths specific to API responses are distinguished separately
- The overall data model is defined in `events/models.py` file
- All the view handler functions are defined in `events/views.py` file. This is the most important file and almost the entirety of the backend logic is defined in this file
- All the frontend jinja templates and `.html` UI files are defined in `/events/templates/events/` directory. The `layout.html` file is the base file and all other templates are extending this base layout.
- All the static assets like icons, images, stylesheets (CSS) and scripts (JavaScript) are defined in `/events/static/events/` directory which are getting fetched by the frontend as and when required

## How to Run the Application ?

1. Make sure that `Python` and `Django` is already installed in your system
2. Clone this repository to your local by using the following command in your system terminal:
   `git clone git@github.com:basuabhirup/flourish.git`
3. Go to the root directory of project using `cd flourish`
4. Make the migration files for the db model if required: `python3 manage.py makemigrations events`
5. Migrate the databse: `python3 manage.py migrate`
4. Run the the Django server by executing the following command: `python3 manage.py runserver`

