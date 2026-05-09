---
sidebar_position: 1
---

# Building a Complete Humanoid Robot System

Creating a complete humanoid robot system integrates all the components covered in this book: physical design, perception, cognition, action, and control. This capstone project demonstrates how to combine these elements into a functional, intelligent humanoid robot capable of interacting with its environment.

## Project Overview: APEX (Autonomous Physical Intelligence eXperiment)

Our capstone project involves building APEX, a 1.2-meter tall humanoid robot designed to perform household tasks and interact with humans. The system integrates:

- **Perception**: Vision, audition, and tactile sensing
- **Cognition**: VLA models and cognitive architectures
- **Action**: Full-body motion and manipulation capabilities
- **Control**: Real-time balance and coordination
- **Learning**: Continuous skill acquisition from experience

![Humanoid Robot Build](/img/chap15.jpg)

*Figure: Complete humanoid robot system integrating all components of Physical AI*

## System Architecture

### Hardware Design

The robot consists of 32 degrees of freedom (DoF) distributed across the body:

```yaml
# Robot specification
total_dof: 32
body_parts:
  head:
    joints: 3
    joints_list:
      - neck_yaw
      - neck_pitch
      - neck_roll
  torso:
    joints: 2
    joints_list:
      - torso_yaw
      - torso_pitch
  left_arm:
    joints: 7
    joints_list:
      - left_shoulder_pitch
      - left_shoulder_roll
      - left_shoulder_yaw
      - left_elbow
      - left_wrist_pitch
      - left_wrist_yaw
      - left_wrist_roll
  right_arm:
    joints: 7
    joints_list:
      - right_shoulder_pitch
      - right_shoulder_roll
      - right_shoulder_yaw
      - right_elbow
      - right_wrist_pitch
      - right_wrist_yaw
      - right_wrist_roll
  left_leg:
    joints: 6
    joints_list:
      - left_hip_roll
      - left_hip_yaw
      - left_hip_pitch
      - left_knee
      - left_ankle_pitch
      - left_ankle_roll
  right_leg:
    joints: 6
    joints_list:
      - right_hip_roll
      - right_hip_yaw
      - right_hip_pitch
      - right_knee
      - right_ankle_pitch
      - right_ankle_roll
  sensors:
    - stereo_camera
    - depth_camera
    - IMU
    - force_torque_sensors
    - microphones
```

### Control Hierarchy

The control system operates at multiple levels:

```python
class RobotControlSystem:
    def __init__(self):
        # High-level cognitive planning
        self.cognitive_arch = CognitiveArchitecture()

        # Mid-level motion planning
        self.motion_planner = MotionPlanner()

        # Low-level control
        self.balance_controller = BalanceController()
        self.impedance_controllers = self._init_impedance_controllers()

        # VLA integration
        self.vla_model = VLAIntegrationModel()

        # Real-time scheduler
        self.scheduler = RealTimeScheduler(
            control_freq=500,    # 500Hz for balance
            planning_freq=20,    # 20Hz for planning
            perception_freq=30   # 30Hz for perception
        )

    def execute_command(self, language_command, visual_input):
        """Execute a natural language command on the physical robot"""
        # 1. Parse command using cognitive architecture
        high_level_plan = self.cognitive_arch.parse_command(language_command)

        # 2. Process visual input through VLA system
        perception_outputs = self.vla_model.process_visual_input(visual_input)

        # 3. Generate detailed motion plan
        motion_plan = self.motion_planner.create_plan(
            high_level_plan, perception_outputs
        )

        # 4. Execute with real-time control
        execution_result = self._execute_with_realtime_control(motion_plan)

        return execution_result

    def _execute_with_realtime_control(self, motion_plan):
        """Execute motion plan with real-time balance and safety"""
        for motion_primitive in motion_plan:
            # Execute primitive while monitoring balance
            start_time = time.time()

            while not motion_primitive.is_complete():
                # Get current state
                current_state = self._get_robot_state()

                # Check balance safety
                if not self.balance_controller.is_stable(current_state):
                    return self._emergency_balance_recovery()

                # Apply motion primitive with impedance control
                control_commands = self._generate_control_commands(
                    motion_primitive, current_state
                )

                # Apply to robot
                self._apply_commands(control_commands)

                # Wait for next control cycle
                self.scheduler.wait_next_cycle()

                # Check execution timeout
                if time.time() - start_time > motion_primitive.timeout:
                    return "execution_timeout"

        return "success"
```

## Construction Process

### 1. Frame and Structure

Start with the mechanical frame. For APEX, we use:

- **Materials**: Aluminum 6061-T6 for structural components
- **Actuators**: Series elastic actuators for safe interaction
- **Design philosophy**: Human-like proportions with optimized weight distribution

```python
class FrameDesign:
    def __init__(self):
        self.material_properties = {
            'density': 2700,  # kg/m³ for aluminum
            'strength': 310,  # MPa yield strength
            'cost': 'medium'  # Relative cost factor
        }

        self.joint_design = {
            'range_of_motion': self._calculate_rom_requirements(),
            'torque_requirements': self._calculate_torque_map(),
            'compliance_needs': self._analyze_compliance_map()
        }

    def _calculate_torque_map(self):
        """Calculate required torque for each joint"""
        # Torque = Force × Distance (for static load)
        # Torque = Inertia × Angular_acceleration (for dynamic load)

        torque_map = {}

        # Hip joints (high torque for lifting body weight)
        for hip_joint in ['left_hip_pitch', 'right_hip_pitch']:
            torque_map[hip_joint] = {
                'static': 150,    # N⋅m for static holding
                'dynamic': 200,   # N⋅m for dynamic movement
                'safety_factor': 2.0
            }

        # Ankle joints (high torque for balance)
        for ankle_joint in ['left_ankle_pitch', 'right_ankle_pitch']:
            torque_map[ankle_joint] = {
                'static': 80,
                'dynamic': 120,
                'safety_factor': 2.5  # Higher for balance
            }

        # Shoulder joints (moderate torque for manipulation)
        for shoulder_joint in ['left_shoulder_pitch', 'right_shoulder_pitch']:
            torque_map[shoulder_joint] = {
                'static': 60,
                'dynamic': 80,
                'safety_factor': 1.8
            }

        # Wrist joints (low torque for fine manipulation)
        for wrist_joint in ['left_wrist_pitch', 'right_wrist_pitch']:
            torque_map[wrist_joint] = {
                'static': 20,
                'dynamic': 30,
                'safety_factor': 2.0
            }

        return torque_map
```

### 2. Electronics Integration

Critical electronics for the humanoid robot:

```python
class ElectronicsIntegration:
    def __init__(self):
        self.main_computer = SingleBoardComputer(
            cpu='ARM64',
            ram=32,  # GB
            gpu='Jetson AGX Orin'  # For AI inference
        )

        self.actuator_controllers = self._init_actuator_controllers()
        self.sensor_hub = SensorHub()

        self.power_system = PowerSystem(
            battery_type='Li-ion',
            capacity=24,  # Ah
            voltage=24    # V
        )

        self.safety_system = SafetySystem()

    def _init_actuator_controllers(self):
        """Initialize distributed actuator control system"""
        controllers = {}

        # Each joint has its own controller for low-latency response
        joint_list = self._get_all_joints()

        for joint in joint_list:
            controllers[joint] = ActuatorController(
                joint_name=joint,
                control_freq=1000,  # 1kHz for each joint
                position_resolution=0.001,  # 1 mrad
                current_resolution=0.01,    # 10 mA
            )

        return controllers

    def _get_all_joints(self):
        """Get complete list of robot joints"""
        return [
            # Head joints
            'neck_yaw', 'neck_pitch', 'neck_roll',
            # Torso joints
            'torso_yaw', 'torso_pitch',
            # Left arm joints
            'left_shoulder_pitch', 'left_shoulder_roll', 'left_shoulder_yaw',
            'left_elbow', 'left_wrist_pitch', 'left_wrist_yaw', 'left_wrist_roll',
            # Right arm joints
            'right_shoulder_pitch', 'right_shoulder_roll', 'right_shoulder_yaw',
            'right_elbow', 'right_wrist_pitch', 'right_wrist_yaw', 'right_wrist_roll',
            # Left leg joints
            'left_hip_roll', 'left_hip_yaw', 'left_hip_pitch',
            'left_knee', 'left_ankle_pitch', 'left_ankle_roll',
            # Right leg joints
            'right_hip_roll', 'right_hip_yaw', 'right_hip_pitch',
            'right_knee', 'right_ankle_pitch', 'right_ankle_roll',
        ]

    def setup_communication(self):
        """Set up communication protocols"""
        # Real-time Ethernet for joint control
        self.ethercat_network = EtherCATNetwork(
            cycle_time=0.001  # 1ms cycle for real-time control
        )

        # ROS2 for high-level communication
        self.ros2_network = ROS2Network(
            domain_id=42
        )

        # Safety bus for emergency stops
        self.safety_network = SafetyNetwork(
            response_time=0.0001  # 100 μs maximum
        )
```

### 3. Sensor Integration

Comprehensive sensor integration for complete environmental awareness:

```python
class SensorIntegration:
    def __init__(self):
        # Visual perception
        self.stereo_camera = StereoCamera(
            resolution=(1280, 720),
            fps=60,
            baseline=120  # mm between cameras
        )

        self.depth_camera = DepthCamera(
            resolution=(640, 480),
            type='stereo'  # or 'structured_light' or 'ToF'
        )

        # Auditory perception
        self.microphone_array = MicrophoneArray(
            num_mics=8,
            sample_rate=48000,
            array_type='circular',
            diameter=100  # mm
        )

        # Tactile sensing
        self.tactile_sensors = TactileSensorArray(
            locations=['fingertips', 'palms', 'feet']
        )

        # Inertial measurement
        self.imu = IMU(
            gyro_resolution=0.01,  # deg/s
            accel_resolution=0.001,  # g
            update_rate=1000  # Hz
        )

        # Force/torque sensing
        self.force_sensors = ForceTorqueSensors(
            locations=['ankles', 'wrists'],
            max_force=500,  # N
            resolution=0.1  # N
        )

        # Joint position sensors
        self.encoders = self._init_joint_encoders()

    def _init_joint_encoders(self):
        """Initialize high-resolution encoders for all joints"""
        encoders = {}

        for joint in self._get_all_joints():
            encoders[joint] = HighResolutionEncoder(
                resolution=16,  # bits
                type='absolute',  # absolute or incremental
                accuracy=0.001  # rad (about 0.06 deg)
            )

        return encoders

    def sensor_fusion_pipeline(self):
        """Create unified perception pipeline"""
        # Multi-sensor data acquisition
        raw_data = {
            'visual': self.stereo_camera.get_frame(),
            'depth': self.depth_camera.get_depth(),
            'audio': self.microphone_array.get_audio(),
            'inertial': self.imu.get_measurements(),
            'force': self.get_force_measurements(),
            'joint_states': self.get_joint_states()
        }

        # Data preprocessing and calibration
        calibrated_data = self._calibrate_sensors(raw_data)

        # Multi-modal feature extraction
        features = self._extract_features(calibrated_data)

        # Unified state estimation
        unified_state = self._estimate_unified_state(features)

        return unified_state

    def _estimate_unified_state(self, features):
        """Estimate unified robot and environment state"""
        state = {
            'robot_pose': self._estimate_robot_pose(features),
            'self_model': self._update_self_model(features),
            'environment': self._map_environment(features),
            'objects': self._detect_objects(features),
            'humans': self._detect_humans(features)
        }

        return state
```

## Software Integration

### 1. Control Software Stack

The complete control software stack:

```python
class ControlSoftwareStack:
    def __init__(self):
        # Real-time control layer
        self.realtime_controller = RealTimeController(
            priority=99,  # Highest priority
            cycle_time=0.002  # 2ms control cycle
        )

        # Perception layer
        self.perception_system = PerceptionSystem(
            model_path='models/perception.pt'
        )

        # Planning layer
        self.planning_system = PlanningSystem(
            planning_freq=20  # Hz
        )

        # Behavior layer
        self.behavior_engine = BehaviorEngine()

        # Learning layer
        self.learning_module = LearningModule()

    def main_control_loop(self):
        """Main real-time control loop"""
        while self.running:
            start_time = time.time()

            # 1. Update perception (30Hz)
            if self.scheduler.perception_time():
                self.perception_update()

            # 2. Update planning (20Hz)
            if self.scheduler.planning_time():
                self.planning_update()

            # 3. Generate low-level commands (500Hz)
            control_commands = self.generate_control_commands()

            # 4. Send to hardware
            self.send_to_hardware(control_commands)

            # 5. Wait for next cycle
            self.wait_for_next_cycle(start_time)

    def generate_control_commands(self):
        """Generate control commands for all joints"""
        # Get current state
        robot_state = self.get_robot_state()
        perception_data = self.get_perception_data()
        high_level_goals = self.get_goals()

        # Balance control
        balance_commands = self.balance_controller.compute(
            robot_state, self.desired_com
        )

        # Motion control
        motion_commands = self.motion_controller.compute(
            robot_state, self.desired_motion
        )

        # Combine with safety limits
        final_commands = self._apply_safety_limits(
            balance_commands, motion_commands
        )

        return final_commands

    def _apply_safety_limits(self, balance_cmd, motion_cmd):
        """Apply safety limits to control commands"""
        # Joint limits
        limited_cmd = self._apply_joint_limits(motion_cmd)

        # Torque limits
        limited_cmd = self._apply_torque_limits(limited_cmd)

        # Balance constraints
        final_cmd = self._apply_balance_constraints(
            limited_cmd, balance_cmd
        )

        return final_cmd
```

### 2. AI Integration Layer

Integrating VLA models and cognitive architectures:

```python
class AIIntegrationLayer:
    def __init__(self):
        # VLA model for perception-action mapping
        self.vla_model = self._load_trained_vla_model(
            model_path='models/vla_model.pt'
        )

        # Cognitive architecture for reasoning
        self.cognitive_arch = HybridCognitiveArchitecture()

        # World model for prediction
        self.world_model = WorldModel(
            prediction_horizon=5.0  # seconds
        )

        # Memory systems
        self.memory_system = MemorySystems()

    def process_command(self, natural_language, visual_scene):
        """Process natural language command in visual context"""
        # 1. Parse language command
        semantic_meaning = self.parse_language(natural_language)

        # 2. Analyze visual scene
        scene_understanding = self.analyze_scene(visual_scene)

        # 3. Ground command in scene
        grounded_command = self.ground_command(
            semantic_meaning, scene_understanding
        )

        # 4. Generate task plan
        task_plan = self.cognitive_arch.reason(
            goal=grounded_command,
            current_state=scene_understanding
        )

        # 5. Execute with VLA integration
        execution_result = self._execute_with_vla(
            task_plan, visual_scene
        )

        # 6. Update learning and memory
        self.update_learning(natural_language, execution_result)
        self.memory_system.store_episode(
            command=natural_language,
            visual_scene=visual_scene,
            result=execution_result
        )

        return execution_result

    def _execute_with_vla(self, task_plan, visual_scene):
        """Execute task plan using VLA system"""
        for subtask in task_plan.subtasks:
            # Convert subtask to visual-language-action format
            vla_input = {
                'image': visual_scene,
                'language': subtask.description,
                'context': self.world_model.get_state()
            }

            # Generate low-level actions
            actions = self.vla_model.generate_actions(vla_input)

            # Execute with safety monitoring
            result = self.execute_actions_with_monitoring(actions)

            # Update world model
            self.world_model.update(subtask, result)

            if not result.success:
                return result  # Return on failure

        return ExecutionResult(success=True)
```

## Integration and Testing

### 1. Component Integration

Test each component before system integration:

```python
class IntegrationTesting:
    def __init__(self):
        self.robot = HumanoidRobot()
        self.test_scenarios = self._define_test_scenarios()

    def _define_test_scenarios(self):
        """Define comprehensive test scenarios"""
        return [
            # Basic functionality tests
            {
                'name': 'joint_movement_test',
                'description': 'Test each joint for full range of motion',
                'requirements': ['single_joint_control'],
                'expected_outcome': 'smooth movement within limits'
            },
            {
                'name': 'balance_standing_test',
                'description': 'Test static balance in standing position',
                'requirements': ['balance_control', 'imu_feedback'],
                'expected_outcome': 'stable standing for 1 minute'
            },
            {
                'name': 'object_detection_test',
                'description': 'Test object detection and localization',
                'requirements': ['vision_system', 'perception_model'],
                'expected_outcome': '95% detection accuracy'
            },

            # Integrated behavior tests
            {
                'name': 'grasp_cube_test',
                'description': 'Detect, approach, and grasp a cube',
                'requirements': ['vision', 'motion_planning', 'grasping'],
                'expected_outcome': 'successful grasp in 5 trials'
            },
            {
                'name': 'walk_to_object_test',
                'description': 'Walk to an object and pick it up',
                'requirements': ['locomotion', 'manipulation', 'perception'],
                'expected_outcome': 'complete task successfully'
            },
            {
                'name': 'natural_language_task',
                'description': 'Perform task from natural language command',
                'requirements': ['cognitive_arch', 'vla_model', 'all_systems'],
                'expected_outcome': 'understand and execute command'
            }
        ]

    def execute_integration_tests(self):
        """Execute integration tests in sequence"""
        results = {}

        for scenario in self.test_scenarios:
            print(f"Running test: {scenario['name']}")

            # Setup test conditions
            self.setup_test_conditions(scenario)

            # Execute test
            result = self.run_test_scenario(scenario)

            # Evaluate result
            evaluation = self.evaluate_test_result(scenario, result)

            # Store results
            results[scenario['name']] = {
                'passed': evaluation['passed'],
                'metrics': evaluation['metrics'],
                'issues': evaluation['issues']
            }

            print(f"Result: {'PASS' if evaluation['passed'] else 'FAIL'}")

            # Clean up before next test
            self.cleanup_test_scenario(scenario)

        # Generate integration report
        self.generate_integration_report(results)

        return results

    def setup_test_conditions(self, scenario):
        """Setup conditions for a specific test"""
        # Reset robot to known state
        self.robot.reset_to_home_position()

        # Configure safety parameters
        self.robot.set_safety_limits(scenario.get('safety_config', {}))

        # Initialize required systems
        for req in scenario['requirements']:
            self.initialize_system(req)

        # Wait for systems to be ready
        time.sleep(1.0)
```

### 2. Safety and Validation

Critical safety systems and validation:

```python
class SafetyAndValidation:
    def __init__(self):
        self.safety_monitor = SafetyMonitor()
        self.emergency_stop = EmergencyStopSystem()
        self.validation_framework = ValidationFramework()

    def safety_validation_process(self):
        """Comprehensive safety validation process"""

        # 1. Hardware safety validation
        hardware_safety_checks = [
            self._validate_emergency_stop(),
            self._validate_joint_limits(),
            self._validate_force_limits(),
            self._validate_collision_detection()
        ]

        # 2. Software safety validation
        software_safety_checks = [
            self._validate_control_bounds(),
            self._validate_perception_safety(),
            self._validate_behavior_safety(),
            self._validate_learning_safety()
        ]

        # 3. System-level safety validation
        system_safety_checks = [
            self._validate_human_interaction_safety(),
            self._validate_failure_modes(),
            self._validate_recovery_procedures()
        ]

        # Execute all safety checks
        all_checks = hardware_safety_checks + software_safety_checks + system_safety_checks

        safety_results = {}
        safe = True

        for check_name, check_func in all_checks:
            result = check_func()
            safety_results[check_name] = result
            if not result['passed']:
                safe = False
                print(f"SAFETY ISSUE in {check_name}: {result['details']}")

        return {
            'overall_safe': safe,
            'report': safety_results
        }

    def _validate_emergency_stop(self):
        """Validate emergency stop functionality"""
        # Test that emergency stop stops all motion immediately
        self.robot.move_to_position([1.0] * 32)  # Move to non-zero position
        time.sleep(0.5)

        # Trigger emergency stop
        self.emergency_stop.trigger()

        # Verify all joints stop within safety time
        start_time = time.time()
        while time.time() - start_time < 0.1:  # 100ms safety window
            joint_velocities = self.robot.get_joint_velocities()
            max_vel = max(abs(v) for v in joint_velocities)
            if max_vel < 0.1:  # rad/s threshold
                break
            time.sleep(0.001)

        stopped_in_time = (time.time() - start_time) <= 0.1
        return {
            'passed': stopped_in_time,
            'details': f'Stopped in {(time.time() - start_time)*1000:.1f}ms'
        }

    def _validate_collision_detection(self):
        """Validate collision detection and avoidance"""
        # Set up scenario where collision should be detected
        self.robot.set_collision_objects(['obstacle1', 'obstacle2'])

        # Plan motion through collision area
        collision_plan = self.robot.plan_motion_with_obstacles(
            start_pos=self.robot.get_current_position(),
            goal_pos=[1.0, 1.0, 0.5, 0.0, 0.0, 0.0],  # Position that should collide
            obstacles=['obstacle1']
        )

        # Check that collision was detected
        collision_detected = collision_plan.contains_collision_warning()

        return {
            'passed': collision_detected,
            'details': 'Collision detection working correctly' if collision_detected else 'Collision not detected'
        }
```

## Deployment and Operation

### Deployment Configuration

Setting up the robot for operation:

```python
class DeploymentSystem:
    def __init__(self):
        self.environment_map = None
        self.operational_modes = self._define_operational_modes()
        self.calibration_system = CalibrationSystem()

    def _define_operational_modes(self):
        """Define different operational modes"""
        return {
            'development': {
                'control_frequency': 500,  # Hz
                'safety_limits': 'high',   # Conservative
                'logging': 'full',         # Maximum detail
                'autonomy': 'low'          # Human supervision required
            },
            'evaluation': {
                'control_frequency': 500,
                'safety_limits': 'medium',
                'logging': 'standard',
                'autonomy': 'medium'
            },
            'production': {
                'control_frequency': 500,
                'safety_limits': 'low',    # Performance-focused
                'logging': 'essential',
                'autonomy': 'high'         # Autonomous operation
            },
            'maintenance': {
                'control_frequency': 200,   # Reduced for diagnostics
                'safety_limits': 'very_high', # Maximum safety
                'logging': 'diagnostic',
                'autonomy': 'none'          # Manual control only
            }
        }

    def deploy(self, environment_config, mode='development'):
        """Deploy robot to specific environment"""
        # Load environment map
        self.environment_map = self._load_environment_map(
            environment_config.map_file
        )

        # Configure operational mode
        self._set_operational_mode(mode)

        # Calibrate sensors and actuators
        self.calibration_system.calibrate_all()

        # Initialize cognitive systems
        self._initialize_cognitive_systems(environment_config)

        # Test basic operations
        self._run_deployment_tests()

        # Report deployment status
        return self._generate_deployment_report()

    def _set_operational_mode(self, mode):
        """Configure system for specified operational mode"""
        config = self.operational_modes[mode]

        # Set control parameters
        self.set_control_frequency(config['control_frequency'])

        # Configure safety limits
        self.set_safety_configuration(config['safety_limits'])

        # Configure logging
        self.set_logging_level(config['logging'])

        # Set autonomy level
        self.set_autonomy_level(config['autonomy'])

        print(f"Robot configured for {mode} mode")

    def _initialize_cognitive_systems(self, env_config):
        """Initialize cognitive systems with environmental knowledge"""
        # Load environment-specific knowledge
        self.cognitive_arch.load_environment_knowledge(
            env_config.knowledge_base
        )

        # Initialize world model
        self.world_model.initialize_from_environment(
            env_config.layout,
            env_config.objects
        )

        # Set up spatial reasoning
        self.spatial_reasoning.initialize_environment_map(
            env_config.layout,
            env_config.navigation_goals
        )
```

## Performance Evaluation

### Benchmarking and Metrics

Evaluate the complete robot system:

```python
class PerformanceEvaluation:
    def __init__(self, robot_system):
        self.robot = robot_system
        self.metrics = {}

    def run_comprehensive_evaluation(self):
        """Run comprehensive evaluation of the robot system"""
        evaluation_results = {
            'physical_performance': self._evaluate_physical_performance(),
            'cognitive_performance': self._evaluate_cognitive_performance(),
            'integration_performance': self._evaluate_integration(),
            'safety_performance': self._evaluate_safety(),
            'learning_performance': self._evaluate_learning()
        }

        # Generate overall performance score
        overall_score = self._calculate_overall_score(evaluation_results)
        evaluation_results['overall_score'] = overall_score

        return evaluation_results

    def _evaluate_physical_performance(self):
        """Evaluate physical capabilities"""
        physical_metrics = {
            'balance_stability': self._test_balance_stability(),
            'locomotion_performance': self._test_locomotion(),
            'manipulation_accuracy': self._test_manipulation(),
            'energy_efficiency': self._test_energy_efficiency(),
            'real_time_performance': self._test_latency()
        }

        return physical_metrics

    def _test_balance_stability(self):
        """Test balance stability metrics"""
        # Test standing stability
        start_time = time.time()
        duration = 60  # seconds
        stability_errors = 0

        while time.time() - start_time < duration:
            robot_state = self.robot.get_state()
            if not self.robot.balance_controller.is_stable(robot_state):
                stability_errors += 1

            time.sleep(0.01)  # 100Hz check

        stability_score = 1.0 - (stability_errors / (duration * 100))
        return {
            'stability_score': stability_score,
            'errors_per_minute': stability_errors / (duration / 60)
        }

    def _evaluate_cognitive_performance(self):
        """Evaluate cognitive system performance"""
        cognitive_tests = [
            ('language_understanding', self._test_language_comprehension),
            ('object_recognition', self._test_object_recognition),
            ('task_planning', self._test_task_planning),
            ('learning_from_interaction', self._test_learning_from_interaction)
        ]

        cognitive_results = {}
        for test_name, test_func in cognitive_tests:
            cognitive_results[test_name] = test_func()

        return cognitive_results

    def _calculate_overall_score(self, eval_results):
        """Calculate weighted overall performance score"""
        weights = {
            'physical_performance': 0.3,
            'cognitive_performance': 0.3,
            'integration_performance': 0.2,
            'safety_performance': 0.1,
            'learning_performance': 0.1
        }

        # Simplified averaging - in practice, would be more complex
        score = 0.0
        for category, weight in weights.items():
            if category in eval_results:
                # Assume each category returns a score between 0 and 1
                category_score = self._calculate_category_score(
                    eval_results[category]
                )
                score += weight * category_score

        return score

    def _calculate_category_score(self, category_results):
        """Calculate score for a specific category"""
        if isinstance(category_results, dict) and 'score' in category_results:
            return category_results['score']

        # If no score is provided, calculate from submetrics
        values = []
        for key, value in category_results.items():
            if isinstance(value, dict) and 'score' in value:
                values.append(value['score'])
            elif isinstance(value, (int, float)):
                values.append(value)

        return sum(values) / len(values) if values else 0.0

# Example usage of the complete system
def deploy_humanoid_robot():
    """Example function showing how to deploy the complete humanoid robot"""
    # Initialize the complete system
    robot = RobotControlSystem()
    ai_layer = AIIntegrationLayer()
    deployment = DeploymentSystem()
    evaluation = PerformanceEvaluation(robot)

    print("Starting humanoid robot deployment process...")

    # Deploy the system
    env_config = {
        'map_file': 'home_environment.yaml',
        'knowledge_base': 'home_tasks.kb',
        'layout': 'home_layout.json',
        'objects': 'known_objects.json',
        'navigation_goals': 'navigation_goals.json'
    }

    deployment_result = deployment.deploy(env_config, mode='evaluation')

    # Run initial evaluation
    eval_results = evaluation.run_comprehensive_evaluation()
    print(f"Deployment evaluation score: {eval_results['overall_score']:.3f}")

    # Example task execution
    try:
        result = ai_layer.process_command(
            "Please pick up the red box from the table and place it on the shelf",
            visual_scene=robot.get_camera_image()
        )
        print(f"Task execution result: {result}")
    except Exception as e:
        print(f"Task execution failed: {e}")

    print("Humanoid robot deployment complete!")

if __name__ == "__main__":
    deploy_humanoid_robot()
```

Building a complete humanoid robot system represents the ultimate test of Physical AI principles, requiring integration of perception, cognition, action, and control in a real physical system. This capstone project demonstrates how all the concepts covered in this book come together to create a truly intelligent, embodied system capable of complex interactions with the physical world.