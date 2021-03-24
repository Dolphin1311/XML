import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path


class Car:
    def __init__(self, brand: str, model: str, speed: float, count_seats: int):
        self.brand = brand
        self.model = model
        self.speed = speed
        self.count_seats = count_seats

    def __str__(self):
        return self.brand + ' ' + self.model


def create_xml(filename):
    """Create xml file"""
    root = minidom.Document()
    xml = root.createElement('Car')
    root.appendChild(xml)
    xml_str = root.toprettyxml(indent='\t')

    with open(filename, 'w') as fw:
        fw.write(xml_str)


def add_car_to_xml(car: Car):
    tree = ET.parse(filename)
    root = tree.getroot()

    # create elements
    child = ET.Element('Car')
    child.set('brand', car.brand)
    model = ET.SubElement(child, 'model')
    model.text = car.model
    speed = ET.SubElement(child, 'speed')
    speed.text = str(car.speed)
    count_of_seats = ET.SubElement(child, 'count_seats')
    count_of_seats.text = str(car.count_seats)

    root.append(child)

    # add data to XML file
    with open(filename, 'wb') as file:
        tree.write(file)


filename = 'cars.xml'
# if there is no XML file => create it
if not os.path.exists('cars.xml'):
    create_xml(filename)

choose = 1

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
            add_car_to_xml(car)
        except ValueError:
            print('Enter correct value')
    if choose == 4:
        tree = minidom.parse(filename)
        root = tree.documentElement

        # get all cars
        cars = root.getElementsByTagName('car')

        for car in cars:
            print('-----Car-----')
            if car.hasAttribute('brand'):
                print(f'Brand: {car.getAttribute("brand")}')

            # show info
            print(f'Model: {car.getElementsByTagName("model")[0].childNodes[0].data}')
            print(f'Speed: {car.getElementsByTagName("speed")[0].childNodes[0].data}')
            print(f'Count of seats: {car.getElementsByTagName("count_seats")[0].childNodes[0].data}')
