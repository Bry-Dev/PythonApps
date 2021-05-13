import secrets


def do_fibonacci():
    """ Do fibonacci """
    fib_length = int(input("How Long? ( ͡° ͜ʖ ͡°) "))
    b, a = 0, 1
    for i in range(fib_length):
        print(b)
        sum = a + b
        a = b
        b = sum


def create_random_int(n: int = 1000):
    """
    Create random int based on the parameter given

    Args:
        n (int, optional): Max value of the random int. Defaults to 1000.

    Returns:
        int: returns a random int below the given parameter
    """
    return secrets.randbelow(n+1)


def play_time():
    """
    Ask the user to provide the number of 
    tries he/she can have for the game.

    Returns:
        int: Max retries
    """
    while True:
        try:
            max_tries = int(input("How many tries(1 - 10 only)? "))
        except ValueError:
            print("Not number")
            continue
        else:
            if (max_tries > 10 or max_tries < 1):
                print("Select between 1 to 10 only")
                continue
            else:
                return max_tries


def get_min_max(tries: int, game_list: list, secret_num: int):
    """
    Get minimum and maximum int values based on the retries for the guessing game

    Args:
        tries (int): Number of retries
        game_list (list): Percentage list for in-between(min and max) of the game
        secret_num (int): the final answer

    Returns:
        list[tuple]: List of min and max based on the number of retries
    """
    between_list = []
    for times in range(tries):
        min_num = int(
            round(secret_num - (secret_num * game_list[times])))
        max_num = int(
            round(secret_num + (secret_num * game_list[times])))
        between_list.append((min_num, max_num))
    return between_list


def main():
    """ Game Time """
    num_list = [.01, .05, .08, .1, .15, .18, .2, .23, .25, .3]
    num_list_less = [.03, .05, .08, .1, .25, .3, .4, .5, .6, .7]
    secret_number = create_random_int()
    if secret_number <= 100:
        num_list = num_list_less
    tries = play_time()
    game_list = get_min_max(tries, num_list, secret_number)
    print(secret_number)
    for idx, game in enumerate(game_list[::-1]):
        while True:
            try:
                guess_num = int(
                    input(f"Guess the number, it is between {game[0]} and {game[1]}: "))
            except ValueError:
                print("Not number")
                continue
            else:
                break
        if (guess_num == secret_number):
            print("WINNER!")
            break
        elif(idx != len(game_list) - 1):
            print("Try again!")
        else:
            print("Game Lost!")


if __name__ == "__main__":
    main()
