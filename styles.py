from colorama import Fore, Back, Style


class ColorStyle:
    def __init__(self) -> None:
        self.__reset = Back.RESET + Fore.RESET + Style.RESET_ALL
        self.__user = Fore.MAGENTA + Style.BRIGHT
        self.__warning = Fore.YELLOW + Style.BRIGHT
        self.__error = Fore.RED + Style.BRIGHT
        self.__success = Fore.GREEN + Style.BRIGHT
        self.__bright = Style.BRIGHT

    def bright(self, text: str):
        return self.__bright + text + self.__reset

    def warning(self, text: str):
        return self.__warning + text + self.__reset

    def error(self, text: str):
        return self.__error + text + self.__reset

    def success(self, text: str):
        return self.__success + text + self.__reset

    def user(self, text: str):
        return self.__user + text + self.__reset
