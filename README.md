
# ExerLogix
#### Video Demo:  <https://youtu.be/2vZCL6O0VAg>
#### Description:
This project aims to provide users with a comprehensive tool for tracking their fitness and weight-related data. It enables them to monitor their progress over time, set weight goals, and log their daily activities to get a better understanding of their health and fitness journey. Users can also delete data entries as needed, providing them with flexibility and control over their information.

My project is ExerLogix, a web application created with Python, HTML, Jinja, CSS, JavaScript, and  SQL using Flask web framework. It designed to help users manage their fitness goal and uses the Nutritionix API to  calculate the calories burned.

**The Vision of ExerLogix**

At its core, ExerLogix is driven by a vision to provide users with a holistic solution for tracking their fitness and weight-related data. It aims to simplify the often complex process of managing health goals and offers a user-friendly interface that anyone can navigate. The primary objectives of ExerLogix are as follows:

**Comprehensive Tracking:** ExerLogix enables users to monitor various aspects of their health and fitness journey, including weight changes, daily activities, and nutritional intake. This comprehensive approach helps users gain a better understanding of their overall well-being.

**Goal Setting and Progress Monitoring:** Setting achievable fitness goals is crucial, and ExerLogix empowers users to do just that. Whether it's shedding a few pounds, building muscle, or improving endurance, users can set weight goals and track their progress over time.

**User-Friendly Interface:** ExerLogix is designed with the user in mind. It offers a straightforward and intuitive interface, making it accessible to individuals of all fitness levels. The user-centric design ensures that tracking and managing fitness data is a hassle-free experience.

**Data Control and Flexibility:** Flexibility is key, and ExerLogix provides users with the ability to manage their data as they see fit. Users can easily delete data entries when needed, ensuring that they have full control over their information.

**Here's a breakdown of the key features and functionalities of the application:**
1. **Authentication System:** The web application has a login page and a register page. Users can create an account by registering and then log in using their credentials.

   ![Screenshot of a Authentication System.](/image/5.png)   
3. **Dashboard Page:** After logging in, users are directed to a dashboard page. This page provides an overview of important information, including:
    - User's current weight
    - Calories burned today
    - Today's date
    - Weight goal
     **Chart Display:** The dashboard page also includes two chart displays:
    - **Bar Chart:** This chart shows the calories burned per day, allowing users to track their daily progress in burning calories.
    - **Line Chart:** This chart displays the trend of the user's weight over time, helping users visualize their weight changes.
      ![Screenshot of a Dashboard.](/image/1.png) 
4. **Profile Page:** user's personal information
   ![Screenshot of a profile page.](/image/2.png)
6. **Weight Page:** Users can log their current weight on this page. They can also add and delete weight entries. When adding weight, the application records it with the current date. This feature allows users to track their weight changes over time.
   ![Screenshot of a weight manager page.](/image/3.png)
8. **Exercise Page:** Users can log their workouts on this page by entering workout details into a text box. The application uses an Nutritionix API to estimate the number of calories burned during the workout and records this information in the user's database. However, before using the exercise page, users are required to:
    *  Input their personal information on the profile page.
    * Log their current weight on the weight page.
  ![Screenshot of a exercise log page.](/image/4.png)
## How To Use
From the command line, first clone ExerLogix:
```
# Clone the respository
$ git clone https://github.com/Acceletor/ExerLogix.git

# install package
$ pip install -r requirements.txt

# run the program
$ flask run
```
