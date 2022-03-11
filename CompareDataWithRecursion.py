import re

import deepdiff

objects_dev = []
objects_new = []
equal_objects = []
non_equal_objects = []
#place:Gwardamarga, Pieta;street:Triq Hookham Frere;number:FL2

def parseObject(param):
    finalObject=dict()
    param=param.replace('{', '')
    param=param.replace('}', '')
    param=param.replace('"','')
    key_value_pairs=param.split(';')
    for key_value in key_value_pairs:
        key_value=key_value.split(':')
        if(len(key_value)>1):
            object_part=key_value[0]
            key_value[1]=key_value[1].strip()
            if key_value[1].startswith('{'):
                key_value[1]=parseObject(key_value[1])
            elif key_value[1].startswith('['):
                key_value[1] = key_value[1].replace("[", "")
                key_value[1] = key_value[1].replace("]", "")
                key_value[1] = key_value[1].replace('"', "")

                key_value[1] = key_value[1].split(",")
                new_key_value = []
                for item in key_value[1]:
                    new_key_value.append(item.strip())
                new_key_value.sort()
            else:
                key_value[1] = key_value[1].replace('"', '')
            finalObject[object_part]=key_value[1]
    return finalObject



def read_file_data(file_path, file_type, object_parts):
    f = open(file_path, 'r')
    line = f.readline()
    object = dict()
    currentPart = ''
    while (line):
        line = line.strip()
        if (line == '' or line == '\n'):
            line = f.readline()
            continue
        if (
                line != '\n' and ' side processing time:' not in line and 'Photo' not in line and 'extraction duration' not in line):
            data = dict()
            line = line.strip()
            line = line.lower()
           # x = line.replace(':', '')
            x = line
            for part in object_parts:
                if (x in part):
                    currentPart = part
                    object[currentPart] = dict()
                    line = f.readline()
                    continue

            key_value = line.split(':')

            if (len(key_value) > 1):
                if ('image' in key_value[0]):
                    if (object):
                        for part in object_parts:
                            try:
                                if (object[part]):
                                    pass
                            except:
                                print('exception')
                                object[part] = dict()

                        if file_type == 'd':
                            objects_dev.append(object)
                        elif file_type == 'n':
                            objects_new.append(object)

                    object = dict()
                    key_value[0] = key_value[0].split(' --> ')[1]
                    object[key_value[0]] = key_value[1]

                else:
                    if ('[' in key_value[1]):
                        key_value[1] = key_value[1].replace("[", "")
                        key_value[1] = key_value[1].replace("]", "")
                        key_value[1] = key_value[1].replace('"', "")

                        key_value[1] = key_value[1].split(",")
                        new_key_value = []
                        for item in key_value[1]:
                            new_key_value.append(item.strip())
                            new_key_value.sort()

                            data[key_value[0].strip()] = new_key_value
                            object[currentPart].update(data)
                    if '{' in key_value[1]:
                        key_value[1] = parseObject(key_value[1])
                        data[key_value[0].strip()] = key_value[1]
                        object[currentPart].update(data)

                    if (isinstance(key_value[1], str)):
                        key_value[1] = key_value[1].replace('"', '')
                        if (currentPart == 'mrz data' and file_type == 'd'):
                            if (key_value[0] == 'validUntil' or key_value[0] == 'dateOfBirth'):
                                date_dev = key_value[1]
                                date_dev = date_dev.strip()
                                date_dev = date_dev.replace('-', '')
                                d = date_dev[:2]
                                m = date_dev[2:4]
                                y = date_dev[4:]
                                date_dev = y + m + d
                                key_value[1] = date_dev
                        if (currentPart):
                            data[key_value[0].strip()] = key_value[1].strip()
                            object[currentPart].update(data)

        line = f.readline()
    for part in object_parts:
        if (not object[part]):
            object[part] = {}

    if file_type == 'd':
        objects_dev.append(object)
    elif file_type == 'n':
        objects_new.append(object)
    f.close()


def print_results(object_parts):
    single_line = '---------------------------------------------------\n'
    double_line = '================================================================================================\n'
    f = open("MLT/Front/ResultFront", "w")

    f.write('Compare result: \n')
    f.write(single_line)
    if len(non_equal_objects) == 0:
        f.write('Matching percent -> 100%')
        return

    for item in non_equal_objects:
        dev = item['dev_object']
        new = item['new_object']
        f.write('Image:' + dev['image'] + ' \n')
        f.write(double_line)
        for op in object_parts:
            f.write(op + '\n')
            f.write(single_line)
            try:
                object_part_dev = dev[op]
                object_part_new = new[op]
                for k in object_part_dev:

                    match = object_part_new[k] == object_part_dev[k]
                    f.write(k + ': ' + str(match) + '\n')
                    if (match == False):
                        f.write(
                            '>>>New value: ' + str(object_part_new[k]) + '\n>>>Dev value: ' + str(
                                object_part_dev[k]) + '\n')

                f.write(double_line)
            except:
                print('exception')

    f.close()


def compareObjects(dev_item, new_item):
    for key in dev_item:
        try:
            if (type(dev_item[key]) == str):
                dev_item[key] = dev_item[key].lower()
                new_item[key] = new_item[key].lower()
                if (dev_item[key] == new_item[key]):
                    continue
                else:
                    return False
            elif type(dev_item[key]) == dict:
                eq = compareObjects(dev_item[key], new_item[key])
                return eq
            elif type(dev_item[key]) == list:
                for list_item in dev_item[key]:
                    list_item = list_item.lower()
                for list_item in new_item[key]:
                    list_item = list_item.lower()
                if (dev_item[key] == new_item[key]):
                    continue
                else:
                    return False
        except:
            print('exception')
            return False

    return True


def compare():
    for dev_item in objects_dev:
        for new_item in objects_new:
            if dev_item['image'] == new_item['image']:
                diff = compareObjects(dev_item, new_item)
                if diff:
                    same = dict(dev_object=dev_item, new_object=new_item)
                    equal_objects.append(same)
                else:
                    distinct = dict(dev_object=dev_item, new_object=new_item)
                    non_equal_objects.append(distinct)


def compareResults(dev_file_path, new_file_path, object_parts):
    read_file_data(dev_file_path, 'd', object_parts)
    read_file_data(new_file_path, 'n', object_parts)
    compare()
    print_results(object_parts)


compareResults('MLT/Front/oldFrontside.txt', 'MLT/Front/newFrontside.txt', ['front data'])
print(objects_dev[4])
