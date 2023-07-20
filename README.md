<!DOCTYPE html>
<html>
<head>
 
</head>
<body>
  <h1>Restaurant Menu and Room Booking App</h1>
  <h1>Restaurant Menu App</h1>
  <h2>Prerequisites Of the project</h2>
  <ul>
    <li>Install Python by navigating to the link <a href="https://www.python.org/downloads/">Download Python</a></li>
    <li>Install the Pushbullet Google Chrome plugin: <a href="https://chrome.google.com/webstore/detail/pushbullet/chlffgpmiacpedhhbkiomidkjlcfhogd">Pushbullet</a></li>
    <li>Also install mobile app from playstore Pushbullet</li>
    <li>Create an account on Pushbullet and generate an access token in the settings. Replace the access token in the .env file with your generated token.</li>
    <li>Install the required dependencies mentioned in the project.</li>
    <li>Ensure you have Python and Django installed on your local machine.</li>
  </ul>

   <h2>Project Setup (Restaurant Menu)</h2>
   <li>Clone project from github</li>
   <li>Run requirements by the command <strong>pip3 install -r requirements.txt</strong></li>
   <li>Go the restaurants folder and then settings folder and open base.py file and change the database settings with your own local mysql settings</li>
   <li>Run the commands <strong>Python3 manage.py makemigrations <br> Python3 manage.py migrate</strong> </li>
   
  <h2>Project Entry Points</h2>
  <ol>
    <li><strong>Table Number Selection (Waiter):</strong> Waiters can log in to the application through the <a href="http://127.0.0.1:8000/admin_utiliti">Admin Utility</a> link to select the table number for the customers and proceed with taking orders.</li>
    <li><strong>Chef Interface:</strong> Chefs can log in to the application using the <a href="http://127.0.0.1:8000/chef_api/">Chef API</a> link. They can view the order details and send notifications to the admin to generate bills for completed orders.</li>
    <li><strong>Admin Interface:</strong> Admins can log in to the application through the <a href="http://127.0.0.1:8000/admin_login_api">Admin Login API</a> link. Admins can add table numbers, categories, and menu items. They can also view order details and generate bills for completed orders.</li>
    <li><strong>QR Code Access (Customers):</strong> Customers can scan the provided QR code using their mobile devices to access the menu and place orders.</li>
  </ol>

  <h2>Usage</h2>
  <ol>
    <li>Create a superuser by running the following command: <code>python manage.py createsuperuser</code>. This will allow you to log in as an admin.</li>
    <li>Access the admin interface at <a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a>. Here, you can add table numbers, categories, menu items, and manage orders.</li>
    <li>Log in as a chef using the Chef API link to view order details and send notifications to the admin.</li>
    <li>Waiters can log in to the Admin Utility link to select table numbers and proceed with taking orders.</li>
    <li>Customers can use their mobile devices to scan the provided QR code and access the menu. They can view menu items and place orders directly.</li>
  </ol>

  <h1>Room Booking App</h1>
  <h2>Description: </h2> <p>The Room Booking App is a web application that allows users to search for and book rooms in accommodation. It provides a seamless and user-friendly interface for both guests and accommodation owners to manage their reservations effectively.</p>
 <h2>Key Features:</h2>
<ul>
  <li>User Registration and Authentication: Users can sign up for an account, log in, and securely authenticate their identity to access personalized features.</li>
  
  <li>Room Search and Booking: Guests can search for available rooms based on their preferred location, dates, and other filters. Once a suitable room is found, they can easily book it and receive booking confirmation.</li>
  
  <li>Owner Dashboard: Accommodation owners can create an account, add their rooms to the system, manage room availability, and view incoming reservations through a dedicated dashboard.</li>
  
  <li>Room Details and Media: Users can view detailed information about each room, including room type, amenities, and images, to make informed booking decisions.</li>
  
  <li>User Profile: Users have their own profile pages where they can update personal information, view booking history, and manage preferences.</li>
  
  <li>Room Availability Calendar: Owners can easily manage their room availability using an intuitive calendar view.</li>
  
  <li>Admin Panel: An administrative panel is available to manage user accounts, listings, and resolve any issues that may arise.</li>
</ul>

<h2>Technologies Used:</h2>
<ul>
  <li>Backend: Python and Django web framework.</li>
  <li>Frontend: HTML, CSS, JavaScript, and Bootstrap for responsive design.</li>
  <li>Database: Mysql to store room listings, user data, and reservations.</li>
  <li>Cloudinary: To handle image uploads and storage.</li>
</ul>


  <h2>Project Entry Point</h2>
  <ul>
    <li>After the cloning the project now in the terminal execute the commnad <strong>python3 manage.py createsuperuser</strong></li>
    <li>The above command is to create a admin for the project.</li>
   <li>Execute the command <strong>python3 manage.py runserver</strong><small>(This will start local server) </small> and you can use the project.</li>
  </ul>
  
</body>
</html>




   
