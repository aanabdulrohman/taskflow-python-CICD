const API_URL = '/api/v1/tasks';

// Fetch semua task saat halaman dimuat
document.addEventListener('DOMContentLoaded', fetchTasks);

async function fetchTasks() {
    try {
        const response = await fetch(API_URL);
        const tasks = await response.json();

        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';

        tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${task.title}</strong> - ${task.description || 'Tidak ada deskripsi'}`;
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

async function createTask() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    if (!title) {
        alert('Judul tidak boleh kosong!');
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, is_completed: false })
        });

        if (response.ok) {
            document.getElementById('title').value = '';
            document.getElementById('description').value = '';
            fetchTasks(); // Refresh list
        }
    } catch (error) {
        console.error('Error creating task:', error);
    }
}