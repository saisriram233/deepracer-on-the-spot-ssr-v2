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
[3.17183, -5.09172, 4.0, 0.07531],
[3.43584, -5.23683, 4.0, 0.07531],
[3.69973, -5.38217, 3.77757, 0.07975],
[3.96392, -5.52529, 3.42061, 0.08784],
[4.22886, -5.66344, 3.13285, 0.09538],
[4.49484, -5.79391, 2.89071, 0.10249],
[4.76196, -5.91412, 2.68248, 0.1092],
[5.03016, -6.02161, 2.50354, 0.11541],
[5.29918, -6.11409, 2.33542, 0.12181],
[5.56862, -6.18934, 2.17391, 0.12869],
[5.83788, -6.24518, 2.03158, 0.13536],
[6.10615, -6.27943, 2.03158, 0.13312],
[6.37238, -6.28993, 2.03158, 0.13115],
[6.63516, -6.27418, 2.03158, 0.12958],
[6.89253, -6.22912, 2.03158, 0.12861],
[7.14154, -6.15135, 2.19378, 0.11892],
[7.38142, -6.046, 2.2675, 0.11554],
[7.61099, -5.91502, 2.32967, 0.11345],
[7.82901, -5.75981, 2.39631, 0.11168],
[8.03419, -5.58178, 2.46616, 0.11015],
[8.22522, -5.38241, 2.54193, 0.10862],
[8.40082, -5.16346, 2.60768, 0.10763],
[8.55959, -4.92679, 2.58914, 0.11008],
[8.70002, -4.6745, 2.53653, 0.11383],
[8.82005, -4.4089, 2.48197, 0.11743],
[8.91769, -4.13306, 2.42969, 0.12043],
[8.991, -3.85057, 2.37866, 0.1227],
[9.03859, -3.56532, 2.32135, 0.12458],
[9.05969, -3.28104, 2.2654, 0.12584],
[9.05416, -3.00095, 2.20311, 0.12716],
[9.02236, -2.72778, 2.10978, 0.13035],
[8.96488, -2.46376, 2.0, 0.1351],
[8.88218, -2.21095, 2.0, 0.133],
[8.77473, -1.97127, 2.0, 0.13133],
[8.64273, -1.74681, 2.0, 0.1302],
[8.48553, -1.54047, 2.0, 0.1297],
[8.30203, -1.35639, 2.11705, 0.12277],
[8.09645, -1.19421, 2.24734, 0.11652],
[7.87216, -1.05319, 2.39287, 0.11072],
[7.63201, -0.93241, 2.565, 0.1048],
[7.37853, -0.83064, 2.75305, 0.09922],
[7.11387, -0.74659, 2.98299, 0.09309],
[6.84006, -0.67866, 3.25652, 0.08663],
[6.55891, -0.62505, 3.60218, 0.07946],
[6.27206, -0.58374, 4.0, 0.07245],
[5.98097, -0.55254, 4.0, 0.07319],
[5.68688, -0.52914, 4.0, 0.07375],
[5.39084, -0.51133, 4.0, 0.07414],
[5.09587, -0.48739, 4.0, 0.07399],
[4.80214, -0.45684, 4.0, 0.07383],
[4.50988, -0.41909, 4.0, 0.07367],
[4.21932, -0.37355, 3.90623, 0.07529],
[3.93079, -0.31953, 3.7694, 0.07788],
[3.64462, -0.25648, 3.64194, 0.08046],
[3.3612, -0.18389, 3.52428, 0.08302],
[3.081, -0.10113, 3.4197, 0.08543],
[2.80461, -0.0076, 3.33917, 0.08738],
[2.53272, 0.09731, 3.28359, 0.08875],
[2.26612, 0.21417, 3.25003, 0.08956],
[2.00575, 0.3435, 3.23858, 0.08977],
[1.75263, 0.48568, 3.23858, 0.08964],
[1.5078, 0.64088, 3.23858, 0.08951],
[1.27223, 0.80902, 3.23858, 0.08937],
[1.04678, 0.98979, 3.23858, 0.08923],
[0.83214, 1.18271, 3.25109, 0.08877],
[0.62876, 1.38711, 3.28946, 0.08766],
[0.43688, 1.60222, 3.3572, 0.08586],
[0.25642, 1.82716, 3.46185, 0.0833],
[0.08704, 2.06099, 3.61852, 0.07979],
[-0.0719, 2.30265, 3.86188, 0.0749],
[-0.22148, 2.551, 4.0, 0.07248],
[-0.36291, 2.8049, 4.0, 0.07266],
[-0.49733, 3.0634, 4.0, 0.07284],
[-0.62597, 3.3256, 4.0, 0.07301],
[-0.74985, 3.59074, 3.78434, 0.07733],
[-0.87006, 3.8581, 3.25341, 0.0901],
[-0.98287, 4.11603, 2.89151, 0.09736],
[-1.09882, 4.37129, 2.61154, 0.10735],
[-1.22065, 4.62148, 2.38071, 0.11689],
[-1.35097, 4.86425, 2.38071, 0.11574],
[-1.49234, 5.09713, 2.38071, 0.11443],
[-1.64704, 5.31762, 2.38071, 0.11314],
[-1.81728, 5.52298, 2.38071, 0.11204],
[-2.00516, 5.70986, 2.40708, 0.11009],
[-2.20936, 5.87814, 2.51001, 0.10542],
[-2.42789, 6.0287, 2.60337, 0.10193],
[-2.65928, 6.16209, 2.70239, 0.09883],
[-2.90225, 6.27882, 2.79429, 0.09647],
[-3.15579, 6.37917, 2.89043, 0.09434],
[-3.41897, 6.46338, 2.99677, 0.09221],
[-3.69084, 6.53175, 3.11319, 0.09005],
[-3.97049, 6.58459, 3.23696, 0.08792],
[-4.25695, 6.62228, 3.34356, 0.08641],
[-4.54933, 6.64502, 3.40756, 0.08606],
[-4.84664, 6.65297, 3.28745, 0.09047],
[-5.14748, 6.64603, 3.17369, 0.09482],
[-5.4438, 6.62477, 3.05542, 0.09723],
[-5.73451, 6.58972, 2.93381, 0.09981],
[-6.01897, 6.54055, 2.82201, 0.10229],
[-6.29654, 6.4769, 2.66975, 0.10667],
[-6.56661, 6.39841, 2.50131, 0.11244],
[-6.82846, 6.30458, 2.50131, 0.11121],
[-7.08126, 6.19475, 2.50131, 0.11019],
[-7.32404, 6.06824, 2.50131, 0.10945],
[-7.55527, 5.92368, 2.50131, 0.10902],
[-7.77265, 5.75916, 2.55619, 0.10665],
[-7.97589, 5.57608, 2.60402, 0.10505],
[-8.16445, 5.37561, 2.63472, 0.10445],
[-8.33742, 5.15881, 2.64323, 0.10493],
[-8.49352, 4.92679, 2.60592, 0.10731],
[-8.63128, 4.68106, 2.56723, 0.10973],
[-8.74909, 4.42367, 2.5088, 0.11283],
[-8.84548, 4.15711, 2.44209, 0.11607],
[-8.9193, 3.88423, 2.37672, 0.11894],
[-8.9694, 3.6079, 2.27733, 0.12332],
[-8.99513, 3.33097, 2.17875, 0.12765],
[-8.99591, 3.05609, 2.07998, 0.13216],
[-8.97128, 2.7857, 2.07998, 0.13054],
[-8.92095, 2.52197, 2.07998, 0.12908],
[-8.84382, 2.26719, 2.07998, 0.12798],
[-8.7385, 2.02384, 2.07998, 0.12748],
[-8.60316, 1.79494, 2.32432, 0.11441],
[-8.44411, 1.57908, 2.48798, 0.10777],
[-8.26429, 1.37576, 2.66975, 0.10167],
[-8.06621, 1.18437, 2.87781, 0.09571],
[-7.85213, 1.00416, 3.11726, 0.08977],
[-7.62418, 0.83431, 3.42534, 0.08299],
[-7.38453, 0.6737, 3.84511, 0.07503],
[-7.13548, 0.52089, 4.0, 0.07305],
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

        above_three_five = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 57, 58, 59, 60, 61, 62, 63,80, 81, 82, 83, 84, 85,
                            137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157,
                            158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168]

        above_three = [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                      105, 106, 107, 108, 109, 110, 111, 112]
        above_two_five = [83, 84, 85, 86, 87, 88, 89,  91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104,
                          122, 123, 124, 125, 126, 127, 128, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

        above_two = [90]
        ################## INPUT PARAMETERS ###################

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
