# A very elegant and clever implementation of the algorithm by @John-L-Jones-IV i found on github.
# notice that my last test makes the algorithm crash as it assumes that the limit can be reached exactly.

def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    NOTE: memo will keep memory of how it was built the first time it was used. It is possible to use the wrong memo on the set of
    egg_weights. Or build a completly invalid memo when called again with a new set of egg_weights.

    Returns: int, smallest number of eggs needed to make target weight
    """
    # memo's key is the target weight. if the target weight is not in memo check if it can be reached in 1 step
    if target_weight not in memo:
        if target_weight in egg_weights:
            # save the fastest rout - 1 step
            memo[target_weight] = 1
        elif target_weight < min(egg_weights):
            return 0  # can't get any closer to target, stop adding eggs
        else:
            memo[target_weight] = min(
                # do the first line for each egg weight in the list
                1 + dp_make_weight(egg_weights, target_weight - egg_weight, memo)
                for egg_weight in egg_weights if target_weight > egg_weight
            )

    return memo.get(target_weight)


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 26
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 26")
    print("Expected ouput: 2 (25 + 1 = 26)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    n = 100
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 100")
    print("Expected ouput: 4 (4 * 25 = 100)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    n = 7
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 7")
    print("Expected ouput: 3 (1 * 5 + 2 * 1 = 100)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    n = 101
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 101")
    print("Expected ouput: 5 (4 * 25 + 1 * 1 = 100)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 5, 10, 20)
    n = 99
    print("Egg weights = ", egg_weights)
    print("n = ", n)
    print("Expected ouput: 10 (4 * 20 + 1 * 10 + 1 * 5 + 4 * 1 = 99)")
    # print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print()

    n = 100
    print("Egg weights = ", egg_weights)
    print("n = ", n)
    print("Expected ouput: 5 (5 * 20 = 100)")
    # print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print()

    egg_weights = (7, 11, 13)
    n = 30
    print("Egg weights = (7, 11, 13)")
    print("n = 30")
    print("Expected ouput: 3 (2 * 11 + 1 * 7 = 29)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()