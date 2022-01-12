#!/usr/bin/env python3
from pprint import pprint


class Flag:
    def __init__(self, name, price, description, colors, stripes, stars):
        self.name = name
        self.price = price
        self.description = description
        self.colors = colors
        self.stripes = stripes
        self.stars = stars

    def __str__(self):
        return f'{self.name} - {self.description} (price: {self.price})'

# self.is_VIP = sum(flag.stars for flag in self.owned_flags) >= 120
# we need a collection of flags such that sum of starts is >=120
class User:
    def __init__(self, name):
        self.name = name
        self.owned_flags = []

        #INTERESTING!
        if name == "Dr. Sheldon Lee Cooper":
            self.is_VIP = True
            self.coins = INITIAL_COINS * 2
        else:
            self.is_VIP = False
            self.coins = INITIAL_COINS

    def __str__(self):
        user_value = self.coins + sum(flag.price for flag in self.owned_flags)
        result = f"User {self.name} "
        result += "(VIP)." if self.is_VIP else "(NON-VIP)"
        result += f" has {str(self.coins)} coins."
        result += f" Account value: {user_value}."

        if self.owned_flags:
            total_colors = sum(flag.colors for flag in self.owned_flags)
            total_stripes = sum(flag.stripes for flag in self.owned_flags)
            total_stars = sum(flag.stars for flag in self.owned_flags)

            result += "\nAverage value per: "
            result += "color (total {}) - {:0.2f}, ".format(total_colors, user_value / total_colors)
            result += "stripe (total {}) - {:0.2f}, ".format(total_stripes, user_value / total_stripes)
            result += "star (total {}) - {:0.2f}.\n".format(total_stars, user_value / total_stars)

            result += "Owned flags:\n"
            result += "\n".join(str(flag) for flag in self.owned_flags)

        result += "\n"
        return result

    #can become a vip
    def buy_flag(self, flag):
        self.coins -= flag.price
        self.owned_flags.append(flag)
        self.update_VIP()

    # can become a vip
    def sell_flag(self, flag):
        self.coins += flag.price
        self.owned_flags.remove(flag)
        self.update_VIP()

    def update_VIP(self):
        if self.is_VIP:
            return  # once VIP, always VIP
        self.is_VIP = sum(flag.stars for flag in self.owned_flags) >= 120  # Real stars collectors can be VIP too :)

    def can_afford_flag(self, flag):
        return self.coins >= flag.price

    def allowed_to_buy_CSA_flag(self):
        return self.is_VIP

#20 Flags, stars is the last argument
 #Our main interest!!!!! index 16
available_flags = [
    Flag("Suriname", 100, "The smallest South American country", 4, 5, 1),
    Flag("Togo", 100, "Has French as the official language", 4, 5, 1),
    Flag("Azerbaijan", 100, "The Land of Fire", 4, 3, 1),
    Flag("Liberia", 200, "Has Africa's cleanest cities", 3, 11, 1),
    Flag("Myanmar", 200, "Formerly known as Burma", 4, 3, 1),
    Flag("Philippines", 300, "Named after King Philip II of Spain", 4, 2, 1),
    Flag("Uzbekistan", 400, "Has the world's largest open-pit gold mine", 4, 5, 12),
    Flag("Tajikistan", 500, "Has the world's second highest dam", 4, 3, 7),
    Flag("Slovenia", 600, "Has the world's longest stone arch railroad bridge", 3, 3, 3),
    Flag("Syria", 700, "Has the world's oldest operational dam", 4, 3, 2),
    Flag("Honduras", 800, "Has a dual capital", 2, 2, 5),
    Flag("Cape Verde", 900, "Named after the Cap-Vert peninsula", 4, 5, 10),
    Flag("Israel", 1000, "The country that brought you CSA", 2, 2, 1),
    Flag("Russia", 1200, "Home to the Hermitage Museum", 3, 3, 0),
    Flag("USA", 1200, "United States of America", 3, 13, 50),
    Flag("Cuba", 1300, "Famous for it's cigars", 3, 5, 1),
    Flag("CSA", 1337, open("flag.txt", "rt").read(), 1, 33, 7),
    Flag("Jordan", 1400, "Home to Petra", 4, 3, 1),
    Flag("Singapore", 1400, "The world's second most densely populated country", 2, 2, 5),
    Flag("Venezuela", 1500, "Home to the world's highest waterfall", 4, 3, 8),
]


def send(message):
    print(message)


# No input sanitization!!!! , returns a string (one line)
def recv():
    return input()


def get_int_from_user():
    try:
        user_selection = int(recv())
        return user_selection
    except:
        return 0


def list_flags(flags):
    res = "=================================\n"
    for i, flag in enumerate(flags):
        res += f'{i} {flag.name} - {flag.price}\n'
    res += "=================================\n"
    return res


def modify_flag_menu():
    raise NotImplementedError  # Sheldon todo - allow users to add and remove stars from their owned flags


def buy_flag_menu():
    send(f"There are {len(available_flags)} flags available to buy.")
    send("How many flags would you like to buy?")
    amount = get_int_from_user()
    if amount > len(available_flags):
        send("There aren't that many available flags!")
        return

    for _ in range(amount):
        send(f"You have {user.coins} coins.")
        if user.coins == 0:
            return

        send("Available flags to buy:")
        send(list_flags(available_flags))
        send("Which flag would you like to buy?")
        flag_index = get_int_from_user()
        flag_to_buy = None
        allowed_to_buy_flag = False
        try:
            if 0 <= flag_index < len(available_flags):
                flag_to_buy = available_flags[flag_index]
                allowed_to_buy_flag = user.can_afford_flag(flag_to_buy)
                log_message = str(user) + f" is trying to buy flag {flag_to_buy.name}"
                if flag_to_buy.name == "CSA":
                    log_message += "\n***ATTENTION - CSA FLAG PURCHASE. RUNNING ADDITIONAL CHECK***"
                    allowed_to_buy_flag = allowed_to_buy_flag and user.allowed_to_buy_CSA_flag()
                    log_message += " Additional checks result - user is " + (
                        "ALLOWED" if allowed_to_buy_flag else "NOT ALLOWED") + " to purchase it"

                send("You tried to buy flag " + flag_to_buy.name + " (allowed to purchase? " + str(
                    allowed_to_buy_flag) + "). This transaction was logged successfully.")
            else:
                log_message = str(user) + " is trying to buy an non-existing flag. This looks suspicious!"
                send("Invalid flag index. This attempt is logged!")

            open("log.txt", "a+").write(log_message + "\n")
        except:
            send(f'Failed to log transaction of flag purchase. Do you have write permission?')

        if flag_to_buy is not None:
            if allowed_to_buy_flag:
                user.buy_flag(flag_to_buy)
                available_flags.remove(flag_to_buy)
                send(f"{flag_to_buy.name} flag bought!")
            else:
                send(f"You can't buy flag {flag_to_buy.name}!")


def sell_flag_menu():
    send(f"You have {len(user.owned_flags)} flags.")
    if not user.owned_flags:
        return
    send("How many flags would you like to sell?")
    amount = get_int_from_user()
    if amount > len(user.owned_flags):
        send("You don't have that many flags!")
        return

    #BUG IN SELL -LOL, should be inside the loop
    flag_to_sell = None
    for _ in range(amount):
        send("Available flags to sell:")
        send(list_flags(user.owned_flags))
        send("Which flag would you like to sell?")
        flag_index = get_int_from_user()

        try:
            if 0 <= flag_index < len(user.owned_flags):
                flag_to_sell = user.owned_flags[flag_index]
                log_message = str(user) + " is selling flag " + flag_to_sell.name
            else:
                log_message = str(user) + " is trying to sell a flag they don't have. This looks suspicious!"
                send("Invalid flag index. This attempt is logged!")

            if flag_to_sell is not None:
                user.sell_flag(flag_to_sell)
                available_flags.append(flag_to_sell)
                send(f"{flag_to_sell.name} flag sold!")
                log_message += f". {flag_to_sell.name} Sold successfully!"

            open("log.txt", "a+").write(log_message + "\n")
        except:
            send(f'Failed to log transaction of {flag_to_sell.name} flag. Do you have write permission?')


def main_menu():


    while True:
        send("What would you like to do?\n")
        send("\n".join([
            #           "0 - MODIFY FLAGS",
            "1 - LIST AVAILABLE FLAGS",
            "2 - BUY FLAG",
            "3 - SELL FLAG",
            "4 - LIST MY FLAGS",
            "5 - LIST MY STATS",
            "6 - EXIT",
        ]))

        try:
            selection = get_int_from_user()
            #HIDDEN FEATURE -modify flag
            if selection == 0:
                modify_flag_menu()
            elif selection == 1:
                send("Available flags to buy:")
                send(list_flags(available_flags))
            elif selection == 2:
                buy_flag_menu()
            elif selection == 3:
                sell_flag_menu()

            elif selection == 4:
                flags_amount = len(user.owned_flags)
                if flags_amount > 0:
                    send(f"You have {flags_amount} flags:")
                    send(list_flags(user.owned_flags))
                else:
                    send("You have no flags :(\n")
            elif selection == 5:
                send(str(user))
            elif selection == 6:  # exit
                break
            else:
                send(f"Invalid menu selection {selection}")
        except:
            send("Apologies, not all functions are implemented yet!")

    send("Hope you had Fun With Flags! Goodbye.")


def logo():
    send("""Welcome to

    █▀▀ █ █ █▄ █   █ █ █ █ ▀█▀ █ █   █▀▀ █   ▄▀█ █▀▀ █▀
    █▀  █▄█ █ ▀█   ▀▄▀▄▀ █  █  █▀█   █▀  █▄▄ █▀█ █▄█ ▄█
    """)


INITIAL_COINS = 1000
user = User("Dr. Amy Farrah Fowler")

if __name__ == '__main__':
    # print(sum(c.stars for c in available_flags)) #total of 118 stars
    # pprint(list(str(s) for s in available_flags))
    # a = available_flags[3]
    # print(a)
    # print()
    # available_flags.remove(a)
    # pprint(list(str(s) for s in available_flags))
    logo()
    main_menu()

