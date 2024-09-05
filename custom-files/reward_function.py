import numpy as np

def reward_function(params):
    

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    steering_angle = params['steering_angle']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']
    heading = params['heading']

    
    reward = 1e-3

    
    if not all_wheels_on_track:
        return 1e-3  # Immediate low reward if the car is off track

    # 2. Reward for staying close to the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 3.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += 1e-3  # likely near or off track

    # 3. Adjust speed based on track curvature
    CURVATURE_THRESHOLD = 10  # Assumed curvature threshold for sharper turns
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    track_direction = np.arctan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    heading_diff = abs(track_direction - np.radians(heading))

    # Penalize sharp turns if speed is too high
    if heading_diff > CURVATURE_THRESHOLD:
        if speed > 2.0:
            reward *= 0.5  # Reduce reward in sharp turns if going too fast
    else:
        if speed > 2.5 and distance_from_center <= marker_1:
            reward += 2.0  # Encourage high speed on straight segments
        elif speed > 2.0 and distance_from_center <= marker_2:
            reward += 1.0

    # 4. Penalize zig-zagging or sudden steering changes
    ABS_STEERING_THRESHOLD = 15
    if abs(steering_angle) > ABS_STEERING_THRESHOLD:
        reward *= 0.8  # Reduce reward for sharp steering

    # 5. Reward smooth progress (progress/steps)
    step_reward = (progress / steps) * 10
    reward += step_reward

    # Return final reward
    return float(reward)
