from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================


# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # opens the file "filename" and specify read purpose. the "with" keyword promise correct handling of the file,
    # closing it at the end of use even when an error occurs
    with open(filename, 'r') as f:
        cows_dict = {}
        # reading through the lines in the file
        for line in f.readlines():
            # strips each line from a new-line char and splits it to both its components - name and weight
            cow_info = line.strip('\n').split(',')
            # building the dictionary
            cows_dict[cow_info[0]] = cow_info[1]
    return cows_dict


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # initializing the list of trip lists
    trip_list = []
    # sorting the dictionary into a list of tuples, sorted by weight - highest first
    sorted_cows_list = sorted(list(cows.items()), key=lambda cows_tup: cows_tup[1], reverse=True)
    # eliminating the cows that singly exceed the weight limit for transport
    sorted_cows_list = [tup for tup in sorted_cows_list if int(tup[1]) <= limit]
    # while we didnt transported all cows
    while sorted_cows_list:
        # initializing a single trip list, the trip current weight, and copying the list for iteration purposes
        sing_trip = []
        trip_curr_weight = 0
        sorted_per_trip = sorted_cows_list.copy()
        # while the current weight is less than the limit
        while trip_curr_weight < limit and sorted_per_trip:
            # pop the info of the heaviest cow and save it
            heaviest_cow = sorted_per_trip.pop(0)
            # if the weight of the cow + the current weight on the ship is within limit
            if int(heaviest_cow[1]) + trip_curr_weight <= limit:
                # add the cow's name to the trip's list
                sing_trip.append(heaviest_cow[0])
                # sum up the weight on this trip
                trip_curr_weight += int(heaviest_cow[1])
                # pop the cow from the main cows' list
                sorted_cows_list.remove(heaviest_cow)
        if sing_trip:
            trip_list.append(sing_trip)
    return trip_list

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    pass
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass

file_name = "ps1_cow_data.txt"
print(load_cows(file_name))
print(greedy_cow_transport(load_cows(file_name), 10))

file_name = "ps1_cow_data_2.txt"
print(load_cows(file_name))