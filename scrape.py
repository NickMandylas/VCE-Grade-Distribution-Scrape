from tika import parser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import csv


def get_pdfs(y):
    folder_location = os.getcwd() + "/PDF/"

    while y < 2020:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/Users/nickmandylas/Downloads/chromedriver", chrome_options=chrome_options)
        driver.get(
            'https://www.vcaa.vic.edu.au/administration/research-and-statistics/performance-senior-secondary/Pages/'
            + str(y) + '-grade-dist.aspx')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        for link in soup.select("a[href$='.pdf']"):
            print(link.find('span').getText())
            print(link.get('href'))

            name = str(link.find('span').getText())
            if name[0] == " ":
                name = name[1:]

            filename = folder_location + "/" + str(y) + "/" + name + ".pdf"
            with open(filename, 'wb') as f:
                f.write(requests.get("https://www.vcaa.vic.edu.au/" + link.get('href')).content)

        y += 1

def get_data_small(filename):
    data = parser.from_file(filename)
    data['content'] = data['content']
    lines = data['content'].splitlines()

    data = [[], [], [], [], [], [], [], [], []]

    index = 0
    count = -1
    for each in lines:
        index += 1
        temp_list = each.split(" ")

        # Max
        if temp_list.__contains__("Max"):
            count += 1
            data[count].append(temp_list[len(temp_list) - 1])
            data[count].append(lines[index + 1])
            data[count].append(lines[index + 3])
            data[count].append('0')

            del temp_list[len(temp_list) - 3:len(temp_list) - 1]

            for i in range(len(temp_list) - 2, -1, -1):
                v_range = temp_list[i].split("-")
                for item in v_range:
                    data[count + 3].append(item)

    return data


def get_data(filename):
    data = parser.from_file(filename)
    data['content'] = data['content']
    lines = data['content'].splitlines()

    data = [[], [], [], [], [], [], [], [], []]

    count = -1
    for each in lines:
        temp_list = each.split(" ")

        # Max
        if temp_list.__contains__("Max"):
            count += 1
            data[count].append(temp_list[len(temp_list) - 1])

        # Mean
        if temp_list[0] == 'Mean' and len(temp_list) > 1:
            data[count].append(temp_list[1])
        elif temp_list[0] == 'Mean':
            data[count].append(0)

        # SD
        if temp_list[0] == 'Std' and len(temp_list) > 2:
            data[count].append(temp_list[2])
        elif temp_list[0] == 'Std':
            data[count].append(0)

        # Student Totals
        # if temp_list[0] == 'Total' and len(temp_list) > 5:
        #     temp_list.remove('n')
        #     temp_list[len(temp_list) - 1] = temp_list[len(temp_list) - 1].replace(",", '')
        #     del temp_list[len(temp_list) - 2]
        #     del temp_list[0]
        #     data[count + 6].append(temp_list)

        # Score Ranges
        if temp_list[0] == 'Score':
            del temp_list[0:2]
            del temp_list[len(temp_list) - 3:len(temp_list) - 1]

            for i in range(len(temp_list) - 2, -1, -1):
                v_range = temp_list[i].split("-")
                for each in v_range:
                    data[count + 3].append(each)

    for i in range(0, 3, 1):
        data[i].append('0')

    if not data[3]:
        data = get_data_small(filename)

    return data


subjects = []
year = 2017
csv_data = [["Subject", "Year", "GA1 Max", "GA1 Mean", "GA1 Std D", "GA1 Weight", "GA2 Max", "GA2 Mean", "GA2 Std D",
             "GA2 Weight", "GA3 Max", "GA3 Mean", "GA3 Std D", "GA3 Weight", "GA1 A+ Low", "GA1 A+ High", "GA1 A Low",
             "GA1 A High", "GA1 B+ Low", "GA1 B+ High", "GA1 B Low", "GA1 B High", "GA1 C+ Low", "GA1 C+ High",
             "GA1 C Low", "GA1 C High", "GA1 D+ Low", "GA1 D+ High", "GA1 D Low", "GA1 D High", "GA1 E+ Low",
             "GA1 E+ High", "GA1 E Low", "GA1 E High", "GA1 UG Low", "GA1 UG High", "GA2 A+ Low", "GA2 A+ High",
             "GA2 A Low", "GA2 A High", "GA2 B+ Low", "GA2 B+ High", "GA2 B Low", "GA2 B High", "GA2 C+ Low",
             "GA2 C+ High", "GA2 C Low", "GA2 C High", "GA2 D+ Low", "GA2 D+ High", "GA2 D Low", "GA2 D High",
             "GA2 E+ Low", "GA2 E+ High", "GA2 E Low", "GA2 E High", "GA2 UG Low", "GA2 UG High", "GA3 A+ Low",
             "GA3 A+ High", "GA3 A Low", "GA3 A High", "GA3 B+ Low", "GA3 B+ High", "GA3 B Low", "GA3 B High",
             "GA3 C+ Low", "GA3 C+ High", "GA3 C Low", "GA3 C High", "GA3 D+ Low", "GA3 D+ High", "GA3 D Low",
             "GA3 D High", "GA3 E+ Low", "GA3 E+ High", "GA3 E Low", "GA3 E High", "GA3 UG Low", "GA3 UG High"]]

# Download PDFs
get_pdfs(year)

# Scrape PDF Data
while year < 2020:
    for filename in os.listdir(os.getcwd() + "/PDF/" + str(year) + "/"):
        subject = filename.replace(".pdf", "")
        if not subject.__contains__("VET"):
            subjects.append(subject)

    for each in subjects:
        print(each, year)
        sub_data = get_data(os.getcwd() + "/PDF/" + str(year) + "/" + each + ".pdf")
        temp_data = [each, year]

        for i in range(0, len(sub_data)):
            for j in range(0, len(sub_data[i])):
                temp_data.append(sub_data[i][j])

        print(len(temp_data))

        csv_data.append(temp_data)

    year += 1
    subjects = []

# Write CSV file
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)