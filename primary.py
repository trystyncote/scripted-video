from script_manager import Scripter


def primary():
    xar = Scripter("sample_script.txt")

    for iar in xar:
        print(iar)


if __name__ == "__main__":
    primary()
