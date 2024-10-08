import math

def reward_function(params) :

    max_speed = 3.8
    speed_control = -5
    center_lane = [0,1,2,3,4,5,6,7,8,9,10,11,35,36,37,38,165,166,167,168,169,202,203,204,205,206,207,208,209]
    reward = 0.001
   
    # Read input variables
    x = params['x']
    y = params['y']
    speed = params['speed']
    heading = params['heading']
    waypoints = params['waypoints']
    is_offtrack = params['is_offtrack']
    steering = abs(params['steering_angle'])
    closest_waypoints = params['closest_waypoints']
    all_wheels_on_track = params['all_wheels_on_track']
    center_variance = params["distance_from_center"] / params["track_width"]
   
   
    next_waypoint_index = closest_waypoints[1]
    look_ahead_distance = 4
    look_ahead_index = (next_waypoint_index + look_ahead_distance) % len(waypoints)
    look_ahead_waypoint = waypoints[look_ahead_index]

    waypoint_x, waypoint_y = look_ahead_waypoint
    desired_heading = math.degrees(math.atan2(waypoint_y - y, waypoint_x - x))
   
    heading_diff = abs(desired_heading - heading)
    if heading_diff > 180:
        heading_diff = abs(360 - heading_diff)
       
       
    if not is_offtrack and all_wheels_on_track:
        reward += round(min(100/(1+abs((max_speed*10)-((speed*10)+heading_diff)+(speed_control/4)*(4-speed))),100))

        if  steering == 0:
            reward += 50
        elif steering < 5:
            reward += 25

        if next_waypoint_index in center_lane and center_variance < 0.4:
            reward += 50


    return float(reward)
