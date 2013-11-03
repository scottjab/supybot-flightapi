#!/usr/bin/env python


def wind_ratio(wind, runway):
    if wind > 90 and wind < 270:
        return abs(wind - runway)
    else:
        return abs(reciprocal(wind) - reciprocal(runway))


def reciprocal(runway):
    if runway > 180:
        return runway - 180
    return runway + 180


def best_runway(wind, runways):
    runways = sorted(runways)
    fixed_runways = []
    for runway in runways:
        if len(runway) > 2:
            runway = runways[:-1]
        fixed_runways.append(int(runway) * 10)
    ratios = [wind_ratio(wind, runway) for runway in fixed_runways]
    ratios = sorted(zip(ratios, runways))
    last = -1
    color_list = []
    for runway in ratios:
        if last == -1:
            last = runway[0]
        if runway[0] == last:
            color_list.append((runway[1], True))
        else:
            color_list.append((runway[1], False))
    returned_list = []
    runway_count = len(color_list)
    for i in range(runway_count / 2):
        reciprocal = None
        for runway in color_list:
            if runway[0] == find_runway_reciprocal(color_list[i][0]):
                reciprocal = runway
        runway_set = (color_list[i], reciprocal)
        returned_list.append(runway_set)
    return returned_list


def find_runway_reciprocal(runway):
    runway_heading = 0
    runway_position = None
    reciprocal_position = None
    reciprocal_heading = None

    if len(runway) > 2:
        runway_position = runway[2]
        runway_heading = int(runway[:-1])
    else:
        runway_heading = int(runway)
    if runway_heading <= 18:
        reciprocal_heading = runway_heading + 18
    else:
        reciprocal_heading = runway_heading - 18

    if runway_position is not None:
        if runway_position == 'R':
            reciprocal_position = 'L'
        elif runway_position == 'L':
            reciprocal_position = 'R'
        else:
            reciprocal_position = 'C'
    if reciprocal_heading < 10:
        reciprocal_heading = '0%s' % (reciprocal_heading, )
    if reciprocal_position is not None:
        return str(reciprocal_heading) + reciprocal_position
    else:
        return str(reciprocal_heading)
