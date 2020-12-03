
import os
import pandas
import path as path

UNSORTED_BASE_FOLDER = "D:/PythonProject/scic_new/"
SORTED_BASE_FOLDER = "D:/PythonProject/"
count = 0


def compute_per_venue_data_set(csv_file):
    df = pandas.read_csv(csv_file)
    a = df.groupby('TC ID').apply(lambda g: g.values.tolist()).to_dict()
    # return a
    global count  # declare a to be a global
    first_key = [key for key, val in a.items()][count]
    for key, val in a.items():
        if first_key == key:
            # print("first_key",first_key)
            str = val
            # print("vall",val)
            count = count + 1
            # print("strr",str)
            #print("aa",a)
    return str, a


def compute_per_candidate_timeline(venue_data_set):
    # todo: Compute per candidate timeline
    # return per_candidate_timeline
    #list = venue_data_set
    per_candidate_timeline ={}
    for candidate in venue_data_set:
        per_candidate_timeline[candidate[0]] = candidate[1:]
    #print("list", per_candidate_timeline)
    return per_candidate_timeline


def create_folders(venue_name, candidate_id,candidate_timeline):
    converted_num = str(venue_name)
    converted_num1 = str(candidate_id)
    #print("candidate id", candidate_id)
    #print("venue_name", venue_name)
    #print("canditimeline",candidate_timeline[3])
    for i in range (venue_name):
        path1 = os.path.join(SORTED_BASE_FOLDER, converted_num)
        os.mkdir(path1)
        if venue_name == candidate_timeline[3] :
            path = os.path.join(SORTED_BASE_FOLDER, converted_num, converted_num1)
            if not os.path.exists(path):
                os.mkdir(path)


def is_ip_folder(folder_name):
    # check the given folder name to see if it is actually an IP
    # folder. We dont want to mess with random non IP folders which
    # got put into the venue-path
    # print("foldername",folder_name)
    isdir = os.path.isdir(folder_name)
    # print("isdir",isdir)
    if isdir == True:
        True
        # print("folder exist")
    else:
        False
        # print("folder does not exist")
    return True


def parse_image_name(image_file_name):
    # todo: Parse the given file name and parse the capture-ts. Return
    # this capture-ts
    image_name = image_file_name.replace(".jpeg", "")
    final_image = image_name.replace('_', " ")
    final_image_name = final_image.replace('-', "")
    name = final_image_name.replace(' ', "")
    # final_image_name=datetime.strptime(final_image, '%Y-%m-%d %H-%M-%S')
    # print("image_nm",final_image)
    # print("img_filenam",name)

    capture_ts = name
    return capture_ts


def compute_image_name_list(venue_name):
    # Construct a dict of the following form:
    #
    # { '192.168.1.1': [
    #    (202011111011, "2020-11-11_10-11-00.jpeg"),
    #    (...), ...
    #   ],
    # }
    #
    # print("venue_nm",venue_name)
    converted_num = str(venue_name)
    venue_path = os.path.join(UNSORTED_BASE_FOLDER)
    #print("venupath", venue_path)
    venue_path_contents = os.listdir(venue_path)
    #print("venupathcont", venue_path_contents)
    image_name_list = {}
    for element in venue_path_contents:
        #print("elem",element)
        element_path = os.path.join(venue_path, element)
        #print("element_path",element_path)
        if not os.path.isdir(element_path):
            # we want to ignore the normal files, if any. We want only
            # the IP folders.
            continue
        if not is_ip_folder(element):
            continue
        image_name_list[element] = []
        image_elements = os.listdir(element_path)
        #print("img_elemnt",image_elements)
        for image_element in image_elements:
            # print("img_ele",image_elements)
            capture_ts = parse_image_name(image_element)
            # print("capture_ts",capture_ts)
            image_name_list[element].append((capture_ts, image_element))
            #print("image_nm_list", image_name_list)
    return image_name_list


def process_venue(venue, venue_data_set):
    print("vv",venue)
    print("dst",venue_data_set)
    venue_image_list = compute_image_name_list(venue)
    #print("ven_imag_list",venue_image_list)
    per_candidate_timeline = compute_per_candidate_timeline(venue_data_set)
    print("percandtime", per_candidate_timeline)
    for candidate, timeline in per_candidate_timeline.items():
        #print("candi", per_candidate_timeline.keys())
        print("timeline", timeline)
        create_folders(venue, candidate, timeline)
        #print("venue", venue)
        #print("c", candidate)
        for timeline_entry in timeline:
            #print("timeline",timeline)
            #print("timeline_entry", timeline_entry)
            ip_image_list = venue_image_list[timeline[0]]
            #print("ip_imag_list", ip_image_list)
            for image_entry in ip_image_list:
                #print("img_entry", image_entry)
                if image_entry[0] >= timeline[1] and \
                        image_entry[0] <= timeline[2]:
                    #print("img_entry", image_entry)
                    image_path = path.join(
                        UNSORTED_BASE_FOLDER, venue,
                        timeline[0], image_entry[1])
                    target_path = path.join(
                        SORTED_BASE_FOLDER, venue, candidate, image_entry[1])
                    print("imag_path", image_path)
                    os.copyfile(target_path, image_path)


def main():
    # todo: Get this from the commandline as a parameter
    csv_file = "Result.csv"
    # a ,b = compute_per_venue_data_set(csv_file)
    # a, b = compute_per_venue_data_set(csv_file)
    # b = compute_per_venue_data_set(csv_file)
    # print("a",a)
    # print("b",b)
    per_venue_data_set, per_venue_dict = compute_per_venue_data_set(csv_file)
    compute_per_candidate_timeline(per_venue_data_set)
    print("pervenue", per_venue_data_set)
    # print("venue dict",per_venue_dict)
    for venue, venue_data_set in per_venue_dict.items():
        process_venue(venue, venue_data_set)
        # print("vv",venue)
        # print("vds",venue_data_set)
    """per_venue_data_set, per_venue_dict = compute_per_venue_data_set(csv_file)
    compute_per_candidate_timeline(per_venue_data_set)
    print("pervenue", per_venue_data_set)
    print("venue dict", per_venue_dict)

    per_venue_data_set, per_venue_dict = compute_per_venue_data_set(csv_file)
    compute_per_candidate_timeline(per_venue_data_set)
    print("pervenue", per_venue_data_set)
    print("venue dict", per_venue_dict)"""

    """per_venue_data_set = compute_per_venue_data_set(csv_file)
    compute_per_candidate_timeline(per_venue_data_set)
    print("pervenue",per_venue_data_set)

    per_venue_data_set = compute_per_venue_data_set(csv_file)
    compute_per_candidate_timeline(per_venue_data_set)
    print("pervenue", per_venue_data_set)

    per_venue_data_set = compute_per_venue_data_set(csv_file)
    compute_per_candidate_timeline(per_venue_data_set)
    print("pervenue", per_venue_data_set)"""

    # pool = mp.Pool(size=30)
    # plist = []
    # for venue, venue_data_set in per_venue_data_set.items():
    # process_venue(venue, venue_data_set)
    # p = pool.Process(process_venue(venue, venue_data_set))
    # plist.append(p)
    # for p in plist:
    # p.join()


if __name__ == "__main__":
    main()
