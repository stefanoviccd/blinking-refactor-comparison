import traceback
import sys
import argparse

objects_dev = []
objects_new = []
equal_objects = []
non_equal_objects = []


def parseObject(param):
    finalObject = dict()

    param = param.replace('{', '')
    param = param.replace('}', '')
    param = param.replace('"', '')
    key_value_pairs = param.split(';')
    for key_value in key_value_pairs:
        key_value = key_value.split(':')
        if len(key_value) > 1:
            object_part = key_value[0].strip()
            key_value[1] = key_value[1].strip()
            if key_value[1].startswith('{'):
                key_value[1] = parseObject(key_value[1])
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
            finalObject[object_part] = key_value[1]
    return finalObject


def parseToArray(value):
    value = value.replace("[", "")
    value = value.replace("]", "")
    value = value.replace('"', "")

    value = value.split(",")
    new_key_value = []
    for item in value:
        new_key_value.append(item.strip())
    new_key_value.sort()
    return new_key_value


def formatDate(value):
    date_dev = value
    date_dev = date_dev.strip()
    date_dev = date_dev.replace('-', '')
    d = date_dev[:2]
    m = date_dev[2:4]
    y = date_dev[4:]
    date_dev = y + m + d
    value = date_dev
    return value


def read_file_data(file_path, file_type, object_parts):
    f = open(file_path, 'r')
    line = f.readline()
    object = dict()
    current_part = ''
    if object_parts == []:
        current_part = 'data'
    while line:
        line = line.strip()
        if line == '' or line == '\n':
            line = f.readline()
            continue
        if line != '\n' and ' side processing time:' not in line and 'Photo' not in line and 'extraction duration' not in line:
            data = dict()
            line = line.strip()
            # line = line.lower()
            line_lower = line.lower()
            for part in object_parts:
                if part in line_lower:
                    current_part = part
                    object[current_part] = dict()
                    line = f.readline()
                    continue
            if '{' in line:
                line=line.strip()
                key_value = line.split('{')
                key_value[0] = key_value[0].replace(':', '')
                key_value[1] = '{'+key_value[1]

                key_value[1] = parseObject(key_value[1])
                data[key_value[0].strip()] = key_value[1]
                object[current_part].update(data)
                line=f.readline()
                continue
            else:
                key_value=line.split(':')

            if len(key_value) > 1:
                if 'Image' in key_value[0]:
                    if object:
                        for part in object_parts:
                            try:
                                if object[part]:
                                    pass
                            except:
                                object[part] = dict()

                        if file_type == 'd':
                            objects_dev.append(object)
                        elif file_type == 'n':
                            objects_new.append(object)

                    object = dict()
                    key_value[0] = key_value[0].split('-->')[1]
                    object[key_value[0].strip()] = key_value[1]

                else:
                    key_value[1] = key_value[1].replace('"', '')
                    if '[' in key_value[1]:
                        new_key_value = parseToArray(key_value[1])
                        new_key_value.sort()
                        data[key_value[0].strip()] = new_key_value
                        object[current_part].update(data)
                    elif isinstance(key_value[1], str):
                        key_value[1].replace('"', '')
                        if current_part == 'mrz data' and file_type == 'd':
                            if key_value[0] == 'validUntil' or key_value[0] == 'dateOfBirth':
                                key_value[1] = formatDate(key_value[1])
                        if current_part:
                            data[key_value[0].strip()] = key_value[1].strip()
                            object[current_part].update(data)

        line = f.readline()
    for part in object_parts:
        if not object[part]:
            object[part] = {}

    if file_type == 'd':
        objects_dev.append(object)
    elif file_type == 'n':
        objects_new.append(object)
    f.close()


def print_results(object_parts, result_file_path):
    blank_space = '  '
    single_line = '---------------------------------------------------\n'
    double_line = '===================================================\n'
    f = open(result_file_path, "w")

    f.write(blank_space + 'Compare result: \n')
    f.write(blank_space + single_line)
    if len(non_equal_objects) == 0:
        f.write(blank_space + 'Matching percent -> 100%')
        return

    for item in non_equal_objects:
        dev = item['dev_object']
        new = item['new_object']
        f.write(blank_space + 'Image:' + dev['Image'] + ' \n')
        f.write(blank_space + double_line)
        for op in object_parts:
            f.write(blank_space + op + '\n')
            f.write(blank_space + single_line)
            if dev[op] == {}:
                f.write(blank_space + str(op) + ' NOT READED IN DEV FILE \n')
            if new[op] == {}:
                f.write(blank_space + str(op) + ' NOT READED IN NEW FILE \n')

            try:
                object_part_dev = dev[op]
                object_part_new = new[op]
                for k in object_part_dev:
                    match = object_part_new[k] == object_part_dev[k]
                    if type(object_part_dev[k]) == str:
                        dev_lower = object_part_dev[k].lower()
                        new_lower = object_part_new[k].lower()
                        match = dev_lower == new_lower
                    elif type(object_part_dev[k]) == list:
                        dev_lower = object_part_dev[k].copy()
                        new_lower = object_part_new[k].copy()
                        i = 0
                        while i < len(dev_lower):
                            dev_lower[i] = dev_lower[i].lower()
                            i = i + 1
                        i = 0
                        while i < len(new_lower):
                            new_lower[i] = new_lower[i].lower()
                            i = i + 1
                        dev_lower.sort()
                        new_lower.sort()
                        match = dev_lower == new_lower

                    f.write(blank_space + k + ': ' + str(match) + '\n')
                    if (match == False):
                        f.write(
                            blank_space + '>>>New value: ' + str(
                                object_part_new[k]) + '\n' + blank_space + '>>>Dev value: ' + str(
                                object_part_dev[k]) + '\n')

                f.write(blank_space + double_line)
            except:
                traceback.print_exc()

    f.close()


def compareObjects(dev_item, new_item):
    for key in dev_item:
        if dev_item[key] == {} or dev_item[key] == {}:
            return False
        try:
            if type(dev_item[key]) == dict:
                eq = compareObjects(dev_item[key], new_item[key])
                return eq
            if (type(dev_item[key]) == str):
                if (dev_item[key].lower() == new_item[key].lower()):
                    continue
                else:
                    return False
            if type(dev_item[key]) == list:
                dev_list_lower = []
                new_list_lower = []
                for list_item in dev_item[key]:
                    li = list_item
                    li = li.lower()
                    dev_list_lower.append(li)
                for list_item in new_item[key]:
                    li = list_item
                    li = li.lower()
                    new_list_lower.append(li)
                dev_list_lower.sort()
                new_list_lower.sort()
                if (dev_list_lower == new_list_lower):
                    continue
                else:
                    return False
        except:
            traceback.print_exc()
            return False

    return True


def compare():
    for dev_item in objects_dev:
        for new_item in objects_new:
            if dev_item['Image'] == new_item['Image']:
                diff = compareObjects(dev_item, new_item)
                if diff:
                    pass
                else:
                    distinct = dict(dev_object=dev_item, new_object=new_item)
                    non_equal_objects.append(distinct)


def compareResults(dev_file_path, new_file_path, object_parts, result_file_path):
    read_file_data(dev_file_path, 'd', object_parts)
    read_file_data(new_file_path, 'n', object_parts)
    compare()
    print_results(object_parts, result_file_path)


#compareResults('/home/blinking/Front/oldFrontSide.txt', '/home/blinking/Front/newFrontSide.txt', ['front data'], '/home/blinking/Front/ResultFront.txt')
CLI=argparse.ArgumentParser()
CLI.add_argument(
  "--dev_file_path",
  #nargs="*",
  type=str,
)
CLI.add_argument(
  "--new_file_path",
  #nargs="*",
  type=str,
)
CLI.add_argument(
  "--keys",
  nargs="*",
  type=str,
    default=['data']
)
CLI.add_argument(
  "--result_file_path",
  #nargs="*",
  type=str,
)

# parse the command line
args = CLI.parse_args()
compareResults(args.dev_file_path, args.new_file_path, args.keys, args.result_file_path)



