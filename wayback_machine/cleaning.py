import re
import csv

def fix_broken_links(links):
    fixed_links = set()
    for link in links:
        cleaned_link = re.sub(r"[^\w/:@?\.~#&=+$%]", "", link)  

        # Check if link already has the full format (https://web.archive.org/...)
        if "web.archive.org" in cleaned_link:
            fixed_links.add(cleaned_link)
        else:
            if cleaned_link.startswith("/web/"):
                fixed_links.add(f"https://web.archive.org{cleaned_link}")
            else:
                pass

    # Remove comments and "expand/close" instructions
    filtered_links = [link for link in fixed_links if not link.startswith("#")]
    return list(filtered_links)

def read_csv_to_list(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        final_list = sum(list(csv_reader), [])
    return final_list

def write_list_to_csv(links, filename):
    with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

links = read_csv_to_list('crawled_links.csv')

cleaned_links = fix_broken_links(links)


write_list_to_csv(cleaned_links, 'cleaned_links.csv')
