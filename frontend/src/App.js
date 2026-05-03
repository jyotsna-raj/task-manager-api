import React, { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const getTasks = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API}/tasks`);
      const data = await res.json();
      setTasks(data);
    } catch (err) {
      setMessage("Error fetching tasks");
    } finally {
      setLoading(false);
    }
  };

  const createTask = async () => {
    if (!title || !description) {
      setMessage("Please fill all fields");
      return;
    }

    try {
      setLoading(true);
      await fetch(`${API}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description }),
      });

      setMessage("Task created successfully");
      setTitle("");
      setDescription("");
      getTasks();
    } catch {
      setMessage("Error creating task");
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (id) => {
    try {
      await fetch(`${API}/tasks/${id}`, {
        method: "DELETE",
      });
      setMessage("Task deleted");
      getTasks();
    } catch {
      setMessage("Error deleting task");
    }
  };

  useEffect(() => {
    getTasks();
  }, []);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1> Task Manager Dashboard</h1>

      {message && <p style={{ color: "green" }}>{message}</p>}

      <div style={{ marginBottom: "20px" }}>
        <h3>Create Task</h3>

        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ padding: "8px", width: "250px" }}
        />
        <br /><br />

        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ padding: "8px", width: "250px" }}
        />
        <br /><br />

        <button onClick={createTask} disabled={loading}>
          {loading ? "Creating..." : "Create Task"}
        </button>
      </div>

      <div>
        <h3>Tasks</h3>

        <button onClick={getTasks}>Refresh</button>

        {loading && <p>Loading...</p>}

        <ul>
          {tasks.map((task) => (
            <li key={task.id} style={{ marginBottom: "10px" }}>
              <strong>{task.title}</strong> - {task.description}
              <button
                style={{ marginLeft: "10px" }}
                onClick={() => deleteTask(task.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;