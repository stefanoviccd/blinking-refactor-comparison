import json

objects_dev = []
objects_new = []
equal_objects = []
non_equal_objects = []


def read_file_data(file_path, file_type):

    f = open(file_path, 'r')
    line = f.readline()
    object = dict()
    while (line):
        #object = dict()
        while (
                '=====================================================================================================================' not in line):

            if ('processing time' not in line):
                key_value = line.split(':')
                if (len(key_value) > 1):
                    if (' --> ' in key_value[0]):
                        if file_type == 'd':
                            objects_dev.append(object)
                        elif file_type == 'n':
                            objects_new.append(object)
                        print(object)
                        object=dict()
                        key_value[0] = key_value[0].split(' --> ')[1]

                    if ('[' in key_value[1]):
                        key_value[1] = key_value[1].replace("[", "")
                        key_value[1] = key_value[1].replace("]", "")
                        key_value[1] = key_value[1].replace('"', "")

                        key_value[1] = key_value[1].split(",")
                        new_key_value = []
                        for item in key_value[1]:
                            new_key_value.append(item.strip())
                        new_key_value.sort()
                        object[key_value[0].strip()] = new_key_value

                    if (isinstance(key_value[1], str)):
                        key_value[1] = key_value[1].replace('"', '')
                        object[key_value[0].strip()] = key_value[1].strip()

            line = f.readline()


        """if file_type == 'd':
            objects_dev.append(object)
        elif file_type == 'n':
            objects_new.append(object)
        print(object)
"""
        line = f.readline()

    f.close()



def compare():
    for dev_item in objects_dev:
        for new_item in objects_new:
            if dev_item['Image'] == new_item['Image']:
                if dev_item == new_item:
                    same = dict(dev_object=dev_item, new_object=new_item)
                    equal_objects.append(same)
                else:
                    distinct = dict(dev_object=dev_item, new_object=new_item)
                    non_equal_objects.append(distinct)


def print_results():
    if (len(non_equal_objects) > 0):
        matching_percent = len(equal_objects) / (len(equal_objects) + len(non_equal_objects)) * 100
    else:
        matching_percent = 100
    print('Percent od matching objects --> ', matching_percent, '%')
    print('----------------------------------------------------')
    print('Distinct values: ')
    # print(neObjects)
    print(json.dumps(non_equal_objects, indent=4))


def compareResults(dev_file_path, new_file_path):
    read_file_data(dev_file_path, 'd')
    read_file_data(new_file_path, 'n')
    compare()
    print_results()


compareResults('frontDataDev.txt', 'frontDataNew.txt')
