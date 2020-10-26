import csv, os, shutil
from datetime import datetime
import pandas

def parse_csv(csv_path):
	line_count = 0
	for line_count,row in enumerate(csv_path):
			if line_count == 0:
				continue


def create_images(key,a):
    dstfolder="D:/PythonProject/"
    srcfolder="D:/PythonProject/scic_new/"

    folder_name = key
    starttime = datetime.now()
    filectr = 0
    for i in range(len(folder_name) - 1):
        # path = D+"%s" % folder_name[i+1]
        path = dstfolder + "/%s" % folder_name[i + 1]
        os.mkdir(path)
    """
    Seperated nested for loops , earlier if there were 'm' unique test centers and 'n' candidates then there would be m*n  iterations
    now there are only m+n iterations thus improving time complexity
    """
    for j in range(len(a) - 1):
        # if folder_name[i + 1] == df['TC ID'][j + 1]:
        # candidate_folder = path + "/%s" % df['Candidate ID'][j + 1]
        candidate_folder = dstfolder + "/%s" % a['TC ID'][j + 1] + "/%s" % a['Candidate ID'][j + 1]
        if not os.path.exists(candidate_folder):
            os.mkdir(candidate_folder)
        else:
            shutil.rmtree(candidate_folder)  # Removes all the subdirectories!
            os.makedirs(candidate_folder)
        # ip_path=D +"/scic/%s " % df['IP Address'][j+1]
        ip_path = srcfolder + "/%s " % a['IP Address'][j + 1]
        if (os.path.exists(ip_path)):
            ip_add = a['IP Address'][j + 1].replace(" ", "")
            # ip_path = D + "scic/" + ip_add
            ip_path = srcfolder + "/" + ip_add
            start = datetime.strptime(a['Start Time'][j + 1], '%d/%b/%Y %H:%M:%S %p')
            end = datetime.strptime(a['End Time'][j + 1], '%d/%b/%Y %H:%M:%S %p')
            print("ip_path", ip_path)
            if (os.path.exists(ip_path)):
                for images in os.listdir(ip_path):
                    date = images.replace(".jpeg", "")
                    final_date = date.replace('_', " ")
                    check_date = datetime.strptime(final_date, '%Y-%m-%d %H-%M-%S')
                    src = ip_path
                    dst = candidate_folder
                    # print("source:",src)
                    if start <= check_date and end >= check_date:
                        print(src, dst)
                        filectr = filectr + 1
                        shutil.copyfile(src + "/%s" % images, dst + "/%s" % images)


if __name__ == "__main__":
    df = pandas.read_csv('Result.csv')
    a = df.groupby('TC ID').apply(lambda g: g.values.tolist()).to_dict()
    print(a)
    res = []
    for key, val in a.items():
        res.append([key] + val)
        print("res", res)
        create_images(key,a)
