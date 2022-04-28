# finalproject
Final Software Project: Personal Finance Management Application

To execute the program, ensure correct libraries are installed, and execute the mainProgram.py file.

Version History:

Version 0.1 Alpha
- Login system completed

Version 0.2 Alpha
- Encryption added to Login System (bcrypt module)
	- Register (encrypt password & security answer)
	- Login (decrypt password)
	- Reset Password (decrypt security answer + encrypt new password)

Version 0.3 Alpha
- Settings Created (Options: Change Salary, Change Security Details, Change Password, Delete User)
	- Includes Encryption for Change Security Answer & Change Password
- Security Addition: Account locks if user inputs password incorrectly 5 times, forcing for a reset of password
- Security Addition: Require entry of Security Answer Twice on Registration
- Username on Login no longer case-sensitive

Version 0.4 Alpha
- Checks if local dataset exists for storing finances (Offline Only)
- Database input for finances PARTIALLY works (Offline Only)
- Data Visualisation Partially Operational (Offline Only)

Version 0.5 Alpha
- Dataset input Functional (Offline)
- Data Visualisation Fully Functional (Offline)
	- More Details Section Added
	- Overview of Previous Years Added
- Bug Fix - Application now opens without Internet connection
	- On launch and when utilising certain features, application would error when not connected to the 	internet as the application would attempt to make a connection to the database despite not being used
- If user is not connected to the Internet, they will automatically be placed into Offline Mode

Version 0.6 Alpha
- Data Visualisation Graphs No Longer Show Finances with 0 Value
- Dataset input Functional (Online)
- Data Visualisation Fully Functional (Online)

Version 0.7 Alpha
- Reminder Section Created (Online + Offline)
	- Reminders Outputted in Date Order so urgent reminders appear at top
	- If there are reminders in next 2 days, user is prompted upon opening

Version 1.0 Beta
- Button Issue and other UI aesthetics fixed
- Disposable Spelling Corrected in UI Only

Version 1.1 Beta
- Clean Up of Code and Improved Commenting
	- Python files organised into appropriate folders
	- Monthly Bills and Disposable Income Python Files are now one as re-coded to be modular.
	- Commenting cleaned up and improved, more clear
	- Code cleaned up, unnecessary code removed as well as commented code removed

Version 1.2 Beta
- Bug Fix when opening reminders section with no reminders (Offline & Online)
	- Application wouldn’t break but Python would display an error saying a local variable was referenced 	before assignment.
- Change Colour of Drop Down Boxes when Viewing Expenditures

Version 1.3 Beta (Version 1.0 Final)
- Financial Recommendations Section Created (Online + Offline)
