import React, { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [tasks, setTasks] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [socketConnected, setSocketConnected] = useState(false);

  const getTasks = async () => {
    try {
      setLoading(true);

      const res = await fetch(`${API}/tasks`);
      const data = await res.json();

      setTasks(data);
    } catch {
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
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title,
          description
        })
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
        method: "DELETE"
      });

      setMessage("Task deleted");

      getTasks();

    } catch {
      setMessage("Error deleting task");
    }
  };

  useEffect(() => {
    getTasks();

    const socket = new WebSocket("ws://127.0.0.1:8001/ws");

    socket.onopen = () => {
      console.log("WebSocket connected");
      setSocketConnected(true);
    };

    socket.onmessage = (event) => {
      const notification = JSON.parse(event.data);

      setNotifications((prev) => [
        notification,
        ...prev
      ]);
    };

    socket.onerror = () => {
      setSocketConnected(false);
    };

    socket.onclose = () => {
      setSocketConnected(false);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial",
        backgroundColor: "#f4f6f9",
        minHeight: "100vh"
      }}
    >
      <h1>Task Manager Dashboard</h1>

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginBottom: "20px"
        }}
      >
        <div
          style={{
            background: "white",
            padding: "15px",
            borderRadius: "10px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
          }}
        >
          <strong>Total Tasks:</strong> {tasks.length}
        </div>

        <div
          style={{
            background: "white",
            padding: "15px",
            borderRadius: "10px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
          }}
        >
          <strong>Notifications:</strong> {notifications.length}
        </div>

        <div
          style={{
            background: socketConnected ? "#d4edda" : "#f8d7da",
            padding: "15px",
            borderRadius: "10px",
            fontWeight: "bold"
          }}
        >
          {socketConnected
            ? "WebSocket Connected"
            : "WebSocket Disconnected"}
        </div>
      </div>

      {message && (
        <div
          style={{
            background: "#d1ecf1",
            padding: "10px",
            borderRadius: "8px",
            marginBottom: "20px"
          }}
        >
          {message}
        </div>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginBottom: "30px"
        }}
      >
        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
          }}
        >
          <h2>Create Task</h2>

          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px"
            }}
          />

          <input
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px"
            }}
          />

          <button
            onClick={createTask}
            disabled={loading}
            style={{
              padding: "10px 20px",
              cursor: "pointer"
            }}
          >
            {loading ? "Creating..." : "Create Task"}
          </button>
        </div>

        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
            maxHeight: "350px",
            overflowY: "auto"
          }}
        >
          <h2>Live Notifications</h2>

          {notifications.length === 0 ? (
            <p>No notifications yet</p>
          ) : (
            notifications.map((notification, index) => (
              <div
                key={index}
                style={{
                  border: "1px solid #ddd",
                  padding: "10px",
                  marginBottom: "10px",
                  borderRadius: "8px",
                  background: "#fafafa"
                }}
              >
                <strong>{notification.event}</strong>
                <br />
                Title: {notification.title}
                <br />
                Description: {notification.description}
              </div>
            ))
          )}
        </div>
      </div>

      <div
        style={{
          background: "white",
          padding: "20px",
          borderRadius: "10px",
          boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
        }}
      >
        <h2>Tasks</h2>

        <button
          onClick={getTasks}
          style={{
            marginBottom: "20px"
          }}
        >
          Refresh Tasks
        </button>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))",
            gap: "15px"
          }}
        >
          {tasks.map((task) => (
            <div
              key={task.id}
              style={{
                border: "1px solid #ddd",
                borderRadius: "10px",
                padding: "15px",
                background: "#fafafa"
              }}
            >
              <h3>{task.title}</h3>

              <p>{task.description}</p>

              <button
                onClick={() => deleteTask(task.id)}
                style={{
                  cursor: "pointer"
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;