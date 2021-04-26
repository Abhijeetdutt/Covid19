import requests
from prettytable import PrettyTable

indore_hospital_codes = [2981, 3005, 3007, 3501, 2460, 2461, 3234, 2991, 990, 3436, 3059, 3233, 2886, 3189, 2999, 70, 3010, 3425, 2462, 2463, 3430, 2464, 3006, 2738, 2997, 3004, 3002, 2465, 3424, 3001, 2689, 3203, 2466, 2703, 323, 3510, 122, 2467, 2468, 3060, 3509, 2995, 3063, 2994, 3439, 2912, 2469, 3431, 3199, 3008, 3420, 3183, 3433, 298, 2470, 2471, 2996, 3293, 2472, 3219, 3354, 3040, 3528, 2984, 2992, 2988, 3432, 3308, 719, 2911, 3503, 3355, 3307, 3426, 2983, 3423, 2475, 299, 3493, 2989, 3438, 2692, 2476, 2477, 3218, 2473, 3000, 3195, 301, 2986, 2478, 3057, 2990, 3187, 2479, 3442, 3039, 2987, 2690, 2993, 2480, 2481]
indore_hospital_status = [[] for i in range(len(indore_hospital_codes))]

counter=0
for i in indore_hospital_codes:
    url = 'http://sarthak.nhmmp.gov.in/covid/facility-bed-occupancy-details/?district_id=17&facility_org_type=2' \
          '&facility=' + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        arr = response.content.decode(encoding='UTF-8', errors='strict').split()
        for index, value in enumerate(arr):
            if '"hospitalname"' in value:
                hospital_name = (arr[index] + " " + arr[index+1]).split('>')[-1]
                print("Checking : {}".format(hospital_name))
                indore_hospital_status[counter].append(hospital_name)
            if 'bed-status"' in value:
                bed_status = ''.join(arr[index-1:index+3]).split('>')[1].split('<')[0]
                total, available = bed_status.split('/')
                indore_hospital_status[counter].append(total)
                indore_hospital_status[counter].append(available)
            if 'tel:' in value and '11123978046' not in value and 'tel:104' not in value:
                contact_number = (arr[index] + " " + arr[index+1]).replace('href="tel:', '').split('>')[0]
                indore_hospital_status[counter].append(contact_number)

    counter += 1

t = PrettyTable(['Hospital Name', 'Total Beds', 'Available Beds', 'Contacts'])
for ihs in indore_hospital_status:
    if ihs[2] != '0':
        t.add_row([ihs[0], ihs[1], ihs[2], ihs[3:]])

print("\n\nStatus : \n\n")

print(t)
