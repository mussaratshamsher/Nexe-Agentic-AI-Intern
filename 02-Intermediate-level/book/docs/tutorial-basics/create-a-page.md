---
sidebar_position: 1
---

# Creating Interactive Pages for Robotics Applications

Creating custom pages allows you to build interactive dashboards, visualization tools, and monitoring interfaces for robotics projects. These standalone pages can integrate real-time data, simulation results, and control interfaces.

## Creating a Robot Status Dashboard

Add **React or Markdown** files to `src/pages` to create specialized interfaces:

- `src/pages/index.js` → `localhost:3000/` (Main landing page)
- `src/pages/control-panel.js` → `localhost:3000/control-panel` (Robot control interface)
- `src/pages/simulation.js` → `localhost:3000/simulation` (Simulator visualization)
- `src/pages/telemetry.js` → `localhost:3000/telemetry` (Real-time data dashboard)

## Create a Robot Telemetry Dashboard

Create a file at `src/pages/robot-telemetry.js` to visualize real-time robot data:

```jsx title="src/pages/robot-telemetry.js"
import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';

// Mock data fetching function - in practice, connect to ROS2 topics or REST API
const fetchTelemetryData = async () => {
  const mockData = {
    battery_level: 87,
    joint_positions: { hip: 0.2, knee: 1.1, ankle: -0.3 },
    imu_data: { roll: 0.01, pitch: 0.03, yaw: 1.57 },
    gps_location: { lat: 37.7749, lon: -122.4194 },
    cpu_temp: 65,
    status: 'ACTIVE'
  };
  return mockData;
};

export default function RobotTelemetryDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const telemetryData = await fetchTelemetryData();
      setData(telemetryData);
      setLoading(false);
    };

    loadData();
    // Refresh every 2 seconds
    const interval = setInterval(loadData, 2000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Layout title="Robot Telemetry">
        <div className="container margin-vert--xl">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <h1>Loading Telemetry Data...</h1>
              <div className="progress">
                <div className="progress__bar progress__bar--animated"></div>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Robot Telemetry Dashboard">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col">
            <h1>Robot Telemetry Dashboard</h1>
            <p>Last Updated: {new Date().toLocaleTimeString()}</p>
          </div>
        </div>

        <div className="row margin-vert--lg">
          {/* Status Panel */}
          <div className="col col--3">
            <div className={`card ${data.status === 'ACTIVE' ? 'card--success' : 'card--danger'}`}>
              <div className="card__header">
                <h3>System Status</h3>
              </div>
              <div className="card__body">
                <p>Status: <strong>{data.status}</strong></p>
                <p>Battery: <strong>{data.battery_level}%</strong></p>
                <p>CPU Temp: <strong>{data.cpu_temp}°C</strong></p>
              </div>
            </div>
          </div>

          {/* Joint Positions */}
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>Joint Positions (rad)</h3>
              </div>
              <div className="card__body">
                {Object.entries(data.joint_positions).map(([joint, pos]) => (
                  <p key={joint}>{joint}: <strong>{pos.toFixed(3)}</strong></p>
                ))}
              </div>
            </div>
          </div>

          {/* IMU Data */}
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>IMU Data (rad)</h3>
              </div>
              <div className="card__body">
                <p>Roll: <strong>{data.imu_data.roll.toFixed(3)}</strong></p>
                <p>Pitch: <strong>{data.imu_data.pitch.toFixed(3)}</strong></p>
                <p>Yaw: <strong>{data.imu_data.yaw.toFixed(3)}</strong></p>
              </div>
            </div>
          </div>

          {/* GPS Location */}
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>Location</h3>
              </div>
              <div className="card__body">
                <p>Lat: <strong>{data.gps_location.lat.toFixed(4)}</strong></p>
                <p>Lon: <strong>{data.gps_location.lon.toFixed(4)}</strong></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
```

A new page is now available at [http://localhost:3000/robot-telemetry](http://localhost:3000/robot-telemetry) showing live robot data.

## Create a Simulation Visualization Page

Create a file at `src/pages/simulation-viewer.md` to show simulation scenarios:

```mdx title="src/pages/simulation-viewer.md"
---
title: Simulation Environment Viewer
description: Visualize robot simulation in realistic environments
---

# Robot Simulation Environment

This page provides an interactive viewer for our robot simulation in various environments.

## Available Scenarios

1. **Warehouse Navigation**: Robot navigating through warehouse aisles to pick up packages
2. **Urban Search**: Robot performing search and rescue in urban environments
3. **Industrial Inspection**: Robot inspecting industrial equipment and structures
4. **Human-Robot Collaboration**: Robot assisting humans in manufacturing tasks

## Features

- Real-time physics simulation
- Dynamic environment objects
- Sensor simulation (LiDAR, cameras, IMU)
- Collision detection and avoidance
- Performance metrics tracking

<iframe width="100%" height="600px" src="https://www.youtube.com/embed/NrLREea2ago?autoplay=0&controls=1" frameborder="0" allowfullscreen></iframe>

*Example simulation footage showing robot navigating an obstacle course*
```

A new page is now available at [http://localhost:3000/simulation-viewer](http://localhost:3000/simulation-viewer) showing simulation content.

## Advanced Page Features for Robotics Applications

### Interactive Controls

For robot control interfaces, create React components that can send commands to your robot:

```jsx
// Example of a simple joint control interface
import React, { useState } from 'react';

function JointControl({ jointName, min, max }) {
  const [position, setPosition] = useState(0);

  const handleMove = () => {
    // In practice, this would send the command to the robot
    console.log(`Moving ${jointName} to position: ${position}`);
  };

  return (
    <div>
      <h4>{jointName}</h4>
      <input
        type="range"
        min={min}
        max={max}
        step="0.01"
        value={position}
        onChange={(e) => setPosition(parseFloat(e.target.value))}
      />
      <span>{position.toFixed(2)}</span>
      <button onClick={handleMove}>Move Joint</button>
    </div>
  );
}
```

### Data Visualization

Use charts and graphs to display sensor data, performance metrics, or training progress:

```jsx
// Example of performance metrics chart
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function PerformanceChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="accuracy" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="loss" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

Custom pages enable you to create rich, interactive interfaces for controlling, monitoring, and visualizing your robotics applications beyond traditional documentation.
