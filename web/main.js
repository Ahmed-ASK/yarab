// Selects HTML elements using their IDs for interaction
const form = document.getElementById('todo-form');         // Form for adding new tasks
const input = document.getElementById('todo-input');       // Input box for task name
const list = document.getElementById('todo-list');         // List where tasks will appear
const completedList = document.getElementById('completed-list'); // Section for completed tasks

// Event listener: When the form is submitted
form.addEventListener('submit', function (e) {
    e.preventDefault(); // Prevents default web behavior (page refresh)
    const taskText = input.value.trim(); // Gets the input provided by the user and trims whitespace
    if (taskText) { // Checks that input is not empty
        eel.add_task(taskText); // Sends the task to the backend via eel
        input.value = ''; // Clears the input field
    }
});

// Automatically render saved tasks from backend upon page load
window.addEventListener('load', () => eel.render_tasks());

// Function: Updates (renders) the task list dynamically
function renderTasks(tasks) {
    list.innerHTML = ''; // Clears the current list to prevent duplicate entries

    // Iterates over every task and creates its HTML structure
    tasks.forEach((task, index) => {
        const li = document.createElement('li'); // Creates a list item for each task

        const span = document.createElement('span'); // Contains the task text
        span.innerText = task; // Sets the text
        span.style.maxWidth = '70%'; // Limits the width of text
        span.style.overflow = 'auto'; // Adds a scroll if the text is too large
        li.appendChild(span); // Appends the task text to the list item

        const div = document.createElement('div'); // Container for "Done" and "Delete" buttons

        // Done task button
        const doneButton = document.createElement('button');
        doneButton.textContent = 'Done'; // Button label
        doneButton.style.backgroundColor = 'green';
        doneButton.addEventListener('click', () => eel.done_task(task, index)); // Moves the task to completed list

        // Delete task button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete'; // Button label
        deleteButton.addEventListener('click', () => eel.delete_task(index)); // Deletes task from backend

        div.appendChild(doneButton); // Adds "Done" button to the div
        div.appendChild(deleteButton); // Adds "Delete" button to the div

        li.appendChild(div); // Appends the div to the list item
        list.appendChild(li); // Adds the list item to the task list
    });
}

// Function: Updates (renders) the completed tasks dynamically
function renderCompletedTasks(completedTasks) {
    completedList.innerHTML = ''; // Clears the completed tasks list

    completedTasks.forEach((task, index) => {
        const li = document.createElement('li'); // Creates a list item for the completed task

        const span = document.createElement('span'); // Displays completed task text
        span.innerText = task;
        span.style.maxWidth = '70%';
        span.style.overflow = 'auto';
        li.appendChild(span); // Adds task text to the list item

        const deleteCompletedButton = document.createElement('button'); // Button to delete completed task
        deleteCompletedButton.textContent = 'Delete';
        deleteCompletedButton.addEventListener('click', () => eel.delete_completed_task(index)); // Removes task from completed list

        li.appendChild(deleteCompletedButton); // Adds the delete button to the list item
        completedList.appendChild(li); // Appends the list item to the completed list
    });
}

// Save tasks to file when the page is closed
window.addEventListener("beforeunload", () => eel.save());

// Makes the functions accessible in Python (backend)
eel.expose(renderTasks);
eel.expose(renderCompletedTasks);