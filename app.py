from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Load the hostel information from the CSV file
hostel_df = pd.read_csv('hostel_info.csv')

allocation = []

@app.route('/allocate', methods=['POST'])
def allocate_rooms():
    global allocation
    # Get the uploaded CSV files
    group_csv = request.files['group_csv']
    hostel_csv = request.files['hostel_csv']

    # Read in the CSV files
    group_df = pd.read_csv(group_csv)
    hostel_df = pd.read_csv(hostel_csv)

    # Allocate rooms using the algorithm
    allocation = []
    for index, row in group_df.iterrows():
        # Find a suitable room for the group
        room = find_suitable_room(row, hostel_df)
        if room:
            allocation.append({
                'groupId': row['Group ID'],
                'hostelName': room['Hostel Name'],
                'roomNumber': room['Room Number'],
                'membersAllocated': row['Members']
            })

    # Return the allocation results
    return jsonify(allocation)

def find_suitable_room(group, hostel_df):
    # Find a room that meets the gender requirement and has enough capacity
    suitable_rooms = hostel_df[(hostel_df['Gender'] == group['Gender']) & (hostel_df['Capacity'] >= group['Members'])]
    if suitable_rooms.empty:
        return None
    else:
        # Allocate the group to the first suitable room
        return suitable_rooms.iloc[0]

@app.route('/download', methods=['GET'])
def download_allocation():
    global allocation
    # Create a CSV file with the allocation details
    allocation_df = pd.DataFrame(allocation)
    csv_file = 'allocation.csv'
    allocation_df.to_csv(csv_file, index=False)
    return send_file(csv_file, as_attachment=True, attachment_filename='allocation.csv')

if __name__ == '__main__':
    app.run(debug=True)
