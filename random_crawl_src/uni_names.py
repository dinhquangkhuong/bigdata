import requests
from bs4 import BeautifulSoup

file_path = "uni_names.txt"
url = "https://vi.wikipedia.org/wiki/Danh_sách_trường_đại_học,_học_viện_và_cao_đẳng_tại_Việt_Nam"

def contains_substring(string, substrings):
    for substring in substrings:
        if substring in string:
            return True
    return False

def get_uni_names(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ols = soup.find_all("ol", class_=False)

        tables = soup.find_all("table")
        class_to_remove = "nowraplinks mw-collapsible autocollapse navbox-inner mw-made-collapsible mw-collapsed"
        # Remove table elements with the specified class
        tables_without_class = [table for table in tables if class_to_remove not in table.get('class', '')]

        all_rows = []

        for table in tables_without_class:
            rows = table.find_all("tr")
            
            for row in rows:
                # Extract text from each cell in the row and append to the list
                row_data = [cell.get_text(strip=True) for cell in row.find_all(["td"])]
                all_rows.append(row_data)

        result = []
        substrings = ["Đại học", "Trường", "Học viện"]
        for row in all_rows:
            for data in row:
                for sub in substrings:
                    if data.startswith(sub) and len(data) > 7:
                        result.append(data)
                        continue

        for ol in ols:
            lis = ol.find_all("li")
            for li in lis:
                result.append(li.get_text(strip=True))

        return result
    else:
        print("Failed.")

names = get_uni_names(url)
with open(file_path, "a", encoding="utf-8") as file:
    for element in names:
        file.write(element + "\n")