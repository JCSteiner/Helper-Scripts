# import dependencies
import bs4
from selenium import webdriver
import time

# opens a "netstat.txt" in a local directory
infile = open('./netstat.txt')

# prints to the user what it is doing
print("Reading netstat output and searching for active connections...", end="\n\n")

# loops through every line of the netstat output
for line in infile:

    # splits the line to get the destination ip address
    dst = line.split()[2]

    # if the destination ip address is a netstat formatted ip (ip:port)
    if "." in dst and ":" in dst:

        # print that the target system had a connection on a given port
        print("\033[96m {}\033[00m".format("Target system was found to have a connection to:"), dst)

        # creates a URL and sends a request to the blacklist checker from what appears to be a chrome browser
        url = 'https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a' + dst.split(':')[0] + '&run=toolpage'
        dr = webdriver.Chrome()
        dr.get(url)
        soup = bs4.BeautifulSoup(dr.page_source,"lxml")
        
        # finds the status columns
        s1 = soup.find_all('td', class_='table-column-Status')

        # creates a counter for things being not on the bad list, being on the bad list, and query timeouts to the site
        ctr_good = 0
        ctr_bad = 0
        ctr_timeout = 0
        ctr_total = 0

        # loops through every result found in the web-scraped output
        # converted all output to lowercase to have a little resiliency in the script
        for rep in s1:
            
            # if it is found to be on the good list
            if "ok" in str(rep).lower():
                # increment good by 1
                ctr_good += 1
            elif "listed" in str(rep).lower():
                # increment bad by 1
                ctr_bad += 1
            elif "timeout" in str(rep).lower():
                # increment timeout by 1
                ctr_timeout += 1

            # total should be the sum of all others, if it is not, an error likely occurred with the script
            ctr_total += 1
            
        # prints web scraping to user
        if ctr_bad > 0:
            print("\033[91m {}\033[00m".format("Reputation checks complete. Timeouts to query the list are treated the same as blocks. False positives may occur."), end="\n\n")
            print("\033[91m {}\033[00m".format("Total number of good lists:"), ctr_good)
            print("\033[91m {}\033[00m".format("Ttoal number of bad lists:"), ctr_bad)
            print("\033[91m {}\033[00m".format("Total number of query timeouts:"), ctr_timeout)
            print("\033[91m {}\033[00m".format("Total number of queries (should be the sum of good, bad, and timeout):"), ctr_total, end="\n\n")
        else:
            print("\033[92m {}\033[00m".format("Reputation checks complete. Timeouts to query the list are treated the same as blocks. False positives may occur."), end="\n\n")
            print("\033[92m {}\033[00m".format("Total number of good lists:"), ctr_good)
            print("\033[92m {}\033[00m".format("Ttoal number of bad lists:"), ctr_bad)
            print("\033[92m {}\033[00m".format("Total number of query timeouts:"), ctr_timeout)
            print("\033[92m {}\033[00m".format("Total number of queries (should be the sum of good, bad, and timeout):"), ctr_total, end="\n\n")

        # sleeps to avoid messing up the web interface
        time.sleep(1)
