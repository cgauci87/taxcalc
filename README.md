# Malta Salary Calculator

![](assets/images/responsive.png)

[Live application can be found here](https://.herokuapp.com/)

This is a Command Line Interface application designed for a user to calculate their salary tax. 
This project has been designed for educational purposes and uses the Code Institutes mock terminal to run.

---
## UX
To begin planning this project I started first with UX, designing the logic of the app, based on the user stories. 
As this is a command-line application there is no design featured as HTML & CSS has not been used.

### Strategy
User Stories:
- As a user, I want to be able to easily access the calculator.
- As a user, I want to be able to input my name.
- As a user, I want to be able to choose from options such as Student, Age, and Marital status.
- As a user, I want to be able to input my salary gross amount to calculate net income.
- As a user, I want to be able to see Weekly Net Income, Monthly Net Income, and Yearly Net Income.
- As a user, I want to be able to see the government bonus/COLA included.
- As a user, I want to be able to have the option to re-calculate any other salary.

### Structure
![Flowchart of Python logic](assets/images/flowchart.png)

As you can see from the flowchart above the logic has been based on the six key questions;

- Are you a Student? (Y/N)	
- Are you over 18? (Y/N)
- Born before 1962? (Y/N)
- Single, Married, or Parent? (S/M/P)
- Enter your income ? (Input amount)
- Would you like to calculate another salary? (Y/N)

---
## Features
The features included in this app are the following:

### Welcome Message:
- As soon as the user runs the app, a welcome message will be printed to the terminal. 
- This message also contains a disclaimer, where it explains that the amount produced in the calculation may vary due to other deductions or benefits.

![](assets/images/welcome_message.png)

### Thank you Message:
- As the user terminates the app, a thank you message will be printed to the terminal.

![](assets/images/thankyou_message.png)

---
