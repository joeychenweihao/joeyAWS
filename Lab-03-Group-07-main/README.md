# Lab-03-Group-07
1. Overview: EsportHeaven
   Goal: EsportHeaven is designed to provide a seamless and engaging platform where users can experience the thrill of esports. 
   The platform offers a user-friendly interface for participating in competitions, forums, and community activities.

   Main Features:
      General User Features:
         Home Page: View the platform's homepage.
         Competitions: Browse ongoing/upcoming esports competitions.
         Bulletins: Access announcements and updates.
         Forums: Engage with the community through posts and discussions.
      User Authentication:
         Registration: Register via email and set a password.
         Login/Logout: Securely log in and out of the platform.
      Forums:
         Create Posts: Authenticated users can create posts with images.
         Like/Unlike: Users can like/unlike posts and comments.
         Commenting: Add, delete, or quote comments on posts.
         Admin Privileges: Admins can delete or pin any post or comment.
      Admin Panel:
         Competition Management: Admins can create and manage competitions.
         Bulletin Management: Admins can create, edit, delete, and pin bulletins.
      Bulletins:
         Search and Sort: Search bulletins by keywords and sort by date.
         View Details: View full bulletin details.
      Competitions:
         Register: Users can register for competitions.
         Simulate Payment Errors: Test payment with invalid details (e.g., CVV or expired cards).
      User Profile:
         Modify Profile: Update profile details such as birthdate or nickname.
         View Activity: View joined competitions and personal posts/comments.

2. Installation Instructions and Configuration and Environment Setup:
   # How to run the web:
      1. python3.10 -m venv venv 
      2. source venv/bin/activate (for Mac User)
         venv\Scripts\activate (for Windows User)
      3. pip install -r requirements.txt
      4. /Applications/Python\ 3.10/Install\ Certificates.command
      5. python manage.py makemigrations
      6. python manage.py migrate
      7. python3 manage.py runserver  
      8. Then click the server exist in the terminal (i.e. http://127.0.0.1:8000/) + til_app/

   # Create superuser of Django server:
   python manage.py createsuperuser
3. Usage Instructions:
   Then click the server exist in the terminal (i.e. http://127.0.0.1:8000/) + til_app/

4. API Documentation
   Overview
   This project includes RESTful APIs that allow users to interact with the forum system, such as creating posts, liking posts and comments, and deleting content. Below is a detailed guide for each API endpoint.

   1. Create Post
   Endpoint: /api/create_post/
   Method: POST
   Authentication Required: Yes

   Request Parameters:
   title (string): The title of the post.
   content (string): The content of the post.
   image (file, optional): An image file associated with the post.

   2. Like a Post
   Endpoint: /api/like_post/{post_id}/
   Method: POST
   Authentication Required: Yes

   3. Like a Comment
   Endpoint: /api/like_comment/{comment_id}/
   Method: POST
   Authentication Required: Yes

   4. Create a Comment
   Endpoint: /api/create_comment/
   Method: POST
   Authentication Required: Yes

   Request Parameters:
   post_id (integer): The ID of the post to comment on.
   content (string): The content of the comment.

   5. Delete Post
   Endpoint: /api/delete_post/{post_id}/
   Method: POST
   Authentication Required: Yes

   6. Delete Comment
   Endpoint: /api/delete_comment/{comment_id}/
   Method: POST
   Authentication Required: Yes

   7. Pin a Post
   Endpoint: /pin_post/{post_id}/
   Method: POST
   Authentication Required: Yes (staff only)

