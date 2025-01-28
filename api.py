from app import app , db ,jsonify , request


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    age = data['age']
    # add user to the table
    return jsonify({'message': 'User added successfully'})
