import os
import random
import asyncio
from alith import Agent
from dotenv import load_dotenv
import contextlib
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json

# Scheduler must be global so it's accessible and startable
scheduler = AsyncIOScheduler()
DATA_FILE = "reminders.json"

@contextlib.contextmanager
def suppress_native_output():
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stdout_fd = os.dup(1)
        old_stderr_fd = os.dup(2)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        yield
    finally:
        for fd in (1, 2):
            try:
                os.dup2(old_stdout_fd if fd == 1 else old_stderr_fd, fd)
            except OSError:
                pass
        os.close(old_stdout_fd)
        os.close(old_stderr_fd)
        os.close(devnull)

# Load environment variables
load_dotenv()

def save_reminders():
    data = {
        "interval_reminders": interval_reminders,
        "scheduled_reminders": {
            task: job.next_run_time.strftime("%H:%M") if job.next_run_time else "unknown"
            for task, job in scheduled_reminders.items()
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_reminders():
    if not os.path.exists(DATA_FILE):
        return {}, {}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data.get("interval_reminders", {}), data.get("scheduled_reminders", {})

# Initialize Alith AI Agent
agent = Agent(
    name="AI Reminder Buddy",
    model="gpt-4",
    preamble="""
    You are a helpful and encouraging AI Reminder Buddy.
    Your job is to remind students about their important tasks, study breaks,
    and keep them motivated with fun messages."""
)

motivations = [
    "💪 You've got this! Small steps lead to big progress!",
    "🎯 Stay focused! Your future self will thank you.",
    "🔥 You're on fire! Keep crushing it!",
    "😎 Don't forget — YOU are awesome!",
    "🌈 Every step forward is a win!"
]

# State
scheduled_reminders = {}  # task_name: (hour, minute)
interval_reminders = {}   # task_name: interval
reminder_tasks = {}       # task_name: asyncio.Task
paused = asyncio.Event()
paused.set()

# --- Reminder Functions ---
def time_reminder(task):
    motivation = random.choice(motivations)
    with suppress_native_output():
        message = agent.prompt(f"Give a motivational message for the task: {task}")
    print(f"\n⏰ Scheduled Reminder: {task}")
    print(f"🌟 {motivation}")
    print(f"🤖 AI Wisdom: {message}")

async def reminder_loop(task, interval):
    while True:
        await paused.wait()
        motivation = random.choice(motivations)
        with suppress_native_output():
            alith_message = agent.prompt(f"Give me a motivational message for a student working on {task}")
        print(f"\n🔔 Interval Reminder: {task}")
        print(f"🌟 {motivation}")
        print(f"🤖 AI Wisdom: {alith_message}")
        await asyncio.sleep(interval)

# --- Command Handling ---
async def listen_for_commands():
    while True:
        command = await asyncio.to_thread(input, "\nEnter your commands here - Type 'help' for menu: ")
        command = command.strip().lower()

        if command in ["stop", "exit"]:
            print("\n🛑 Stopping all reminders...")
            for task in reminder_tasks.values():
                task.cancel()
            scheduler.remove_all_jobs()
            scheduler.shutdown(wait=False)
            save_reminders()
            break

        elif command == "add":
            paused.clear()

            task_name = await asyncio.to_thread(input, "Task name: ")
            task_name = task_name.strip().lower()

            reminder_type = await asyncio.to_thread(input, "Reminder type? Type 'interval' or 'time': ")
            reminder_type = reminder_type.strip().lower()

            if reminder_type == "interval":
                try:
                    interval_str = await asyncio.to_thread(input, "Interval in seconds: ")
                    interval = int(interval_str.strip())

                    if task_name in interval_reminders:
                        print("⚠️ You already have a reminder for that task.")
                    else:
                        interval_reminders[task_name] = interval
                        task = asyncio.create_task(reminder_loop(task_name, interval))
                        reminder_tasks[task_name] = task
                        print(f"✅ Added reminder for '{task_name}' every {interval} seconds.")
                except ValueError:
                    print("❌ Please enter a valid number for interval.")

            elif reminder_type == "time":
                clock_time = await asyncio.to_thread(input, "Time (HH:MM, 24h format): ")

                try:
                    hour, minute = map(int, clock_time.strip().split(":"))
                    job = scheduler.add_job(time_reminder, 'cron', hour=hour, minute=minute, args=[task_name])
                    scheduled_reminders[task_name] = job
                    print(f"✅ Scheduled time-based reminder for '{task_name}' at {hour:02}:{minute:02} daily.")
                except ValueError:
                    print("❌ Invalid time format. Use HH:MM in 24-hour format.")

            else:
                print("❌ Unknown reminder type. Please enter 'interval' or 'time'.")

            paused.set()

        elif command == "remove":
            paused.clear()

            task_name = await asyncio.to_thread(input, "Task name: ")
            task_name = task_name.strip().lower()

            removed = False

            if task_name in interval_reminders:
                interval_reminders.pop(task_name)
                task = reminder_tasks.pop(task_name, None)
                if task:
                    task.cancel()
                print(f"✅ {task_name} (interval) has been removed.")
                if not interval_reminders:
                    print(f"You have NO Interval reminders - Type 'add' to add more reminders: ")
                removed = True

            if task_name in scheduled_reminders:
                job = scheduled_reminders.pop(task_name)
                job.remove()
                print(f"✅ {task_name} (time-based) has been removed.")
                removed = True

                if not scheduled_reminders:
                    print(f"You have NO Scheduled reminders - Type 'add' to add more reminders: ")
            if not removed:
                print(f"❌ {task_name} is not in your reminders.")

            paused.set()

        elif command == "list":
            paused.clear()

            if interval_reminders:
                print("\n🔁 Interval Reminders:")
                for key, value in interval_reminders.items():
                    print(f"🔔 {key} — every {value} seconds")

            if scheduled_reminders:
                print("\n⏰ Time-Based Reminders:")
                for task_name, job in scheduled_reminders.items():
                    next_time = job.next_run_time.strftime("%H:%M") if job.next_run_time else "unknown"
                    print(f"🔔 {task_name} — next at {next_time}")

            if not interval_reminders and not scheduled_reminders:
                print("📭 No reminders set.")

            paused.set()

        elif command == "help":
            paused.clear()
            print("""
📖 Commands:
- add: Add a new reminder
- remove: Delete a reminder
- list: Show current reminders
- stop: Stop all reminders
- help: Show this help menu
""")
            paused.set()

        else:
            print("❓ Unknown command.")

# --- Main Program ---
async def main():
    scheduler.start()

    global interval_reminders, scheduled_reminders, reminder_tasks
    interval_reminders, scheduled_info = load_reminders()
    scheduled_reminders = {}

    existing_reminders = False

    for task_name, time_str in scheduled_info.items():
        try:
            hour, minute = map(int, time_str.split(":"))
            job = scheduler.add_job(time_reminder, 'cron', hour=hour, minute=minute, args=[task_name])
            scheduled_reminders[task_name] = job
            print(f"🔄 Loaded scheduled reminder '{task_name}' at {hour:02}:{minute:02}")
            existing_reminders = True
        except Exception as e:
            print(f"⚠️ Failed to load scheduled reminder {task_name}: {e}")

    # Recreate interval reminder asyncio tasks
    reminder_tasks = {}
    for task_name, interval in interval_reminders.items():
        task = asyncio.create_task(reminder_loop(task_name, interval))
        reminder_tasks[task_name] = task
        print(f"🔄 Loaded interval reminder '{task_name}' every {interval} seconds")
        existing_reminders = True

    if (existing_reminders):
        paused.clear()

    print("👋 Hi! I'm your AI Reminder Buddy. Let's set up your reminders! 🚨")
    first_task = await asyncio.to_thread(input, "What task should I remind you about first? (Type 'no' to pass): ")
    first_task = first_task.strip()

    if (first_task == "no"):
        print("🕒 You have NOT added a reminder yet — type 'add' at any time to create one.")

    else:
        first_task.lower()
        reminder_type = await asyncio.to_thread(input, "Reminder type? Type 'interval' or 'time': ")
        reminder_type = reminder_type.strip().lower()

        if reminder_type == "interval":
            interval = int(await asyncio.to_thread(input, "Interval in seconds: "))
            interval_reminders[first_task] = interval
            reminder_tasks[first_task] = asyncio.create_task(reminder_loop(first_task, interval))
            print(f"✅ Interval reminder for '{first_task}' every {interval} seconds added.")

        elif reminder_type == "time":
            clock_time = await asyncio.to_thread(input, "Time (HH:MM, 24h format): ")
            try:
                hour, minute = map(int, clock_time.strip().split(":"))
                job = scheduler.add_job(time_reminder, 'cron', hour=hour, minute=minute, args=[first_task])
                scheduled_reminders[first_task] = job
                print(f"✅ Time-based reminder for '{first_task}' set at {hour:02}:{minute:02} daily.")
            except ValueError:
                print("❌ Invalid time format. Please restart and use HH:MM format.")
                return
        else:
            print("❌ Invalid reminder type. Please restart and use 'interval' or 'time'.")
            return
    
    paused.set()
    save_reminders()

    await listen_for_commands()
    print("👋 All reminders stopped. Have a productive day!")

# --- Run ---
if __name__ == "__main__":
    asyncio.run(main())
