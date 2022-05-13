import json
import sys
import os

def get_num_lane_changes(action_list):
    lane_change_actions = [0, 2]
    lane_changes = 0

    # can only make at most 4 lane changes in the same direction
    direction_change = 0
    curr_direction = -1
    for action in action_list:
        if action in lane_change_actions:
            if action != curr_direction:
                curr_direction = action
                lane_changes += 1
                direction_change = 1
            elif action == curr_direction and direction_change < 3:
                lane_changes += 1
                direction_change += 1
    return lane_changes

for filename in os.listdir('./stats/'):
    stats = open('./stats/' + filename)
    stats_json = json.load(stats)

    collisions = stats_json["episode_crashed"]

    speeds = stats_json["episode_speed"]

    actions = stats_json["episode_action"]

    num_collisions = 0

    avg_speeds = []

    num_lcs = []

    for episode in range(len(collisions)):
        episode_collision = collisions[episode]
        episode_speeds = speeds[episode]
        episode_actions = actions[episode]

        if any(episode_collision):
            num_collisions += 1

        avg_speeds.append(sum(episode_speeds) / len(episode_speeds))

        num_lcs.append(get_num_lane_changes(episode_actions))


    n = filename.split('n')[1].split('_')[0]
    perc = filename.split('agg')[1].split('.')[0]

    print('n=' + n + ', agg=' + perc + '%')

    print(num_collisions/len(collisions))
    print(sum(avg_speeds)/len(avg_speeds))
    print(sum(num_lcs)/len(num_lcs))


