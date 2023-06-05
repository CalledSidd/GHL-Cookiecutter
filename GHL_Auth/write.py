import csv 

def write_to_csv(data):     
    csv_file_path = 'csv/output.csv'
    with open(csv_file_path, 'w', newline='') as file:
        fieldnames = ['contactName', 'email', 'phone']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for entry in data:
            writer.writerow({field: entry.get(field) for field in fieldnames})