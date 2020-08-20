from herbie import Herbie
import sys


def main():

    with Herbie() as car:
        car.drive_car(40)


if __name__ == '__main__':
    main()
