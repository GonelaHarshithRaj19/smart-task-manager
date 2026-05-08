/**
 * Smart Task Manager - Main JavaScript
 * Handles task management, real-time updates, and WebSocket communication
 */

// Initialize Socket.IO connection
let socket = null;
if (window.io) {
    try {
        socket = io();
    } catch (error) {
        console.warn('Socket.IO initialization failed:', error);
    }
} else {
    console.warn('Socket.IO client library is not loaded. Real-time updates will be disabled.');
}

// DOM Elements
const taskForm = document.getElementById('taskForm');
const tasksTableBody = document.getElementById('tasksTableBody');
const notificationArea = document.getElementById('notificationArea');
const editModal = document.getElementById('editModal');
const editForm = document.getElementById('editForm');
const closeModal = document.querySelector('.close');
const cancelBtn = document.getElementById('cancelBtn');
const statusFilter = document.getElementById('statusFilter');
const priorityFilter = document.getElementById('priorityFilter');

// Store for tasks
let allTasks = [];
let currentFilters = {
    status: '',
    priority: ''
};

/**
 * Initialize event listeners
 */
function initEventListeners() {
    taskForm.addEventListener('submit', handleAddTask);
    editForm.addEventListener('submit', handleUpdateTask);
    closeModal.addEventListener('click', closeEditModal);
    cancelBtn.addEventListener('click', closeEditModal);
    statusFilter.addEventListener('change', applyFilters);
    priorityFilter.addEventListener('change', applyFilters);

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === editModal) {
            closeEditModal();
        }
    });
}

/**
 * Add a new task
 */
async function handleAddTask(e) {
    e.preventDefault();

    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const priority = document.getElementById('taskPriority').value;
    const dueDate = document.getElementById('taskDueDate').value;

    if (!title) {
        showNotification('Title is required', 'error');
        return;
    }

    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                description,
                priority,
                due_date: dueDate
            })
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Task created successfully!', 'success');
            taskForm.reset();
            loadTasks();
            loadAnalytics();
        } else {
            showNotification(data.error || 'Failed to create task', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to create task', 'error');
    }
}

/**
 * Load all tasks
 */
async function loadTasks() {
    try {
        const status = statusFilter.value;
        const priority = priorityFilter.value;
        
        let url = '/api/tasks';
        const params = new URLSearchParams();
        
        if (status) params.append('status', status);
        if (priority) params.append('priority', priority);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await fetch(url);
        const data = await response.json();

        if (data.success) {
            allTasks = data.data;
            renderTasks(allTasks);
        } else {
            showNotification('Failed to load tasks', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to load tasks', 'error');
    }
}

/**
 * Render tasks in table
 */
function renderTasks(tasks) {
    if (!tasks || tasks.length === 0) {
        tasksTableBody.innerHTML = '<tr><td colspan="6" class="text-center">No tasks found</td></tr>';
        return;
    }

    tasksTableBody.innerHTML = tasks.map(task => `
        <tr>
            <td><strong>${escapeHtml(task.title)}</strong></td>
            <td>${task.description ? escapeHtml(task.description.substring(0, 50)) + '...' : '-'}</td>
            <td><span class="priority-${task.priority}">${capitalizeFirst(task.priority)}</span></td>
            <td><span class="status-${task.status}">${capitalizeFirst(task.status.replace('_', ' '))}</span></td>
            <td>${task.due_date ? formatDate(task.due_date) : '-'}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-secondary" onclick="openEditModal(${task.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

/**
 * Open edit modal
 */
async function openEditModal(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const data = await response.json();

        if (data.success) {
            const task = data.data;
            
            document.getElementById('editTaskId').value = task.id;
            document.getElementById('editTaskTitle').value = task.title;
            document.getElementById('editTaskDescription').value = task.description || '';
            document.getElementById('editTaskPriority').value = task.priority;
            document.getElementById('editTaskStatus').value = task.status;
            
            if (task.due_date) {
                document.getElementById('editTaskDueDate').value = task.due_date.split('T')[0];
            }

            editModal.classList.add('show');
        } else {
            showNotification('Failed to load task', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to load task', 'error');
    }
}

/**
 * Close edit modal
 */
function closeEditModal() {
    editModal.classList.remove('show');
    editForm.reset();
}

/**
 * Update a task
 */
async function handleUpdateTask(e) {
    e.preventDefault();

    const taskId = document.getElementById('editTaskId').value;
    const title = document.getElementById('editTaskTitle').value.trim();
    const description = document.getElementById('editTaskDescription').value.trim();
    const priority = document.getElementById('editTaskPriority').value;
    const status = document.getElementById('editTaskStatus').value;
    const dueDate = document.getElementById('editTaskDueDate').value;

    if (!title) {
        showNotification('Title is required', 'error');
        return;
    }

    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                description,
                priority,
                status,
                due_date: dueDate
            })
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Task updated successfully!', 'success');
            closeEditModal();
            loadTasks();
            loadAnalytics();
        } else {
            showNotification(data.error || 'Failed to update task', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to update task', 'error');
    }
}

/**
 * Delete a task
 */
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Task deleted successfully!', 'success');
            loadTasks();
            loadAnalytics();
        } else {
            showNotification(data.error || 'Failed to delete task', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to delete task', 'error');
    }
}

/**
 * Load and display analytics
 */
async function loadAnalytics() {
    try {
        const response = await fetch('/api/tasks/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.data;
            
            document.getElementById('totalTasks').textContent = stats.total_tasks;
            document.getElementById('completedTasks').textContent = stats.completed_tasks;
            document.getElementById('pendingTasks').textContent = stats.pending_tasks;
            document.getElementById('inProgressTasks').textContent = stats.in_progress_tasks;
            document.getElementById('completionPercentage').textContent = stats.completion_percentage + '%';
            document.getElementById('highPriorityTasks').textContent = stats.high_priority_tasks;
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

/**
 * Apply filters to tasks
 */
function applyFilters() {
    currentFilters.status = statusFilter.value;
    currentFilters.priority = priorityFilter.value;
    loadTasks();
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-title">${capitalizeFirst(type)}</div>
        <div class="notification-message">${escapeHtml(message)}</div>
    `;

    notificationArea.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s reverse';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * WebSocket Event Handlers
 */

if (socket) {
    socket.on('connect', () => {
        console.log('Connected to server');
        showNotification('Connected to server', 'success');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        showNotification('Disconnected from server', 'error');
    });

    socket.on('task_created', (task) => {
        console.log('Task created:', task);
        showNotification(`Task "${task.title}" created!`, 'info');
        loadTasks();
        loadAnalytics();
    });

    socket.on('task_updated', (task) => {
        console.log('Task updated:', task);
        showNotification(`Task "${task.title}" updated!`, 'info');
        loadTasks();
        loadAnalytics();
    });

    socket.on('task_deleted', (data) => {
        console.log('Task deleted:', data);
        showNotification('Task deleted!', 'info');
        loadTasks();
        loadAnalytics();
    });
} else {
    console.warn('Socket event handlers were not attached because Socket.IO failed to initialize.');
}

/**
 * Utility Functions
 */

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Initialize when document is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    loadTasks();
    loadAnalytics();
});
