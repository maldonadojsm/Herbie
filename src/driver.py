from herbie import Herbie


def main():

    with Herbie() as car:
        car.drive_car(60)


if __name__ == '__main__':
    main()