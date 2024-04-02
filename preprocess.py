import urllib.request
from collections import defaultdict
import urllib.error


def process_data(text):
    text = text.split("\n")
    data = defaultdict(list)
    for link in text:
        try:
            f = urllib.request.urlopen(link.replace(" ", ""))
            content = f.read().decode('utf-8')
            link = link.split("call_log_")[-1].split(".txt")[0].split("_")[0]
            date = f"{link[:4]}-{link[4:6]}-{link[6:]}"
            data[date].append(content)
        except urllib.error.HTTPError as e:
            data = {
                "Error": f"Error fetching data from URL: {link}"
            }
            print("HTTP Error:", e.code, e.reason)
    # print(data)
    return data

