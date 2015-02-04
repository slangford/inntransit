def distance_on_unit_sphere(lat1, long1, lat2, long2):
    """ function to calculate the distance in miles between two nodes (assuming straight line segments on spherical globe) """
    
    import math
    
    if(lat1 - lat2 == 0 and long1 - long2 == 0):
        return 0.
    else:
        degrees_to_radians = math.pi/180.0
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
        arc = math.acos(cos)
        return arc*3960.

def distance_between_points(lat1, long1, lat2, long2):
    """ function to calculate the distance in miles between two nodes assuming straight line on flat surface """

    xdiff = abs(long2 - long1)*57.912
    ydiff = abs(lat2 - lat1)*69.172
    distance = (xdiff**2 + ydiff**2)**(0.5)
    return distance