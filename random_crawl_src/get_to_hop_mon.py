import requests
import csv
from bs4 import BeautifulSoup

def get_group(soup):
    group = []
    strong = soup.find_all('strong')
    for s in strong:
        if s.text.startswith("Khối"):
            print(s.text)
            group.append(s.text.strip())

    csv_file = "random_crawl_src/data/khối.csv"

    # Writing the list to a CSV file
    with open(csv_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Value"])
        # Write data with IDs
        for idx, value in enumerate(group, start=1):
            writer.writerow([idx, value])

    print(f"List has been written to '{csv_file}' successfully.")

def get_subject(soup):
    group = ('A', 'B', 'C', 'D', 'H', 'K', 'M', 'N', 'R', 'S', 'T', 'V')
    paragrs = soup.find_all('p')
    temp = []
    for p in paragrs:
        if p.text.startswith(group) and ':' in p.text:
            temp.append(p.text)

    all_subjects = []
    for string in temp:
        new = string.split("\n")
        all_subjects.extend(new)

    all_subjects.pop(0)
    codes = []
    subjects_included = []
    for subject in all_subjects:
        substrings = subject.split(":")
        for index, substring in enumerate(substrings):
            if index % 2 == 0:
                codes.append(substring.strip())
            else:
                subjects_included.append(substring.strip())

    # print("Total: ", len(codes))
    # print("All codes: ", codes)
    # print("All subjects: ", subjects_included)
    csv_file = "random_crawl_src/data/tổ_hợp_môn.csv"
    with open(csv_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Value", "Subjects included"])
        for idx, (code, subject) in enumerate(zip(codes, subjects_included), start=1):
            writer.writerow([idx, code, subject])

    print(f"List has been written to '{csv_file}' successfully.")

url = "https://huongnghiep.hocmai.vn/to-hop-mon-la-gi-danh-sach-tat-ca-cac-to-hop-mon-thi-tot-nghiep-thpt/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

get_subject(soup)