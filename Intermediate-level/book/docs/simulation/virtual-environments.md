---
sidebar_position: 1
---

# Virtual Environments and Simulation for Humanoid Robotics

Simulation environments are critical for developing, testing, and validating humanoid robots before deployment in the real world. These virtual environments allow for safe, repeatable, and cost-effective experimentation with complex robotic systems without the risk of hardware damage or safety concerns.

## Why Simulation is Critical for Humanoid Robotics

Humanoid robots present unique challenges that make simulation indispensable:

- **High hardware costs**: Damage to expensive actuators and sensors can be costly
- **Safety concerns**: Testing in simulation prevents potential injury to humans
- **Complex dynamics**: Humanoid locomotion involves complex multi-body dynamics
- **Training data**: Large amounts of training data can be generated more easily in simulation
- **Reproducible experiments**: Virtual environments provide controlled testing conditions

![Simulation Environment](/img/chap10.jpg)

*Figure: Advanced physics simulation environment for humanoid robot testing*

## Major Simulation Platforms

### Gazebo (Classic and Garden)

Gazebo is a powerful open-source simulator with realistic physics:

```xml
<!-- Example URDF model for a humanoid robot in simulation -->
<?xml version="1.0"?>
<robot name="humanoid_sim">
  <!-- Base link -->
  <link name="base_link">
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0.5"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.5"/>
      <geometry>
        <box size="0.5 0.5 1.0"/>
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0.5"/>
      <geometry>
        <box size="0.5 0.5 1.0"/>
      </geometry>
    </collision>
  </link>

  <!-- Hip joint and link -->
  <joint name="left_hip_pitch" type="revolute">
    <parent link="base_link"/>
    <child link="left_thigh"/>
    <origin xyz="-0.1 0.2 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="3.0"/>
  </joint>

  <link name="left_thigh">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 -0.25"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>
</robot>
```

Launch file for simulation:

```xml
<!-- launch/humanoid_sim.launch.py -->
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    return LaunchDescription([
        # Launch Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            )
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
            )
        ),

        # Spawn humanoid robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'humanoid'],
            output='screen'
        )
    ])
```

### PyBullet

PyBullet offers fast physics simulation with Python integration:

```python
import pybullet as p
import pybullet_data
import numpy as np

class HumanoidSimulator:
    def __init__(self, urdf_path="humanoid.urdf", gui=True):
        # Connect to physics engine
        if gui:
            self.client = p.connect(p.GUI)
        else:
            self.client = p.connect(p.HEADLESS)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)

        # Load plane and robot
        self.plane_id = p.loadURDF("plane.urdf")
        self.robot_id = p.loadURDF(urdf_path, [0, 0, 1])

        # Get joint information
        self.joint_info = self._get_joint_info()

        # Enable torque control for all joints
        self._enable_torque_control()

    def _get_joint_info(self):
        """Get information about all joints"""
        joint_info = {}
        num_joints = p.getNumJoints(self.robot_id)

        for i in range(num_joints):
            info = p.getJointInfo(self.robot_id, i)
            joint_name = info[1].decode('utf-8')
            joint_info[joint_name] = {
                'index': info[0],
                'type': info[2],
                'lower_limit': info[8],
                'upper_limit': info[9],
                'max_force': info[10],
                'max_velocity': info[11]
            }
        return joint_info

    def _enable_torque_control(self):
        """Enable torque control for all revolute joints"""
        indices = []
        max_forces = []

        for joint_name, info in self.joint_info.items():
            if info['type'] == p.JOINT_REVOLUTE:  # Revolute joint
                indices.append(info['index'])
                max_forces.append(info['max_force'])

        p.setJointMotorControlArray(
            self.robot_id,
            indices,
            p.VELOCITY_CONTROL,
            forces=[0.0] * len(indices)
        )

    def apply_torques(self, joint_torques):
        """Apply torques to the robot joints"""
        # joint_torques should be a dict mapping joint names to torque values
        indices = []
        torques = []

        for joint_name, torque in joint_torques.items():
            if joint_name in self.joint_info:
                indices.append(self.joint_info[joint_name]['index'])
                torques.append(torque)

        p.setJointMotorControlArray(
            self.robot_id,
            indices,
            p.TORQUE_CONTROL,
            forces=torques
        )

    def get_robot_state(self):
        """Get current robot state"""
        joint_states = p.getJointStates(self.robot_id,
                                       [info['index'] for info in self.joint_info.values()])

        state = {}
        for joint_name, joint_state in zip(self.joint_info.keys(), joint_states):
            state[joint_name] = {
                'position': joint_state[0],
                'velocity': joint_state[1],
                'reaction_force': joint_state[2],
                'applied_torque': joint_state[3]
            }

        # Get base position and orientation
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        state['base'] = {
            'position': pos,
            'orientation': orn
        }

        return state

    def step_simulation(self):
        """Step the simulation forward"""
        p.stepSimulation()

    def close(self):
        """Close the simulation"""
        p.disconnect(self.client)

# Example usage
if __name__ == "__main__":
    sim = HumanoidSimulator(gui=True)

    # Simple PD controller example
    kp = 100  # Proportional gain
    kd = 10   # Derivative gain

    target_positions = {joint: 0.0 for joint in sim.joint_info.keys()}

    for _ in range(1000):  # Run for 1000 steps
        current_state = sim.get_robot_state()

        # Compute torques using PD control
        torques = {}
        for joint_name in target_positions.keys():
            if joint_name in current_state:
                error = target_positions[joint_name] - current_state[joint_name]['position']
                error_dot = -current_state[joint_name]['velocity']

                torques[joint_name] = kp * error + kd * error_dot

        sim.apply_torques(torques)
        sim.step_simulation()

    sim.close()
```

### NVIDIA Isaac Gym

For reinforcement learning applications, Isaac Gym provides GPU-accelerated simulation:

```python
import torch
import numpy as np
from isaacgym import gymapi, gymtorch

class IsaacGymHumanoidEnv:
    def __init__(self, headless=False):
        # Initialize gym
        self.gym = gymapi.acquire_gym()

        # Configure sim
        sim_params = gymapi.SimParams()
        sim_params.up_axis = gymapi.UP_AXIS_Z
        sim_params.gravity = gymapi.Vec3(0, 0, -9.81)

        # Create sim
        self.sim = self.gym.create_sim(0, 0, gymapi.SIM_PHYSX, sim_params)

        # Create viewer
        if not headless:
            self.viewer = self.gym.create_viewer(self.sim, gymapi.CameraProperties())
        else:
            self.viewer = None

        # Load humanoid asset
        asset_root = "assets"
        asset_file = "humanoid.urdf"

        asset_options = gymapi.AssetOptions()
        asset_options.fix_base_link = False
        asset_options.disable_gravity = False

        self.humanoid_asset = self.gym.load_asset(self.sim, asset_root, asset_file, asset_options)

        # Set up environments
        self.envs = []
        num_envs = 4096  # Large number for parallel training
        spacing = 2.5

        env_lower = gymapi.Vec3(-spacing, -spacing, 0.0)
        env_upper = gymapi.Vec3(spacing, spacing, spacing)

        # Create multiple environments
        for i in range(num_envs):
            env = self.gym.create_env(self.sim, env_lower, env_upper, 1)

            # Add humanoid to environment
            pose = gymapi.Transform()
            pose.p = gymapi.Vec3(0.0, 0.0, 1.0)
            pose.r = gymapi.Quat(0, 0, 0, 1)

            self.humanoid_handle = self.gym.create_actor(env, self.humanoid_asset, pose, "humanoid", i, 1, 0)

            # Set DOF properties
            dof_props = self.gym.get_actor_dof_properties(env, self.humanoid_handle)
            dof_props['stiffness'][:] = 400.0
            dof_props['damping'][:] = 80.0
            self.gym.set_actor_dof_properties(env, self.humanoid_handle, dof_props)

            self.envs.append(env)

    def get_observations(self):
        """Get observations from all environments"""
        actor_root_state = self.gym.acquire_actor_root_state_tensor(self.sim)
        dof_state = self.gym.acquire_dof_state_tensor(self.sim)
        force_torque = self.gym.acquire_force_sensor_tensor(self.sim)

        self.gym.refresh_actor_root_state_tensor(self.sim)
        self.gym.refresh_dof_state_tensor(self.sim)
        self.gym.refresh_force_sensor_tensor(self.sim)

        # Convert to PyTorch tensors for RL training
        obs = gymtorch.wrap_tensor(actor_root_state).clone()
        return obs

    def step(self, actions):
        """Step simulation with actions"""
        # Apply actions to humanoid joints
        # Implementation depends on action space definition
        pass
```

## Physics Simulation Considerations

### Contact Modeling

For humanoid robots, accurate contact modeling is crucial:

```python
# Parameters for contact simulation
CONTACT_PARAMETERS = {
    # Contact stiffness and damping
    'contact_stiffness': 10000.0,  # N/m
    'contact_damping': 1000.0,     # Ns/m

    # Friction parameters
    'lateral_friction': 0.8,
    'rolling_friction': 0.01,
    'spinning_friction': 0.01,

    # Contact margin (distance threshold for contact detection)
    'contact_margin': 0.001,  # 1mm
}
```

### Actuator Models

Simulate realistic actuator dynamics:

```python
class SimulatedActuator:
    def __init__(self, gear_ratio=100, max_torque=100.0, motor_constant=0.1):
        self.gear_ratio = gear_ratio
        self.max_torque = max_torque
        self.motor_constant = motor_constant

        # Internal state (simulate motor dynamics)
        self.motor_velocity = 0.0
        self.motor_torque = 0.0

        # Electrical time constant
        self.electrical_tc = 0.01  # 10ms

    def update(self, command_torque, joint_velocity, dt):
        """Update actuator simulation with realistic dynamics"""
        # Apply torque limits
        command_torque = np.clip(command_torque, -self.max_torque, self.max_torque)

        # Simulate motor electrical dynamics
        voltage_command = command_torque / self.motor_constant
        self.motor_torque = voltage_command * self.motor_constant

        # Add damping proportional to velocity
        damping_torque = -0.1 * self.motor_velocity
        self.motor_torque += damping_torque

        # Gear ratio effect
        output_torque = self.motor_torque * self.gear_ratio
        output_velocity = joint_velocity / self.gear_ratio

        # Simulate mechanical time constants
        torque_error = (command_torque * self.gear_ratio) - self.motor_torque
        self.motor_torque += (torque_error / self.electrical_tc) * dt

        # Apply saturation
        self.motor_torque = np.clip(self.motor_torque,
                                   -self.max_torque * self.gear_ratio,
                                    self.max_torque * self.gear_ratio)

        return self.motor_torque / self.gear_ratio
```

## Domain Randomization

To bridge the sim-to-real gap, implement domain randomization:

```python
class DomainRandomizer:
    def __init__(self):
        self.param_ranges = {
            'mass_multiplier': [0.8, 1.2],      # ±20% mass variation
            'friction_multiplier': [0.5, 1.5],  # 0.5x to 1.5x friction
            'restitution': [0.0, 0.2],          # Bounciness
            'latency': [0.005, 0.020],          # 5-20ms sensor latency
            'noise_std': [0.001, 0.01],         # Sensor noise
        }

    def randomize_environment(self, env):
        """Randomize physics properties for domain randomization"""
        random_params = {}

        for param, (min_val, max_val) in self.param_ranges.items():
            random_params[param] = np.random.uniform(min_val, max_val)

        # Apply randomization to environment
        self._apply_mass_randomization(env, random_params['mass_multiplier'])
        self._apply_friction_randomization(env, random_params['friction_multiplier'])
        self._apply_restitution_randomization(env, random_params['restitution'])

        return random_params

    def _apply_mass_randomization(self, env, multiplier):
        """Apply mass randomization to all bodies"""
        # Implementation depends on simulation engine
        pass

    def _apply_friction_randomization(self, env, multiplier):
        """Apply friction randomization"""
        # Implementation depends on simulation engine
        pass
```

## Sensor Simulation

Accurately simulate robot sensors:

```python
class SimulatedSensors:
    def __init__(self, robot_id, physics_client):
        self.robot_id = robot_id
        self.physics_client = physics_client

        # IMU simulation
        self.imu_bias = np.random.normal(0, 0.01, 6)  # Bias in gyro and accelerometer
        self.imu_noise_std = [0.01, 0.01, 0.01, 0.001, 0.001, 0.001]  # Noise std

    def get_imu_data(self):
        """Simulate IMU data with noise and bias"""
        # Get true state from simulation
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        lin_vel, ang_vel = p.getBaseVelocity(self.robot_id)

        # Convert to IMU readings (simplified)
        # In reality, this would depend on IMU position on the robot
        true_angular_velocity = np.array(ang_vel)
        true_linear_acceleration = np.array([0, 0, 9.81])  # Gravity + acceleration

        # Add bias and noise
        noisy_angular_vel = true_angular_velocity + self.imu_bias[:3]
        noisy_linear_acc = true_linear_acceleration + self.imu_bias[3:]

        noisy_angular_vel += np.random.normal(0, self.imu_noise_std[:3])
        noisy_linear_acc += np.random.normal(0, self.imu_noise_std[3:])

        return {
            'angular_velocity': noisy_angular_vel.tolist(),
            'linear_acceleration': noisy_linear_acc.tolist(),
            'orientation': orn
        }

    def get_camera_data(self, camera_id):
        """Simulate camera data"""
        # Get camera image from simulation
        width, height, rgb_img, depth_img, seg_img = p.getCameraImage(
            width=640,
            height=480,
            viewMatrix=p.computeViewMatrix([1, -1, 2], [0, 0, 0], [0, 0, 1]),
            projectionMatrix=p.computeProjectionMatrixFOV(45, 640/480, 0.1, 100)
        )

        return {
            'rgb': rgb_img,
            'depth': depth_img,
            'width': width,
            'height': height
        }
```

## Control Integration with Simulation

Implement control loops that work in both simulation and real hardware:

```python
class ControllerWithSimulation:
    def __init__(self, sim_mode=True):
        self.sim_mode = sim_mode
        self.control_frequency = 500  # Hz
        self.time_step = 1.0 / self.control_frequency

        # Initialize controllers
        self.joint_controllers = self._init_joint_controllers()
        self.whole_body_controller = WholeBodyController()

    def _init_joint_controllers(self):
        """Initialize individual joint controllers"""
        controllers = {}
        joint_names = [
            "left_hip_roll", "left_hip_yaw", "left_hip_pitch",
            "left_knee", "left_ankle_pitch", "left_ankle_roll",
            "right_hip_roll", "right_hip_yaw", "right_hip_pitch",
            "right_knee", "right_ankle_pitch", "right_ankle_roll"
            # Add more joints as needed
        ]

        for joint_name in joint_names:
            controllers[joint_name] = PDController(kp=100, kd=10)

        return controllers

    def control_step(self, current_state, desired_state):
        """Main control loop step"""
        if self.sim_mode:
            # In simulation, we can access true state directly
            control_commands = self._compute_control_commands(current_state, desired_state)

            # Apply commands to simulation
            self._apply_commands_to_simulation(control_commands)
        else:
            # On real robot, use hardware interface
            control_commands = self._compute_control_commands(current_state, desired_state)
            self._apply_commands_to_hardware(control_commands)

        return control_commands

    def _compute_control_commands(self, current_state, desired_state):
        """Compute control commands based on current and desired state"""
        commands = {}

        for joint_name in current_state.keys():
            if joint_name in self.joint_controllers:
                current_pos = current_state[joint_name]['position']
                current_vel = current_state[joint_name]['velocity']

                desired_pos = desired_state[joint_name]['position']
                desired_vel = desired_state[joint_name]['velocity']

                # Compute control command
                command = self.joint_controllers[joint_name].compute(
                    desired_pos, current_pos, desired_vel, current_vel
                )

                commands[joint_name] = command

        return commands
```

## Simulation-to-Real Transfer Strategies

### System Identification

Characterize real robot parameters to match simulation:

```python
def identify_robot_parameters(robot_id, sim_client, real_robot):
    """Identify real robot parameters to tune simulation"""
    # Collect data from real robot
    real_data = collect_excitation_data(real_robot)

    # Simulate with different parameters
    sim_data = run_parameter_sweep(sim_client, robot_id, real_data['inputs'])

    # Find parameters that minimize sim-to-real error
    optimal_params = minimize_model_error(real_data, sim_data)

    # Update simulation with identified parameters
    update_simulation_parameters(sim_client, robot_id, optimal_params)

    return optimal_params
```

### Iterative Learning

Use simulation to pre-train, then adapt on real hardware:

```python
def sim_to_real_learning(
    policy_network,
    sim_env,
    real_env,
    pre_train_steps=1000000,
    adaptation_steps=100000
):
    """Sim-to-real learning approach"""

    # Phase 1: Pre-train in simulation
    print("Pre-training in simulation...")
    for step in range(pre_train_steps):
        sim_obs = sim_env.get_observation()
        sim_action = policy_network.get_action(sim_obs)
        sim_reward = sim_env.step(sim_action)

        # Update policy
        policy_network.update(sim_obs, sim_action, sim_reward)

    # Phase 2: Adapt on real robot with domain adaptation
    print("Adapting on real robot...")
    for step in range(adaptation_steps):
        real_obs = real_env.get_observation()
        real_action = policy_network.get_action(real_obs)
        real_reward = real_env.step(real_action)

        # Update policy with real data
        policy_network.update(real_obs, real_action, real_reward)

        # Occasionally re-train with combination of sim and real data
        if step % 1000 == 0:
            # Retrain with mixed dataset
            policy_network.retrain_with_mixed_data()

    return policy_network
```

## Best Practices for Simulation

1. **Validate simulation accuracy**: Compare simulation behavior with real robot data
2. **Use appropriate time stepping**: Balance accuracy and performance
3. **Implement sensor noise models**: Make simulation more realistic
4. **Randomize physics parameters**: Improve robustness through domain randomization
5. **Test failure scenarios**: Use simulation to test safe failure recovery
6. **Implement realistic actuator models**: Account for motor dynamics and limitations

Simulation environments are an essential tool in the humanoid robotics development pipeline, enabling rapid prototyping, safe testing, and efficient algorithm development before deployment on expensive hardware.