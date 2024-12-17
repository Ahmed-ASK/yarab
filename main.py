from screeninfo import get_monitors  # Import a library to get screen resolution for positioning the app window
import json  # Import the JSON library to handle saving and loading data in JSON format
import eel  # Import the eel library for creating web apps using Python and JavaScript

# Initialize the web folder where the HTML/JS/CSS files are located
eel.init('web')

# Get the screen width and height of the current monitor
screenWidth = get_monitors()[0].width  # Get the total width of the monitor
screenHeight = get_monitors()[0].height  # Get the total height of the monitor

# Declare two lists to store tasks data
tasks = []  # This list will store all "to-do" tasks (pending tasks)
completedTasks = []  # This list will store all completed tasks


# This function is exposed to the JavaScript frontend, allowing it to call this from the browser
@eel.expose
def add_task(task):
    tasks.append(task)  # Add the new task to the tasks list
    eel.renderTasks(tasks)  # Call a frontend method to update the task list in the browser


# This function deletes a specific task from the tasks list, based on its index
@eel.expose
def delete_task(index):
    tasks.pop(index)  # Remove the task at the specified index from the tasks list
    eel.renderTasks(tasks)  # Call the frontend to update the task list in the browser


# This function marks a task as completed
@eel.expose
def done_task(task, index):
    completedTasks.append(task)  # Add the completed task to the completedTasks list
    tasks.pop(index)  # Remove the task from the tasks list
    eel.renderTasks(tasks)  # Update the to-do task list in the browser
    eel.renderCompletedTasks(completedTasks)  # Update the completed tasks list in the browser


# This function deletes a task from the list of completed tasks
@eel.expose
def delete_completed_task(index):
    completedTasks.pop(index)  # Remove the completed task at the specified index
    eel.renderCompletedTasks(completedTasks)  # Update the completed tasks list in the browser


# This function re-renders both lists (tasks and completedTasks) in the frontend
@eel.expose
def render_tasks():
    # Call the JavaScript function to render the current tasks and completed tasks
    eel.renderTasks(tasks)  # Update the task list in the browser
    eel.renderCompletedTasks(completedTasks)  # Update the completed tasks in the browser


# This function saves all tasks (both pending and completed) into a JSON file
@eel.expose
def save():
    data = json.dumps({"tasks": tasks, "completedTasks": completedTasks},
                      indent=4)  # Convert the lists into a JSON-formatted string
    with open("Tasks.json", "w") as outfile:  # Open a file called "Tasks.json" in write mode
        outfile.write(data)  # Write the JSON string to the file


# This part of the code loads tasks data from the JSON file when the app starts
try:
    with open("Tasks.json", "r", encoding='utf-8-sig') as f:  # Open the "Tasks.json" file in read mode
        jsonLoaded = json.load(f)  # Read the JSON data into a Python dictionary
        tasks = jsonLoaded['tasks']  # Load the "tasks" list from the JSON data
        completedTasks = jsonLoaded['completedTasks']  # Load the "completedTasks" list from the JSON data
        render_tasks()  # Render the tasks in the frontend
except FileNotFoundError:  # If the JSON file doesn't exist
    print(
        "Tasks.json not found, JSON file will be created when app closes.")  # Inform the user the file will be created on exit
except json.JSONDecodeError:  # If there's an error in the structure of the JSON file
    print("Invalid JSON, JSON file will be updated when app closes.")  # Inform the user the file will be fixed on exit

# Start the eel (web-based) app and open the main HTML page
eel.start(
    'index.html',  # The main HTML file of the app
    size=(1024, 768),  # The size of the application window (1024x768 pixels)
    position=(  # Position the app window in the center of the screen
        (screenWidth // 2) - (1024 // 2),  # Calculate horizontal center position
        (screenHeight // 2) - (768 // 2)  # Calculate vertical center position
    )
)
