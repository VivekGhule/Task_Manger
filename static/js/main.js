//Task_Manager\static\main.js
document.addEventListener("DOMContentLoaded", () => {

    /* ---------------- ELEMENTS ---------------- */
    const form = document.getElementById("addTaskForm");
    const titleInput = document.getElementById("taskTitle");
    const descInput = document.getElementById("taskDescription");
    const priorityInput = document.getElementById("taskPriority");
    const dueDateInput = document.getElementById("taskDueDate");
    const dueTimeInput = document.getElementById("taskDueTime");
    const taskContainer = document.getElementById("tasksContainer");
    const emptyState = document.getElementById("emptyState");
    const addBtnText = document.getElementById("addBtnText");
    const addTaskBtn = document.getElementById("addTaskBtn");

    const totalEl = document.getElementById("totalTasks");
    const pendingEl = document.getElementById("pendingTasks");
    const completedEl = document.getElementById("completedTasks");

    const darkToggle = document.getElementById("darkModeToggle");
    const filterBtns = document.querySelectorAll(".filter-btn");
    const clearCompletedBtn = document.getElementById("clearCompletedBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    
    const successToast = document.getElementById("successToast");
    const errorToast = document.getElementById("errorToast");
    const toastMessage = document.getElementById("toastMessage");
    const errorMessage = document.getElementById("errorMessage");
    const connectionStatus = document.getElementById("connectionStatus");

    /* ---------------- STATE ---------------- */
    let tasks = [];
    let currentFilter = "all";

    /* ---------------- GET CSRF TOKEN ---------------- */
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    /* ---------------- TOAST NOTIFICATIONS ---------------- */
    function showToast(message, type = "success") {
        const toast = type === "success" ? successToast : errorToast;
        const msgEl = type === "success" ? toastMessage : errorMessage;
        
        msgEl.textContent = message;
        toast.classList.remove("hidden");
        
        setTimeout(() => {
            toast.classList.add("hidden");
        }, 3000);
    }

    /* ---------------- UPDATE CONNECTION STATUS ---------------- */
    function updateConnectionStatus(connected) {
        if (connected) {
            connectionStatus.innerHTML = `
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                Connected
            `;
            connectionStatus.className = "flex items-center gap-2 px-3 py-1 bg-green-500/10 text-green-700 rounded-full text-sm font-medium border border-green-300";
        } else {
            connectionStatus.innerHTML = `
                <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                Disconnected
            `;
            connectionStatus.className = "flex items-center gap-2 px-3 py-1 bg-red-500/10 text-red-700 rounded-full text-sm font-medium border border-red-300";
        }
    }

    /* ---------------- FETCH ALL TASKS ---------------- */
    async function fetchTasks() {
        try {
            const response = await fetch('/api/tasks/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) throw new Error('Failed to fetch tasks');
            
            const data = await response.json();
            tasks = data.tasks || data || [];
            updateConnectionStatus(true);
            renderTasks();
        } catch (error) {
            console.error('Error fetching tasks:', error);
            updateConnectionStatus(false);
            showToast('Failed to load tasks', 'error');
        }
    }

    /* ---------------- ADD TASK ---------------- */
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const title = titleInput.value.trim();
        if (!title) {
            showToast("Please enter a task title", "error");
            return;
        }

        // Disable button during submission
        addTaskBtn.disabled = true;
        addBtnText.textContent = "Adding...";

        const taskData = {
            title: title,
            description: descInput.value.trim(),
            priority: priorityInput.value,
            due_date: dueDateInput.value,
            due_time: dueTimeInput.value,
            completed: false
        };

        try {
            const response = await fetch('/api/tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(taskData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Failed to add task');
            }

            const data = await response.json();
            tasks.unshift(data.task || data);
            
            form.reset();
            renderTasks();
            showToast("Task added successfully!", "success");
            updateConnectionStatus(true);

        } catch (error) {
            console.error('Error adding task:', error);
            showToast(error.message || 'Failed to add task', 'error');
            updateConnectionStatus(false);
        } finally {
            addTaskBtn.disabled = false;
            addBtnText.textContent = "Add Task";
        }
    });

    /* ---------------- UPDATE TASK (Toggle Complete) ---------------- */
    async function toggleTaskComplete(taskId, completed) {
        // Validate taskId before making request
        if (!taskId || taskId === 'undefined' || taskId === 'NaN') {
            console.error('Invalid task ID:', taskId);
            showToast('Invalid task ID', 'error');
            await fetchTasks();
            return;
        }

        try {
            const response = await fetch(`/api/tasks/${taskId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ completed: completed })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to update task');
            }

            const task = tasks.find(t => (t._id || t.id) === taskId);
            if (task) {
                task.completed = completed;
                renderTasks();
                showToast(completed ? "Task completed!" : "Task reopened", "success");
            }
            updateConnectionStatus(true);

        } catch (error) {
            console.error('Error updating task:', error);
            showToast(error.message || 'Failed to update task', 'error');
            updateConnectionStatus(false);
            // Revert the UI
            await fetchTasks();
        }
    }

    /* ---------------- DELETE TASK ---------------- */
    async function deleteTask(taskId) {
        // Validate taskId before making request
        if (!taskId || taskId === 'undefined' || taskId === 'NaN') {
            console.error('Invalid task ID:', taskId);
            showToast('Invalid task ID', 'error');
            await fetchTasks();
            return;
        }

        if (!confirm('Are you sure you want to delete this task?')) return;

        try {
            const response = await fetch(`/api/tasks/${taskId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to delete task');
            }

            tasks = tasks.filter(t => (t._id || t.id) !== taskId);
            renderTasks();
            showToast("Task deleted!", "success");
            updateConnectionStatus(true);

        } catch (error) {
            console.error('Error deleting task:', error);
            showToast(error.message || 'Failed to delete task', 'error');
            updateConnectionStatus(false);
        }
    }

    /* ---------------- FILTER BUTTONS ---------------- */
    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            // Update active state
            filterBtns.forEach(b => {
                b.classList.remove("active", "bg-indigo-600", "text-white", "shadow-md");
                b.classList.add("text-gray-600");
                b.setAttribute("aria-selected", "false");
            });
            
            btn.classList.add("active", "bg-indigo-600", "text-white", "shadow-md");
            btn.classList.remove("text-gray-600");
            btn.setAttribute("aria-selected", "true");

            currentFilter = btn.dataset.filter;
            renderTasks();
        });
    });

    /* ---------------- CLEAR COMPLETED ---------------- */
    clearCompletedBtn.addEventListener("click", async () => {
        const completedTasks = tasks.filter(t => t.completed);
        
        if (completedTasks.length === 0) {
            showToast("No completed tasks to clear", "error");
            return;
        }

        if (!confirm(`Delete ${completedTasks.length} completed task(s)?`)) return;

        try {
            // Delete all completed tasks
            const deletePromises = completedTasks.map(task => {
                const taskId = task._id || task.id;
                
                // Skip if no valid ID
                if (!taskId || taskId === 'undefined' || taskId === 'NaN') {
                    console.error('Invalid task ID for deletion:', task);
                    return Promise.resolve();
                }
                
                return fetch(`/api/tasks/${taskId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                });
            });

            await Promise.all(deletePromises);
            
            tasks = tasks.filter(t => !t.completed);
            renderTasks();
            showToast(`${completedTasks.length} task(s) cleared!`, "success");
            updateConnectionStatus(true);

        } catch (error) {
            console.error('Error clearing tasks:', error);
            showToast('Failed to clear tasks', 'error');
            updateConnectionStatus(false);
            await fetchTasks();
        }
    });

    /* ---------------- DARK MODE ---------------- */
    if (darkToggle) {
        const isDark = localStorage.getItem("darkMode") === "true";
        if (isDark) {
            document.documentElement.classList.add("dark");
            darkToggle.textContent = "☀️ Light";
        }

        darkToggle.addEventListener("click", () => {
            document.documentElement.classList.toggle("dark");
            const isDarkNow = document.documentElement.classList.contains("dark");
            localStorage.setItem("darkMode", isDarkNow);
            darkToggle.textContent = isDarkNow ? "☀️ Light" : "🌙 Dark";
        });
    }

    /* ---------------- FILTER TASKS ---------------- */
    function getFilteredTasks() {
        switch (currentFilter) {
            case "pending":
                return tasks.filter(t => !t.completed);
            case "completed":
                return tasks.filter(t => t.completed);
            case "high":
                return tasks.filter(t => t.priority === "high");
            default:
                return tasks;
        }
    }

    /* ---------------- GET PRIORITY BADGE ---------------- */
    function getPriorityBadge(priority) {
        const badges = {
            low: { color: "bg-green-100 text-green-700", icon: "🌿", text: "Low" },
            medium: { color: "bg-amber-100 text-amber-700", icon: "⚠️", text: "Medium" },
            high: { color: "bg-red-100 text-red-700", icon: "🔥", text: "High" }
        };
        const badge = badges[priority] || badges.medium;
        return `<span class="text-xs px-2 py-1 rounded ${badge.color} font-medium">${badge.icon} ${badge.text}</span>`;
    }

    /* ---------------- FORMAT DATE ---------------- */
    function formatDate(dateString) {
        if (!dateString) return "";
        const date = new Date(dateString);
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);

        today.setHours(0, 0, 0, 0);
        tomorrow.setHours(0, 0, 0, 0);
        date.setHours(0, 0, 0, 0);

        if (date.getTime() === today.getTime()) return "📅 Today";
        if (date.getTime() === tomorrow.getTime()) return "📅 Tomorrow";
        
        const isOverdue = date < today;
        const formatted = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        return isOverdue ? `<span class="text-red-500">⚠️ 📅 ${formatted} (Overdue)</span>` : `📅 ${formatted}`;
    }

   /* ---------------- FORMAT TIME WITH OVERDUE CHECK ---------------- */
    function formatTime(timeString, dateString) {
        if (!timeString || !dateString) return "";
    
        const now = new Date();
    
        // ----- Parse task date -----
        const taskDate = new Date(dateString);
        taskDate.setHours(0, 0, 0, 0);
    
        // ----- Parse task time -----
        const [h, m] = timeString.split(":").map(Number);
        const taskDateTime = new Date(taskDate);
        taskDateTime.setHours(h, m, 0, 0);
    
        // ----- Format time (12-hour) -----
        let hours = h % 12 || 12;
        const period = h >= 12 ? "PM" : "AM";
        const minutes = m.toString().padStart(2, "0");
    
        const formattedTime = `⏰ ${hours}:${minutes} ${period}`;
    
        // ----- Normalize today's date -----
        const today = new Date();
        today.setHours(0, 0, 0, 0);
    
        // ----- CONDITIONS -----
        const isPastDate = taskDate < today;
        const isTodayPastTime = taskDate.getTime() === today.getTime() && taskDateTime < now;
    
        if (isPastDate || isTodayPastTime) {
            return `<span class="text-red-500 font-semibold">⚠️ ${formattedTime} (Time Passed)</span>`;
        }
    
        return formattedTime;
    }




    /* ---------------- UPDATE STATS ---------------- */
    function updateStats() {
        totalEl.textContent = tasks.length;
        pendingEl.textContent = tasks.filter(t => !t.completed).length;
        completedEl.textContent = tasks.filter(t => t.completed).length;
    }

    /* ---------------- RENDER TASKS ---------------- */
    function renderTasks() {
        taskContainer.innerHTML = "";
        const filteredTasks = getFilteredTasks();

        if (tasks.length === 0) {
            emptyState.classList.remove("hidden");
            taskContainer.innerHTML = "";
        } else if (filteredTasks.length === 0) {
            emptyState.classList.add("hidden");
            taskContainer.innerHTML = `
                <div class="text-center py-12 bg-white rounded-2xl shadow-lg border border-gray-100">
                    <svg class="w-12 h-12 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
                    </svg>
                    <p class="text-gray-400 text-lg font-medium">No tasks match this filter</p>
                </div>
            `;
        } else {
            emptyState.classList.add("hidden");

            filteredTasks.forEach(task => {
                // Get task ID - support both MongoDB _id and regular id
                const taskId = task._id || task.id;
                
                // Skip if no valid ID
                if (!taskId) {
                    console.error('Task missing ID:', task);
                    return;
                }
                
                const card = document.createElement("div");
                card.className = `bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 transition-all hover:shadow-xl ${task.completed ? 'opacity-75' : ''}`;

                card.innerHTML = `
                    <div class="flex justify-between items-start gap-4">
                        <div class="flex items-start gap-3 flex-1">
                            <input type="checkbox" ${task.completed ? "checked" : ""} 
                                data-task-id="${taskId}"
                                class="task-checkbox mt-1 w-5 h-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer" />
                            
                            <div class="flex-1 space-y-2">
                                <h4 class="font-semibold text-lg ${task.completed ? "line-through text-gray-400 dark:text-gray-500" : "text-gray-800 dark:text-gray-100"}">
                                    ${escapeHtml(task.title)}
                                </h4>
                                ${task.description ? `<p class="text-sm text-gray-600 dark:text-gray-400">${escapeHtml(task.description)}</p>` : ""}
                                
                                <div class="flex flex-wrap gap-2 items-center">
                                    ${getPriorityBadge(task.priority)}
                                    ${task.due_date ? `<span class="text-xs text-gray-500">${formatDate(task.due_date)}</span>` : ""}
                                    ${task.due_time ? `<span class="text-xs text-gray-500">${formatTime(task.due_time,task.due_date)}</span>` : ""}
                                </div>
                            </div>
                        </div>

                        <button class="delete-btn text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-lg transition" 
                                data-task-id="${taskId}"
                                title="Delete task">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                        </button>
                    </div>
                `;

                taskContainer.appendChild(card);
            });

            // Add event listeners to checkboxes
            document.querySelectorAll('.task-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', (e) => {
                    const taskId = e.target.dataset.taskId;
                    const completed = e.target.checked;
                    toggleTaskComplete(taskId, completed);
                });
            });

            // Add event listeners to delete buttons
            document.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const taskId = e.currentTarget.dataset.taskId;
                    deleteTask(taskId);
                });
            });
        }

        updateStats();
    }

    /* ---------------- ESCAPE HTML ---------------- */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /* ---------------- INITIALIZE ---------------- */
    fetchTasks();

});


