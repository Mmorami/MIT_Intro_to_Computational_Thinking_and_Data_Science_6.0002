#================================
# Part B: Golden Eggs
#================================


# Problem 1
# I chose to implement the function so that it keeps track on the actual eggs taken and the total weight only to see
# the better result better. my previous solution returned the number of steps only and the code was slightly different.
# The problem was that the last 2 tests i've made did not work since some branches included less steps but did not
# maximize the gold value to be taken. in this implementation i force the algorithm to choose the highest amount of gold
# even with a cost of taking extra steps.
def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    # first try to recall if this scenario has been spotted before. the key is a tuple with the list left to consider
    # and the weight still available to pack
    try:
        return memo[(egg_weights, target_weight)]
    # if the scenario never dealt with before compute
    except KeyError:
        # if the list of egg weights is empty or if there is no more space available return 0 and an empty list
        if egg_weights == () or target_weight == 0:
            result = (0, ())
        # if the current item is too heavy to fit in the ship, remove the item from consideration and repeat the flow
        elif egg_weights[-1] > target_weight:
            result = dp_make_weight(egg_weights[:-1], target_weight, memo)
        else:
            # save the item to be taken in this node
            next_item = egg_weights[-1]
            # simulate taking an egg. when taking an egg it doesnt prevent us from taking another one of the same weight
            with_weight, with_count = dp_make_weight(egg_weights, target_weight - next_item)
            # here we count the total weight of the branch
            with_weight += next_item
            # simulate not taking an egg in this node, remove the possibility of taking an egg of this weight.
            # this is because the order of taking is unimportant, so if we dont want to take it now, no reason why
            # we would like to take it in the future.
            without_weight, without_count = dp_make_weight(egg_weights[:-1], target_weight)
            # if the branches result in same total weight we should check which one has less eggs
            if with_weight == without_weight:
                # takes the branch with the fewer eggs/steps that is not 0 eggs.
                if len(with_count) > len(without_count) != len(()):
                    result = (without_weight, without_count)
                else:
                    result = (with_weight, with_count + (next_item,))
            # otherwise takes the branch that amounts to the higher weight
            elif with_weight > without_weight:
                result = (with_weight, with_count + (next_item,))
            else:
                result = (without_weight, without_count)
            # record the specific situation in memp
            memo[(egg_weights, target_weight)] = result
        return result


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", len(dp_make_weight(egg_weights, n)[1]))
    print()

    egg_weights = (1, 6, 14)
    n = 19
    print("Egg weights = (1, 6, 14)")
    print("n = 19")
    print("Expected ouput: 4 (3 * 6 + 1 * 1 = 19)")
    print("Actual output:", len(dp_make_weight(egg_weights, n)[1]))
    print()

    egg_weights = (7, 11, 13)
    n = 73
    print("Egg weights = (7, 11, 13)")
    print("n = 73")
    print("Expected ouput: 7 (6 * 11 + 1 * 7 = 73) or 7 (4 * 13 + 3 * 7))")
    print("Actual output:", len(dp_make_weight(egg_weights, n)[1]))
    print()

    egg_weights = (7, 11, 13)
    n = 30
    print("Egg weights = (7, 11, 13)")
    print("n = 30")
    print("Expected ouput: 3 (2 * 11 + 1 * 7 = 29)")
    print("Actual output:", len(dp_make_weight(egg_weights, n)[1]))
    print()