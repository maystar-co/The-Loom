from datetime import datetime, timedelta
import csv 

urls=[]
base_url = "https://web.archive.org/web/"
start_datetime_str = "20220703213746"
end_datatime_str="20220708213746"
end_url ="https://www.bobble.ai/en/home"


def write_list_to_csv(links, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

def increment_archive_url(base_url, start_datetime_str):
  
  start_datetime = datetime.strptime(start_datetime_str, "%Y%m%d%H%M%S")
  new_datetime = start_datetime + timedelta(minutes=60)
  new_datetime_str = new_datetime.strftime("%Y%m%d%H%M%S")
  return f"{base_url}{new_datetime_str}/{base_url.split('/')[-1]}"


while start_datetime_str < end_datatime_str:
  new_url = increment_archive_url(base_url, start_datetime_str)
  urls.append(new_url+end_url)
  start_datetime_str = new_url.split("/")[-2]
  
write_list_to_csv(urls,"wayback_urls.csv")















# from datetime import datetime, timedelta
# import csv
# import sys

# def write_list_to_csv(links, filename):
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         for link in links:
#             writer.writerow([link])

# def increment_archive_url(base_url, start_datetime_str):
#     start_datetime = datetime.strptime(start_datetime_str, "%Y%m%d%H%M%S")
#     new_datetime = start_datetime + timedelta(minutes=60)
#     new_datetime_str = new_datetime.strftime("%Y%m%d%H%M%S")
#     return f"{base_url}{new_datetime_str}/{base_url.split('/')[-1]}"

# def generate_wayback_urls(base_url, start_datetime_str, end_datetime_str):
#     urls = []
#     while start_datetime_str < end_datetime_str:
#         new_url = increment_archive_url(base_url, start_datetime_str)
#         urls.append(new_url+end_url)
#         start_datetime_str = new_url.split("/")[-2]
#     return urls

# if __name__ == "__main__":
#     print ("starting ...")
#     if len(sys.argv) != 3:
#         sys.exit(1)
#     print(sys.argv[1])
#     print(sys.argv[2])
    
#     base_url = "https://web.archive.org/web/"
#     start_datetime_str = sys.argv[1]
#     end_datetime_str = sys.argv[2]
#     end_url="https://www.bobble.ai/en/home"
#     urls = generate_wayback_urls(base_url, start_datetime_str, end_datetime_str)
#     write_list_to_csv(urls, "wayback_urls.csv")


# from datetime import datetime, timedelta
# import csv

# def write_list_to_csv(links, filename):
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         for link in links:
#             writer.writerow([link])

# def increment_archive_url(base_url, start_datetime_str):
#     start_datetime = datetime.strptime(start_datetime_str, "%Y%m%d%H%M%S")
#     new_datetime = start_datetime + timedelta(days=1)
#     new_datetime_str = new_datetime.strftime("%Y%m%d%H%M%S")
#     return f"{base_url}{new_datetime_str}/{base_url.split('/')[-1]}"
# # minutes=60
# def generate_wayback_urls(base_url, start_datetime_str, end_datetime_str):
#     urls = []
#     while start_datetime_str < end_datetime_str:
#         new_url = increment_archive_url(base_url, start_datetime_str)
#         urls.append(new_url+end_url)
#         start_datetime_str = new_url.split("/")[-2]
#     return urls

# if __name__ == "__main__":
#     print ("starting ...")

    
#     yesterday = datetime.now() - timedelta(days=200)
#     today = datetime.now()

#     start_datetime_str = yesterday.strftime("%Y%m%d%H%M%S")
#     end_datetime_str = today.strftime("%Y%m%d%H%M%S")
    

#     base_url = "https://web.archive.org/web/"
#     end_url="https://www.bobble.ai/en/home"
#     urls = generate_wayback_urls(base_url, start_datetime_str, end_datetime_str)
#     write_list_to_csv(urls, "wayback_urls.csv")
