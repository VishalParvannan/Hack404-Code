# Hack404-Code

🐶 Agent Fred – AI Reminder Assistant
Agent Fred is a personalized AI-powered reminder system created for Mini-Hacks #2: AI Agent. Built on top of the base program provided, it introduces both interval-based and scheduled timers, allowing users to receive motivational messages and timely reminders in a fun, friendly way.

Unlike traditional bots, Agent Fred is designed to feel approachable and human-like—modeled after a loyal dog who keeps you on track.

🔧 Features
🕒 Interval Reminders
Set repeating timers that send messages at a fixed interval (e.g., every 30 minutes).

⏰ Scheduled Reminders
Create one-time alerts that run at a specific time on the 24-hour clock—perfect for alarms or one-time tasks.

💬 Command Interface
Use simple commands to interact:

add – Add a new reminder

remove – Delete an existing reminder

list – View all active reminders

help – Show command guide

stop / exit – Exit the program safely

💾 Persistent Storage
Reminders are saved to a JSON file and reloaded when the program is restarted—no need to re-enter them.

🐾 Personality-Driven Agent
Instead of a boring AI bot, reminders come from Agent Fred, a cheerful virtual dog that adds warmth and charm to the experience.

⚙️ Challenges & Solutions
1. Unwanted AI Output in Terminal
Issue: When running in VSCode, the AI agent printed internal input/output messages directly to the terminal.
Fix: Implemented a suppress_native_output() method to hide irrelevant output and keep the interface clean.

2. Message Overlap During User Input
Issue: Reminders would appear while users were typing commands, breaking the input flow.
Fix: Refactored the program using asyncio, which lets reminders pause while the user types and resume afterward—creating a smooth, non-intrusive experience.

3. Loss of Timers on Exit
Issue: Reminders disappeared after stopping the program.
Fix: Added JSON-based persistence. Timers are saved and restored automatically when the program is rerun.

4. Impersonal AI Experience
Issue: The base AI felt too robotic and unengaging.
Fix: Designed Agent Fred, a dog-themed assistant who delivers messages with personality and encouragement—making it feel more like a companion than a tool.

✅ Summary
Agent Fred blends functionality with personality—offering a reliable reminder tool that feels alive. With support for both interval and scheduled timers, persistent data saving, and a friendly AI companion, it turns productivity into a more positive, motivating experience.

Whether you're working, studying, or just need a nudge now and then—Agent Fred’s got your back. 🐕



