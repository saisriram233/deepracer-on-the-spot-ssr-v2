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
        racing_track = [[-0.11087, -3.28924, 4.0, 0.04281],
[0.00309, -3.3518, 4.0, 0.0325],
[0.11704, -3.41436, 4.0, 0.0325],
[0.26716, -3.49678, 4.0, 0.04281],
[0.53122, -3.64176, 4.0, 0.07531],
[0.79529, -3.78674, 4.0, 0.07531],
[1.05936, -3.93172, 4.0, 0.07531],
[1.32342, -4.07671, 4.0, 0.07531],
[1.58749, -4.22169, 4.0, 0.07531],
[1.85157, -4.36664, 4.0, 0.07531],
[2.11566, -4.51158, 4.0, 0.07531],
[2.37975, -4.65651, 4.0, 0.07531],
[2.6438, -4.80153, 4.0, 0.07531],
[2.9078, -4.94666, 4.0, 0.07531],
[3.17183, -5.09172, 3.72948, 0.08078],
[3.43584, -5.23683, 3.19405, 0.09432],
[3.69973, -5.38217, 2.83318, 0.10634],
[3.96392, -5.52529, 2.56546, 0.11712],
[4.22886, -5.66344, 2.34964, 0.12717],
[4.49484, -5.79391, 2.16803, 0.13665],
[4.76196, -5.91412, 2.01186, 0.1456],
[5.03016, -6.02161, 1.87766, 0.15388],
[5.29918, -6.11409, 1.75156, 0.16241],
[5.56862, -6.18934, 1.63044, 0.17158],
[5.83788, -6.24518, 1.52368, 0.18048],
[6.10615, -6.27943, 1.52368, 0.17749],
[6.37238, -6.28993, 1.52368, 0.17486],
[6.63516, -6.27418, 1.52368, 0.17278],
[6.89253, -6.22912, 1.52368, 0.17148],
[7.14154, -6.15135, 1.64534, 0.15855],
[7.38142, -6.046, 1.70062, 0.15405],
[7.61099, -5.91502, 1.74726, 0.15127],
[7.82901, -5.75981, 1.79723, 0.14891],
[8.03419, -5.58178, 1.84962, 0.14687],
[8.22522, -5.38241, 1.90645, 0.14483],
[8.40082, -5.16346, 1.95576, 0.14351],
[8.55959, -4.92679, 1.94185, 0.14677],
[8.70002, -4.6745, 1.9024, 0.15177],
[8.82005, -4.4089, 1.86147, 0.15657],
[8.91769, -4.13306, 1.82227, 0.16058],
[8.991, -3.85057, 1.78399, 0.16359],
[9.03859, -3.56532, 1.74101, 0.1661],
[9.05969, -3.28104, 1.69905, 0.16778],
[9.05416, -3.00095, 1.65233, 0.16954],
[9.02236, -2.72778, 1.58233, 0.17381],
[8.96488, -2.46376, 1.5, 0.18013],
[8.88218, -2.21095, 1.5, 0.17733],
[8.77473, -1.97127, 1.5, 0.17511],
[8.64273, -1.74681, 1.5, 0.1736],
[8.48553, -1.54047, 1.5, 0.17293],
[8.30203, -1.35639, 1.58779, 0.16369],
[8.09645, -1.19421, 1.6855, 0.15536],
[7.87216, -1.05319, 1.79465, 0.14762],
[7.63201, -0.93241, 1.92375, 0.13973],
[7.37853, -0.83064, 2.06479, 0.13229],
[7.11387, -0.74659, 2.23724, 0.12412],
[6.84006, -0.67866, 2.44239, 0.11551],
[6.55891, -0.62505, 2.70164, 0.10594],
[6.27206, -0.58374, 3.03814, 0.09539],
[5.98097, -0.55254, 3.51361, 0.08332],
[5.68688, -0.52914, 3.53783, 0.08339],
[5.39084, -0.51133, 3.37699, 0.08782],
[5.09587, -0.48739, 3.2582, 0.09083],
[4.80214, -0.45684, 3.15147, 0.09371],
[4.50988, -0.41909, 3.03761, 0.09702],
[4.21932, -0.37355, 2.92967, 0.10039],
[3.93079, -0.31953, 2.82705, 0.10383],
[3.64462, -0.25648, 2.73145, 0.10728],
[3.3612, -0.18389, 2.64321, 0.11069],
[3.081, -0.10113, 2.56478, 0.11391],
[2.80461, -0.0076, 2.50438, 0.11651],
[2.53272, 0.09731, 2.46269, 0.11834],
[2.26612, 0.21417, 2.43752, 0.11942],
[2.00575, 0.3435, 2.42893, 0.11969],
[1.75263, 0.48568, 2.42893, 0.11952],
[1.5078, 0.64088, 2.42893, 0.11934],
[1.27223, 0.80902, 2.42893, 0.11916],
[1.04678, 0.98979, 2.42893, 0.11897],
[0.83214, 1.18271, 2.43832, 0.11836],
[0.62876, 1.38711, 2.4671, 0.11688],
[0.43688, 1.60222, 2.5179, 0.11448],
[0.25642, 1.82716, 2.59639, 0.11107],
[0.08704, 2.06099, 2.71389, 0.10639],
[-0.0719, 2.30265, 2.89641, 0.09986],
[-0.22148, 2.551, 3.1389, 0.09236],
[-0.36291, 2.8049, 3.41537, 0.0851],
[-0.49733, 3.0634, 3.78285, 0.07702],
[-0.62597, 3.3256, 3.46437, 0.0843],
[-0.74985, 3.59074, 2.83826, 0.10311],
[-0.87006, 3.8581, 2.44006, 0.12014],
[-0.98287, 4.11603, 2.16863, 0.12982],
[-1.09882, 4.37129, 1.95865, 0.14314],
[-1.22065, 4.62148, 1.78553, 0.15585],
[-1.35097, 4.86425, 1.78553, 0.15432],
[-1.49234, 5.09713, 1.78553, 0.15257],
[-1.64704, 5.31762, 1.78553, 0.15085],
[-1.81728, 5.52298, 1.78553, 0.14939],
[-2.00516, 5.70986, 1.80531, 0.14679],
[-2.20936, 5.87814, 1.8825, 0.14056],
[-2.42789, 6.0287, 1.95252, 0.13591],
[-2.65928, 6.16209, 2.02679, 0.13178],
[-2.90225, 6.27882, 2.09572, 0.12862],
[-3.15579, 6.37917, 2.16782, 0.12578],
[-3.41897, 6.46338, 2.24757, 0.12294],
[-3.69084, 6.53175, 2.33489, 0.12007],
[-3.97049, 6.58459, 2.42772, 0.11723],
[-4.25695, 6.62228, 2.50767, 0.11522],
[-4.54933, 6.64502, 2.55567, 0.11475],
[-4.84664, 6.65297, 2.46558, 0.12063],
[-5.14748, 6.64603, 2.38027, 0.12643],
[-5.4438, 6.62477, 2.29157, 0.12964],
[-5.73451, 6.58972, 2.20036, 0.13308],
[-6.01897, 6.54055, 2.11651, 0.13639],
[-6.29654, 6.4769, 2.00231, 0.14222],
[-6.56661, 6.39841, 1.87598, 0.14992],
[-6.82846, 6.30458, 1.87598, 0.14827],
[-7.08126, 6.19475, 1.87598, 0.14692],
[-7.32404, 6.06824, 1.87598, 0.14593],
[-7.55527, 5.92368, 1.87598, 0.14536],
[-7.77265, 5.75916, 1.91714, 0.1422],
[-7.97589, 5.57608, 1.95301, 0.14006],
[-8.16445, 5.37561, 1.97604, 0.13927],
[-8.33742, 5.15881, 1.98242, 0.1399],
[-8.49352, 4.92679, 1.95444, 0.14308],
[-8.63128, 4.68106, 1.92542, 0.14631],
[-8.74909, 4.42367, 1.8816, 0.15044],
[-8.84548, 4.15711, 1.83157, 0.15476],
[-8.9193, 3.88423, 1.78254, 0.15859],
[-8.9694, 3.6079, 1.708, 0.16442],
[-8.99513, 3.33097, 1.63406, 0.1702],
[-8.99591, 3.05609, 1.55999, 0.17621],
[-8.97128, 2.7857, 1.55999, 0.17405],
[-8.92095, 2.52197, 1.55999, 0.17211],
[-8.84382, 2.26719, 1.55999, 0.17064],
[-8.7385, 2.02384, 1.55999, 0.16998],
[-8.60316, 1.79494, 1.74324, 0.15254],
[-8.44411, 1.57908, 1.86598, 0.14369],
[-8.26429, 1.37576, 2.00231, 0.13556],
[-8.06621, 1.18437, 2.15836, 0.12762],
[-7.85213, 1.00416, 2.33795, 0.11969],
[-7.62418, 0.83431, 2.569, 0.11066],
[-7.38453, 0.6737, 2.88383, 0.10004],
[-7.13548, 0.52089, 3.34869, 0.08726],
[-6.87928, 0.37413, 4.0, 0.07381],
[-6.61795, 0.23143, 4.0, 0.07444],
[-6.35327, 0.09067, 4.0, 0.07494],
[-6.08715, -0.05025, 4.0, 0.07528],
[-5.82117, -0.19144, 4.0, 0.07528],
[-5.55532, -0.3329, 4.0, 0.07528],
[-5.28961, -0.47462, 4.0, 0.07529],
[-5.02401, -0.61656, 4.0, 0.07529],
[-4.75852, -0.75873, 4.0, 0.07529],
[-4.4931, -0.90104, 4.0, 0.07529],
[-4.2278, -1.04359, 4.0, 0.07529],
[-3.96262, -1.18636, 4.0, 0.07529],
[-3.69756, -1.32937, 4.0, 0.0753],
[-3.43261, -1.47261, 4.0, 0.0753],
[-3.16778, -1.61609, 4.0, 0.0753],
[-2.90307, -1.75981, 4.0, 0.0753],
[-2.63849, -1.90376, 4.0, 0.0753],
[-2.37402, -2.04794, 4.0, 0.07531],
[-2.10967, -2.19236, 4.0, 0.07531],
[-1.84543, -2.33702, 4.0, 0.07531],
[-1.58133, -2.48192, 4.0, 0.07531],
[-1.31726, -2.6269, 4.0, 0.07531],
[-1.05319, -2.77189, 4.0, 0.07531],
[-0.78912, -2.91687, 4.0, 0.07531],
[-0.52505, -3.06184, 4.0, 0.07531],
[-0.26098, -3.20682, 4.0, 0.07531]]
        ################## WAYPOINTS ##########################
        above_three_five = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                    137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157,
                    158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168]

        above_three = [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]
        above_two_five = [67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]

        above_two = [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130,30, 31, 32,
                     33, 34, 35, 36, 37, 38, 39, 40]


        right_track = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]
        center_track = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                        103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 
                        149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168]
        right_track = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]
        center_track = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                      103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 
                      149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168]
        left_track = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
                      56, 57, 58, 59, 60, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 113, 114,
                      115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136]


        strong_left = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
                      112, 113, 114, 115, 116, 117, 118, 119, 120, 129, 130, 131, 132, 133, 134, 
                      135, 136, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        strong_right = [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]



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
        TARGET_STEPS = 169
        if progress == 100:
            reward += REWARD_FOR_FASTEST_TIME / (steps - TARGET_STEPS)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()


def reward_function(params):
    return reward_object.reward_function(params)
