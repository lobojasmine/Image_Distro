import csv, os, shutil
import multiprocessing
from datetime import datetime
from multiprocessing import Process
from timeit import default_timer as timer



def parse_csv(csv_path):
    line_count = 0
    start = timer()
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line_count,row in enumerate(csv_reader):
            if line_count == 0:
                continue
            create_images(row[0], row[1], row[2], row[3], row[4])
            end = timer()
            print("elapsed time:", {end - start})

def create_images(candidate, ip, start, end, tc):
    dstfolder = "D:/PythonProject"
    srcfolder = "D:/PythonProject/scic_new"
    candidate_folder = os.path.join(dstfolder, tc, candidate)
    if not os.path.exists(candidate_folder):
        os.makedirs(candidate_folder)
    print(candidate_folder)

    ip_path = os.path.join(srcfolder, ip)
    start = datetime.strptime(start, '%d/%b/%Y %H:%M:%S %p')
    end = datetime.strptime(end, '%d/%b/%Y %H:%M:%S %p')
    print(ip_path)
    if os.path.exists(ip_path):
        for images in os.listdir(ip_path):
            date = images.replace(".jpeg", "")
            final_date = date.replace('_', " ")
            check_date = datetime.strptime(final_date, '%Y-%m-%d %H-%M-%S')
            src = ip_path
            dst = candidate_folder
            if start <= check_date and end >= check_date:
                print(src, dst)
                file_to_copy = os.path.join(src, images)
                dst_to_copy = os.path.join(dst, images)
                shutil.copyfile(file_to_copy, dst_to_copy)


def main():
    start = timer()
    print(start)
    p = Process(target=parse_csv, args=('Result.csv',))
    p.start()
    end = timer()
    print(end)
    print("elapsed time:", {end - start})




if __name__ == "__main__":
    main()