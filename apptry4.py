from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime
from flask import session, redirect

from flask import send_file
from flask import flash


app = Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'  # Set a secret key for session management


# MySQL configurations
db_config = {
    'host': 'localhost',
    'user': 'dedicatedu',
    'password': 'dedicatedp',
    'database': 'db_1',
}


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided username and password match the records in the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and password == user[2]:  # Plain text comparison for demonstration purposes only
            session['user_id'] = user[0]
            if session['user_id'] in [1,2]:
            	return redirect('/index')
            if session['user_id'] in [11,12,13]:
            	return redirect('/advisor')
            if session['user_id'] == 10:
            	return redirect('/diahome')
            if session['user_id'] in [3,4,5,6,7,8,9]:
            	return redirect('/home') 	
        else:
            return 'Invalid username or password'

    return render_template('login.html')


#### advisor home page
@app.route('/advisor', methods=['GET', 'POST'])
def advisor():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    
    if request.method == 'POST':
    	# Get the form data
    	#advisor_id = user_id
    	    	
    	#connection = mysql.connector.connect(**db_config)
    	#cursor = connection.cursor()
    	#query = "SELECT * FROM students WHERE advisor_id = %s AND approved IS NULL ORDER BY id"
    	#params = (user_id,)
    	#cursor.execute(query, params)
    	
    	
    	#if user_id != advisor[0][0]:
    	#    flash('You are not authorized to access this page', 'error')
    	#    cursor.close()
    	#    return redirect('/login')
    	
    	#query = "INSERT INTO progress (student_id, semester, publication, patent, file, approved) VALUES (%s, %s, %s, %s, %s, %s)"
    	#cursor.execute(query, (student_id, sem, pub, pat, fdata, None))
    	#connection.commit()
    	#cursor.close()

    	print('Form received successfully')
    	return 'Got form'
    	
    else:
    	# Query the details table for all submissions
    	connection = mysql.connector.connect(**db_config)
    	cursor = connection.cursor()
    	query = "SELECT id, student_id, semester, publication, patent, flink, advisor_id, approved FROM progress WHERE advisor_id = %s AND approved IS NULL ORDER BY id"
    	params = (user_id,)
    	cursor.execute(query, params)
    	progress_entries = cursor.fetchall()
    	#print(progress_entries.__class__)
    	#entries = []
    	
    	# Convert rows to a list of dictionaries
    	entries = []
    	for row in progress_entries:
            entry = {
                'id': row[0], 
                'student_id': row[1], 
                'semester': row[2], 
                'publication': row[3], 
                'patent': row[4], 
                'flink': row[5], 
                'advisor_id': row[6], 
                'approved': row[7]
            }
            entries.append(entry)
            
    	query = "SELECT id, student_id, semester, publication, patent, flink, advisor_id, approved FROM progress WHERE advisor_id = %s AND approved = 1 ORDER BY id"
    	params = (user_id,)
    	cursor.execute(query, params)
    	progress_entries = cursor.fetchall()
    	#print(progress_entries.__class__)
    	#entries = []
    	
    	# Convert rows to a list of dictionaries
    	entries2 = []
    	for row in progress_entries:
            entry = {
                'id': row[0], 
                'student_id': row[1], 
                'semester': row[2], 
                'publication': row[3], 
                'patent': row[4], 
                'flink': row[5], 
                'advisor_id': row[6], 
                'approved': row[7]
            }
            entries2.append(entry)

    	query = "SELECT id, student_id, semester, publication, patent, flink, advisor_id, approved FROM progress WHERE advisor_id = %s AND approved = 0 ORDER BY id"
    	params = (user_id,)
    	cursor.execute(query, params)
    	progress_entries = cursor.fetchall()
    	#print(progress_entries.__class__)
    	#entries = []
    	
    	# Convert rows to a list of dictionaries
    	entries3 = []
    	for row in progress_entries:
            entry = {
                'id': row[0], 
                'student_id': row[1], 
                'semester': row[2], 
                'publication': row[3], 
                'patent': row[4], 
                'flink': row[5], 
                'advisor_id': row[6], 
                'approved': row[7]
            }
            entries3.append(entry)
            
            
    	cursor.close()
    	return render_template('advisor.html', entries = entries, entries2 = entries2, entries3 = entries3)

# Route for editing a progress entry
@app.route('/undo/<int:entry_id>', methods=['POST'])
def undo_entry(entry_id):
    print(entry_id.__class__)
    if request.method == 'POST':
        # Update the database record with the approved status
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE progress SET approved = NULL, timestamp_advisor = %s WHERE id = %s", (current_timestamp, entry_id))
        connection.commit()
        cursor.close()
        flash(f"Undo successful for entry_id = {entry_id}", 'success')        

    #return f"Declined progress for entry_id {entry_id}"  # Redirect to the table page after the update NOT
    return redirect('/advisor')


# Route for declining a progress entry
@app.route('/decline/<int:entry_id>', methods=['POST'])
def decline_entry(entry_id):
    print(entry_id.__class__)
    if request.method == 'POST':
        # Update the database record with the approved status
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE progress SET approved = 0, timestamp_advisor = %s WHERE id = %s", (current_timestamp, entry_id))
        connection.commit()
        cursor.close()
        flash(f"Entry declined successfully for entry_id = {entry_id}", 'success')        

    #return f"Declined progress for entry_id {entry_id}"  # Redirect to the table page after the update NOT
    return redirect('/advisor')


# Route for approving a progress entry
@app.route('/approve/<int:entry_id>', methods=['POST'])
def approve_entry(entry_id):
    print(entry_id.__class__)
    if request.method == 'POST':
        # Update the database record with the approved status
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE progress SET approved = 1, timestamp_advisor = %s WHERE id = %s", (current_timestamp, entry_id))
        connection.commit()
        cursor.close()
        flash(f"Entry approved successfully for entry_id = {entry_id}", 'success')

    #return f"Approved progress for entry_id {entry_id}"  # Redirect to the table page after the update NOT
    return redirect('/advisor')


### downloading pdf file
@app.route('/download/<int:file_id>', methods=['POST'])
def download_file(file_id):
    try:
    	print(file_id.__class__)
    	connection = mysql.connector.connect(**db_config)
    	cursor = connection.cursor()
    	#########
    	query = "SELECT id, student_id, semester, publication, patent, file, advisor_id, approved FROM progress WHERE id = %s ORDER BY id"
    	params = (file_id,)
    	cursor.execute(query, params)
    	#########
    	result = cursor.fetchone()
    	cursor.close()
    	print(result.__class__)
    	#print(result[2])
    	#print(cursor.fetchone()[2].__class__)
    	#print(cursor.fetchone()[5].__class__)
    	file_data = result[5]
    	sem_num = result[2] 
    	#print(sem_num)
    	#cursor.close()
    	# Set appropriate content headers
    	#headers = {
    	#    'Content-Disposition': 'attachment; filename=test.pdf',
    	#    'Content-Type': 'application/pdf'
    	#}
    	with open(f"report{file_id}.pdf", 'wb') as file:
    	    file.write(file_data)
    	return send_file(f"report{file_id}.pdf", as_attachment=True)
    	#return send_file(filedata, as_attachment=True, download_name = 'test.pdf', mimetype='application/pdf')
    	#return 'yo'
    except Exception as e:
    	return str(e)

#### student home page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    
    if request.method == 'POST':
    	# Get the form data
    	student_id = user_id
    	d = request.form
    	sem = d['semester']    
    	ay = d['ay']
    	semtype = d['semtype']
    	pub = d['publication']
    	pat = d['patent']
    	f = request.files['upload']
    	fname = f.filename
    	fdata = f.read()
    	#flink = "localhost:5000/download/"
    	
    	connection = mysql.connector.connect(**db_config)
    	cursor = connection.cursor()
    	query = "SELECT * FROM students WHERE id = %s"
    	params = (user_id,)
    	cursor.execute(query, params)
    	stud = cursor.fetchall()
    	if user_id != stud[0][0]:  ## stud[0][0] is student_id
    	    flash('You are not authorized to access this page', 'error')
    	    cursor.close()
    	    return redirect('/login')
    	
    	query = "INSERT INTO progress (student_id, semester, ay, semtype, publication, patent, file, advisor_id ,approved) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s)"
    	cursor.execute(query, (student_id, sem, ay, semtype, pub, pat, fdata, stud[0][5], None)) ### stud[0][5] is prof_id
    	connection.commit()
    	cursor.close()
    	#print(d)
    	#f = request.files.get('upload')
    	#f = request.files['upload']
    	#filename = f.filename
    	#filedata = f.read()
    	#print(filename)
    	#with open('downloaded.pdf', 'wb') as file:
    	#    file.write(filedata)
    	print('Form received successfully')
    	return 'Got form'
    	
    else:
    	# Query the details table for all submissions
    	connection = mysql.connector.connect(**db_config)
    	cursor = connection.cursor()
    	query = "SELECT * FROM students WHERE id = %s"
    	#query = "SELECT * FROM details JOIN students ON details.student_id = students.id ORDER BY year, quarter, timestamp"
    	params = (user_id,)
    	cursor.execute(query, params)
    	#cursor.execute(query)
    	stud = cursor.fetchall()
    	#cursor.close()
    	#print(stud.__class__)
    	#print(len(stud))
    	#print(stud[0])
    	#print(stud[0].__class__)

    	if user_id != stud[0][0]:
            flash('You are not authorized to access this page', 'error')
            cursor.close()
            return redirect('/login')
        
    	cursor.close()
    	return render_template('home.html', student_name=stud[0][1])


# Route to display and handle fees details request. Lets call it index
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect('/login')
        
    user_id = session['user_id']
    session_id = session['user_id']
    #print(user_id.__class__)
         
    if request.method == 'POST':
        # Get the form data
        submissions = []
        d = request.form
        print(d)
        print('test1')
        ids = []
        for key in d:
            if '_' in list(key):
                ids.append(key.split('_')[0])
            elif key == 'year':
                year = d[key]
                #print(year)
            elif key == 'quarter':
                quarter = d[key]
                #print(quarter)
            elif key == 'excessfund':
                ef = float(d[key])
                #print(ef)
            elif key == 'totalfundreceived':
                tfr = float(d[key])
                #print(tfr)
            elif key == 'balancefund':
                bf = float(d[key])
                #print(bf)
            elif key == 'additionalcomments':
                ac = d[key]
                #print(ac)

        idset = set(ids)
        for i in idset:
            for key, value in d.items():
                if key.split('_')[0] == i and key.split('_')[1]== 'age':
                    age = value
                if key.split('_')[0] == i and key.split('_')[1]== 'weight':
                    weight = value
                if key.split('_')[0] == i and key.split('_')[1]== 'height':
                    height = value
                if key.split('_')[0] == i and key.split('_')[1]== 'arg':
                    arg = value
                if key.split('_')[0] == i and key.split('_')[1]== 'brg':
                    brg = value                                        
            submission = {
            		'student_id': int(i),
            		'age': float(age),
            		'weight': float(weight),
            		'height': float(height),
            		'year': int(year),
            		'quarter': int(quarter),
            		'arg': float(arg),
            		'brg': float(brg),
            		'ef': ef,
            		'tfr': tfr,
            		'bf': bf,
            		'ac': ac
            		}
            submissions.append(submission)
            print('test2')
            
        print('test3')

        try:
            # Connect to the database
            print('Connecting to the database...')
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Insert the submissions into the 'details' table
            for submission in submissions:
                query = '''
                INSERT INTO details (student_id, m1, m2, m3, year, quarter, annual_research_grant, balance_research_grant, excess_fund, total_fund_received, balance_fund, additional_comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                values = (
                    submission['student_id'],
                    submission['age'],
                    submission['weight'],
                    submission['height'],
                    submission['year'],
                    submission['quarter'],
                    submission['arg'],
                    submission['brg'],
                    submission['ef'],
                    submission['tfr'],
                    submission['bf'],
                    submission['ac']
                )
                cursor.execute(query, values)
                #print(year, quarter)
                print(ef, tfr, bf, ac)

            connection.commit()
            #cursor.close()
            #connection.close()

            print('Data stored successfully')
            return 'Data stored successfully'
        except Exception as e:
            print('Error storing data: {}'.format(str(e)))
            return 'Error storing data: {}'.format(str(e))

    else:
        try:
            # Connect to the database
            print('Connecting to the database...')
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            print(user_id.__class__)

            # Fetch student information from the 'students' table
            query = 'SELECT * FROM students WHERE institute_id = %s'
            params = (user_id,)
            cursor.execute(query, params)

            rows = cursor.fetchall()

            # Convert rows to a list of dictionaries
            students = []
            for row in rows:
                student = {
                    'id': row[0],
                    'name': row[1],
                    'institute_id': row[4],
                    'major': row[3]
                }
                students.append(student)

            #cursor.close()
            #connection.close()

            print('Retrieved data successfully')
            return render_template('index.html', students=students)
        except Exception as e:
            print('Error retrieving data: {}'.format(str(e)))
            return 'Error retrieving data: {}'.format(str(e))


@app.route('/diahome')
def diahome():
    return render_template('diahome.html')

@app.route('/acadprogress')
def acadprogress():
    return 'WIP'



#### it will be details table not submissions
@app.route('/submissions')
def submissions():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    if user_id != 10:
        flash('You are not authorized to access this page', 'error')
        return redirect('/login')

    # Query the details table for all submissions
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    #query = "SELECT * FROM details"
    query = "SELECT * FROM details JOIN students ON details.student_id = students.id ORDER BY year, quarter, timestamp"
    cursor.execute(query)
    subm = cursor.fetchall()
    cursor.close()

    return render_template('submissions.html', submissions=subm)


    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)

