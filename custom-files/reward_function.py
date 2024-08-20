import math


class Reward:
    def __init__(self):
        self.first_racingpoint_index = 0

    def reward_function(self, params):

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):

            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [[-1.60662, -1.51464, 3.28598, 0.06429],
[-1.40162, -1.57805, 3.54868, 0.06047],
[-1.18656, -1.62816, 3.87264, 0.05702],
[-0.95969, -1.66644, 4.0, 0.05752],
[-0.7188, -1.69411, 4.0, 0.06062],
[-0.46147, -1.71227, 4.0, 0.06449],
[-0.18604, -1.72221, 4.0, 0.0689],
[0.1064, -1.72575, 4.0, 0.07311],
[0.4139, -1.72559, 3.23953, 0.09492],
[0.72164, -1.72567, 2.69761, 0.11408],
[1.02939, -1.72617, 2.35443, 0.13071],
[1.33302, -1.72132, 2.11436, 0.14362],
[1.62373, -1.69728, 1.91429, 0.15238],
[1.89295, -1.64457, 1.7592, 0.15594],
[2.13208, -1.55926, 1.62579, 0.15616],
[2.33453, -1.44237, 1.5, 0.15585],
[2.49578, -1.29778, 1.5, 0.14439],
[2.6113, -1.13028, 1.5, 0.13565],
[2.67615, -0.94582, 1.5, 0.13035],
[2.68279, -0.75207, 1.5, 0.12924],
[2.61848, -0.56269, 1.68411, 0.11876],
[2.49437, -0.39127, 1.93985, 0.10909],
[2.32151, -0.24444, 2.2085, 0.1027],
[2.10748, -0.12604, 2.62602, 0.09314],
[1.8618, -0.03519, 3.40606, 0.0769],
[1.59614, 0.03523, 4.0, 0.06871],
[1.32503, 0.12844, 4.0, 0.07167],
[1.06105, 0.23753, 4.0, 0.07141],
[0.80296, 0.35949, 4.0, 0.07136],
[0.54961, 0.49165, 4.0, 0.07144],
[0.29982, 0.6314, 4.0, 0.07156],
[0.05246, 0.77631, 3.73254, 0.0768],
[-0.1936, 0.92395, 3.23537, 0.08869],
[-0.43486, 1.0678, 2.86839, 0.09793],
[-0.67798, 1.20337, 2.59185, 0.1074],
[-0.92416, 1.3235, 2.3641, 0.11587],
[-1.17369, 1.42146, 2.16644, 0.12374],
[-1.42562, 1.4912, 1.99956, 0.13073],
[-1.67748, 1.52701, 1.85578, 0.13708],
[-1.92496, 1.52392, 1.85578, 0.13336],
[-2.16165, 1.47784, 1.85578, 0.12994],
[-2.37878, 1.38565, 1.85578, 0.12711],
[-2.56517, 1.246, 1.85578, 0.1255],
[-2.70664, 1.05918, 2.3035, 0.10173],
[-2.81398, 0.84489, 2.44001, 0.09823],
[-2.88652, 0.60658, 2.54459, 0.0979],
[-2.92133, 0.34607, 2.6148, 0.10052],
[-2.9127, 0.06526, 2.67975, 0.10484],
[-2.85556, -0.22337, 2.74214, 0.1073],
[-2.7597, -0.48435, 2.68258, 0.10364],
[-2.63673, -0.71231, 2.68258, 0.09655],
[-2.49444, -0.90949, 2.68258, 0.09064],
[-2.33761, -1.07864, 2.68258, 0.08599],
[-2.16929, -1.22211, 2.68258, 0.08245],
[-1.99041, -1.3397, 2.85537, 0.07497],
[-1.80274, -1.43607, 3.04928, 0.06919]]
        # planned speed based on waypoints
        # manually adjust the list for better performance, e.g. lower the speed before turning
        above_three_five = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 93, 94, 95, 114, 115, 116, 117, 118]
        above_three = [12, 41, 71, 91, 92, 96, 97, 112, 113]
        above_two_five = [13, 14, 40, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 88, 89, 90, 98, 99, 110, 111]
        above_two = [38, 39, 75, 76, 86, 87, 100, 101, 108, 109]
        below_two = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 77, 78, 79, 80, 81, 82, 83, 84, 85, 102, 103, 104, 105, 106, 107]
        # planned speed based on waypoints
        # observe which side the car is expected to run at
        right_track = [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
        center_track = [118, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 47, 61]
        left_track = [i for i in range(0, 119) if i not in right_track + center_track]

        # obvious sides
        strong_left = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
        strong_right = [50, 51, 52, 53, 54, 55, 56]

        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        x = params['x']
        y = params['y']
        distance_from_center = params['distance_from_center']
        is_left_of_center = params['is_left_of_center']
        heading = params['heading']
        progress = params['progress']
        steps = params['steps']
        speed = params['speed']
        steering_angle = abs(params['steering_angle'])
        track_width = params['track_width']
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################
        reward = 1e-3

        # Zero reward if off track ##
        if is_offtrack is True:
            return reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            return reward

        # Reward if car goes close to optimal racing line
        def get_distance_reward(threshold, distance, multiplier):
            distance_reward = max(0, 1 - (distance / threshold))

            return distance_reward * multiplier

        DIST_THRESH = track_width * 0.5
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])

        if (distance_from_center < 0.01 * track_width):
            if closest_index in center_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
        elif is_left_of_center:
            if closest_index in left_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_left:
                reward += get_distance_reward(DIST_THRESH, dist, 5)
        else:
            if closest_index in right_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_right:
                reward += get_distance_reward(DIST_THRESH, dist, 5)

        def get_speed_reward(ceiling, threshold, diff):
            return ceiling - diff/threshold

        # Reward if speed falls within optimal range
        PENALTY_RATIO = 0.9
        SPEED_DIFF_NO_REWARD = 1
        speed_diff = abs(optimals[2]-speed)
        if speed_diff > SPEED_DIFF_NO_REWARD:
            return 1e-3

        if closest_index in above_three_five:
            if speed >= 3.5:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 3:
                reward *= PENALTY_RATIO
        elif closest_index in above_three:
            if speed >= 3:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 8:
                reward *= PENALTY_RATIO
        elif closest_index in above_two_five:
            if speed >= 2.5:
                reward += get_speed_reward(0.8, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 15:
                reward *= PENALTY_RATIO
        elif closest_index in above_two:
            if speed >= 2:
                reward += get_speed_reward(1, SPEED_DIFF_NO_REWARD, speed_diff)
        else:
            if speed < 2:
                reward += get_speed_reward(3, SPEED_DIFF_NO_REWARD, speed_diff)

        # Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 2000 # should be adapted to track length and other rewards
        TARGET_STEPS = 110
        if progress == 100:
            reward += REWARD_FOR_FASTEST_TIME / (steps - TARGET_STEPS)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()


def reward_function(params):
    return reward_object.reward_function(params)
