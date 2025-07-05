# Hack404-Code
Mini-Hacks Code 
This program is for Mini-Hacks #2: AI Agent. It branches from the original base program given to us. In this program, users are allowed to create interval-based timers that send motivational messages for every interval and give reminders, using the Alith AI Agent. 

From the base program, I have added a new scheduled-based timer, which runs at a certain time in a 24-hour clock manner. This can act as an alarm, or a one-time reminder that doesn't need to be repeated. The timers are stored into two different timer dictionaries: one for interval and one for schedule, each containing the name of the timer and the timing. 

I have also added new commands, such as "add", "remove", "list", "help", and the "stop"/"exit". The "add" function allows one to add new reminders, the "remove" function allows one to remove reminders, and the "list" function lists the timers added split into its 2 categories. If the user needs help or doesn't understand the program, they can run the "help" command to get a list of the commands and its functions. The "stop/exit" commands are used to end the program and stop the remainders. 

To make it more accesible for longer periods of time, I added a json file containing the data of the reminders the user have previously set up. If the user ends the program (ex: via "stop"), and re-runs the program, the program will list the reminders previously added, and the option to add new ones. The previous reminders will function normally, even when running a new program. 

When running the code in VSCode, a new error popped up that printed the input into the AI Agent into the terminal. To suppress the commands from printing, I added a new method "suppress_native_output" to fix the issue. 

Another major issue I had to deal with was the input and reminder overlay. For example, when a user would add a new reminder, the other reminders would still show their messages, disrupting the user from writing anything. Thus, I had to rewire the entire program using Asyncio, while allowed me to pause and re-run the reminder messages while the user is entering their input. This made it easier for users to run their designed input/output. 

