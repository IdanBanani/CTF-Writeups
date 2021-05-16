# This is used to run the slotmachine locally, the server doesn't use this.
from ServerSide.slotmachine_dummy import Slotmachine, NO_COINS, NOT_ENOUGH_COINS


def main():
    slotmachine = Slotmachine()
    print("You have {} coins".format(slotmachine.total_coins))
    get_next_num = True
    while get_next_num:
        try:
            prize = 0
            coins =  int(input("Enter number of coins:\n"))
            result =  slotmachine.spin(coins)
            if result == NO_COINS:
                get_next_num = False
            elif result != NOT_ENOUGH_COINS:
                prize = slotmachine.get_prize()
            print(result)
            print("You won {} coins!".format(prize))
            print("{} coins left.".format(slotmachine.total_coins))

        except ValueError:
            get_next_num = False
        except NameError:
            get_next_num = False

if __name__ == '__main__':
    main()