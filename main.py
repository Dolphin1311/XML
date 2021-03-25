from xml.dom import minidom
from xml.parsers.expat import ExpatError
import os.path


class Car:
    def __init__(self, brand: str, model: str, speed: float, count_seats: int):
        self.brand = brand
        self.model = model
        self.speed = speed
        self.count_seats = count_seats

    def __str__(self):
        return self.brand + ' ' + self.model


def create_xml_file(filename):
    """Create xml file"""
    root = minidom.Document()
    xml = root.createElement('car')
    root.appendChild(xml)
    xml_str = root.toprettyxml(indent='\t')

    with open(filename, 'w') as fw:
        fw.write(xml_str)


def add_car(car: Car):
    """Add car's info to XML file"""
    # check if xml file exists
    if not check_if_xml_exists(filename):
        create_xml_file()
        print('File xml was created successfully')

    # write to file main tag if it is no here
    if not check_xml_for_writing(filename):
        with open(filename, 'a') as file:
            file.write('<cars/>')

    tree = minidom.parse(filename)
    root = tree.documentElement

    # create main element
    new_car = tree.createElement('car')
    new_car.setAttribute('brand', car.brand)

    # create child elements
    model = tree.createElement('model')
    model.appendChild(tree.createTextNode(car.model))

    speed = tree.createElement('speed')
    speed.appendChild(tree.createTextNode(str(car.speed)))

    count_of_seats = tree.createElement('count_seats')
    count_of_seats.appendChild(tree.createTextNode(str(car.count_seats)))

    # append elements to main element
    new_car.appendChild(model)
    new_car.appendChild(speed)
    new_car.appendChild(count_of_seats)

    root.appendChild(new_car)

    # for prettying xml
    # pretty_xml = tree.toprettyxml()
    # file.write(pretty_xml)

    save_changes(tree)
    print('Car was added successfully!')


def show_xml_file():
    """Show all data from XML file in good formatting"""
    # check if xml file exists
    if not check_if_xml_exists(filename):
        create_xml_file()
        print('File xml was created successfully')

    # write to file main tag if it is no here
    if not check_xml_for_writing(filename):
        with open(filename, 'a') as file:
            file.write('<cars/>')

    tree = minidom.parse(filename)
    root = tree.documentElement

    # get all cars
    cars = root.childNodes

    for index, car in enumerate(cars):
        print(f'-----Car #{index}-----')
        if car.hasAttribute('brand'):
            print(f'Brand: {car.getAttribute("brand")}')

        # show info
        print(f'Model: {car.getElementsByTagName("model")[0].childNodes[0].data}')
        print(f'Speed: {car.getElementsByTagName("speed")[0].childNodes[0].data}')
        print(f'Count of seats: {car.getElementsByTagName("count_seats")[0].childNodes[0].data}')


def delete_car(car_number: int):
    """Delete all data about one car"""
    # check if xml file exists
    if not check_if_xml_exists(filename):
        create_xml_file()
        print('File xml was created successfully')

    # write to file main tag if it is no here
    if not check_xml_for_writing(filename):
        with open(filename, 'a') as file:
            file.write('<cars/>')

    tree = minidom.parse(filename)
    root = tree.documentElement

    try:
        car = root.childNodes[car_number]
    except IndexError:
        print('There is no such car!')
        return

    root.removeChild(car)

    save_changes(tree)
    print('Car was deleted successfully!')


def update_car(car_number: int, brand: str, model: str, speed: float, count_seats: int):
    """Update data about one car"""
    # check if xml file exists
    if not check_if_xml_exists(filename):
        create_xml_file()
        print('File xml was created successfully')

    # write to file main tag if it is no here
    if not check_xml_for_writing(filename):
        with open(filename, 'a') as file:
            file.write('<cars/>')

    tree = minidom.parse(filename)
    root = tree.documentElement
    speed = str(speed)
    count_seats = str(count_seats)

    try:
        car = root.childNodes[car_number]
    except IndexError:
        print('There is no such car!')
        return

    # set new data
    if car.hasAttribute('brand'):
        car.setAttribute('brand', brand)

    car.getElementsByTagName('model')[0].childNodes[0].nodeValue = model
    car.getElementsByTagName('speed')[0].childNodes[0].nodeValue = speed
    car.getElementsByTagName('count_seats')[0].childNodes[0].nodeValue = count_seats

    save_changes(tree)
    print('Car was updated successfully!')


def check_if_xml_exists(filename):
    if not os.path.exists('cars.xml'):
        return False

    return True


def check_xml_for_writing(filename):
    try:
        minidom.parse(filename)
        return True
    except ExpatError:
        return False


def save_changes(tree):
    with open(filename, 'w') as file:
        tree.writexml(file)


filename = 'cars.xml'

# if there is no XML file => create it
if not check_if_xml_exists(filename):
    create_xml_file(filename)

choose = ''

while choose != 0:
    print('1)Add car\n'
          '2)Delete car\n'
          '3)Update car\n'
          '4)Show all cars\n'
          '0)Exit')
    try:
        choose = int(input('Enter number: '))
    except ValueError:
        print('Enter only number!')

    if choose == 1:
        brand = input('Enter car\'s brand: ')
        model = input('Enter car\'s model: ')
        try:
            count_of_seats = int(input('Enter car\'s count of seats: '))
            speed = float(input('Enter car\'s max speed: '))

            # create instance of Car object
            car = Car(brand, model, speed, count_of_seats)
            add_car(car)
        except ValueError:
            print('Enter correct value')
    elif choose == 2:
        car_number = int(input('Enter car\'s number that you want to delete: '))
        delete_car(car_number)
    elif choose == 3:
        car_number = int(input('Enter car\'s number that you want to update: '))
        new_brand = input('Enter new brand: ')
        new_model = input('Enter new model: ')

        try:
            new_speed = float(input('Enter new speed: '))
            new_count_of_seats = int(input('Enter new count of seats: '))

            update_car(car_number, new_brand, new_model, new_speed, new_count_of_seats)
        except ValueError:
            print('Enter correct value')

    elif choose == 4:
        show_xml_file()
