import pymysql
import json
import random as r

db_user = "root"
db_pass = "123456"
db_name = "eatout"
# Location to socket file used to connect cloudsql
socket_path="/home/xxxx/tutorialcloudsql/democloudsql-xxxxx:mysqldb"


def generate_uuid():
    '''Function generating random unique id of 5 digit'''
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = 5
    for n in range(uuid_format):
        random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
    return random_string

def user_input():
    ''' Function to upload User detail/Feedback data in json '''
    try:
        f_name = input("Enter File name to upload User Detail and Feedback Data      ")
        with open(f_name, 'r') as json_file:
            line = json_file.readline()
            count = 1
            while line:
                input_user = json.loads(line)
                #pno = str(input_user["pno"])
                rows_count = cursor.execute("""SELECT id FROM UserDetails WHERE phonenumber='%s'""" % (input_user["pno"]))
                records = cursor.fetchone()
                for i in records:
                    ud_id = i[0]
                if rows_count: # in case user already exists
                    user_update(input_user) # Calling user_update function to update user detail
                    user_feedback(input_user, ud_id) # Calling user_feedback to insert feedback data
                else: # in case of new user
                    ud_id = generate_uuid()
                    user_details(input_user, ud_id) # Calling user_details function to insert user details
                    user_feedback(input_user, ud_id)  # Calling user_feedback to insert feedback data
                print(str(count) + " Record Successfully Inserted/Updated")
                count += 1
                line = json_file.readline()

    except Exception as e:
        print(e)


def user_update(input_json):
    '''function to update user information incase user already exists'''
    try:

        #pno = str(input_json["pno"])
        #us_name = str(input_json["name"])
        #us_eid = str(input_json["emailid"])
        #us_selfdob = str(input_json["selfdob"])
        #us_spdob = str(input_json["spousedob"])
        #us_ma = str(input_json["anniversary"])

        cursor.execute(
            """update UserDetails set Name = '%s' , Emailid='%s', Birthday='%s', SpouseBirthday='%s', Anniversary='%s' where phonenumber='%s'""" % (
            input_json["name"], input_json["emailid"], input_json["selfdob"], input_json["spousedob"], input_json["anniversary"], input_json["pno"],))

        db_conn.commit()
        print("User Record Updated successfully ")
    except Exception as e:
        print(e)


def user_details(input_json=None, ud_id=None):
    '''function to insert user information incase of new user'''
    try:
        # input_json = input()
        # input_json = json.loads(input_json)
        user_id = ud_id
        #ud_rname = str(input_json["name"])
        #ud_pn = str(input_json["pno"])
        #ud_eid = str(input_json["emailid"])
        #ud_selfdob = str(input_json["selfdob"])
        #ud_spdob = str(input_json["spousedob"])
        #ud_ma = str(input_json["anniversary"])
        cursor.execute("""INSERT into UserDetails VALUES ("%s", "%s", "%s", "%s", "%s","%s","%s")""" % (
        user_id, input_json["name"], input_json["pno"], input_json["emailid"], input_json["selfdob"], input_json["spousedob"], input_json["anniversary"]))
        db_conn.commit()
        print("User Detail Record Insertion Successful")

    except Exception as e:
        print(e)


def user_feedback(input_json=None, us_id=None):
    '''function to insert feedback information'''
    try:
        #fb_dov = str(input_json["dateofvisit"])
        #fb_resid = str(input_json["restid"])
        #fb_fq = str(input_json["foodquality"])
        #fb_sq = str(input_json["servicequality"])
        #fb_amb = str(input_json["ambience"])
        #fb_music = str(input_json["music"])
        #fb_vfm = str(input_json["valueformoney"])
        #fb_clean = str(input_json["cleanliness"])
        #fb_fv = str(input_json["foodvariety"])

        cursor.execute("""INSERT INTO UserFeedback (`UserId`, `VisitDate`, `RestaurantId`, `FoodQuality`,`ServiceQuality`,`Ambience`,`LiveMusic`,`ValueForMoney`,`Cleanliness`,`FoodVariety`) VALUES
         ("%s", "%s", "%s", "%s", "%s","%s","%s","%s","%s","%s")""" % (
        us_id, input_json["dateofvisit"], input_json["restid"], input_json["foodquality"], input_json["servicequality"], input_json["ambience"], input_json["music"], input_json["valueformoney"], input_json["cleanliness"], input_json["foodvariety"])))
        db_conn.commit()

        print("Feedback Record Insertion Successful")

    except Exception as e:
        print(e)


def register_restaurant():
    '''function to upload restaurant data from file in json format''' 
    try:
        f_name=input("Enter File name to upload Restaurant Data      ")
        
        with open(f_name,'r') as json_file:
            line=json_file.readline()
            count=1
            while line:
                input_json1 = json.loads(line)
                print(input_json1)
                uid = generate_uuid() # function called to generate unique id.
                cursor.execute("""INSERT INTO Restaurant VALUES ("%s", "%s", "%s", "%s", "%s")""" % (uid, (input_json1["name"]), (input_json1["cuisine"]), (input_json1["region"]),(input_json1["location"])))
                db_conn.commit()
                print("Record No - "+ str(count)+ "  Insertion Successful for Restaurant name -- " + (input_json1["name"]))
                count += 1
                line=json_file.readline()

def delete_restaurant():
    ''' function to delete restaurant data from database based on restaurantid'''
    try:
        f_name = input("Enter File name to Delete Restaurant Data      ")
        with open(f_name, 'r') as json_file:
            line = json_file.readline()
            while line:
                input_json1 = json.loads(line)
                restid = str(input_json1["id"])
                data = (restid,)
                query = "delete from Restaurant where id= %s"
                rows_count = cursor.execute("""SELECT id FROM Restaurant WHERE id='%s'""" % restid)
                if rows_count > 0:
                    cursor.execute(query, data)
                    db_conn.commit()
                    print(" Restaurant Successfully Deleted")
                else:
                    print("Restaurant doesnt exists")
                line = json_file.readline()
    except Exception as e:
        print(e)


"""QUERIES"""
def query_1():
    ''' Fetch top rated restaurant '''
    try:
        cursor.execute("select r1.name from (select restaurantid, avg(((foodquality+servicequality+ambience+livemusic+valueformoney+cleanliness+foodvariety)*1.0)/7) avgratingacrossall from UserFeedback group by restaurantid order by 1 desc limit 1)tbla, Restaurant r1 where tbla.restaurantid=r1.id")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)

def query_2():
    '''Query to fetch top 2 records on the basis of foodquality or servicequality entered as input'''
    try:
        print("Enter parameter on which restaurants has to be compared  :")
        parameter = input('Please enter either foodquality or servicequality')
        if parameter.lower()== 'foodquality':
            cursor.execute("""select r1.name from (select restaurantid, avg(foodquality) avgratingselected from UserFeedback group by restaurantid order by 1 desc limit 2)tbla, Restaurant r1 where tbla.restaurantid=r1.id;""")
        if parameter.lower()=='servicequality':
            cursor.execute("""select r1.name from (select restaurantid, avg(servicequality) avgratingselected from UserFeedback group by restaurantid order by 1 desc limit 2)tbla, Restaurant r1 where tbla.restaurantid=r1.id;""")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)


def query_3():
    '''Query to fetch list of users with birthday on date entered as input'''
    try:
        print("Enter the date for which the birthday has to be checked :")
        date_input = input()
        cursor.execute("""select Name, PhoneNumber, emailId from UserDetails where month(birthday)=month('%s') and day(birthday) between day('%s') and day('%s')+7"""%(date_input,date_input,date_input))
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)

def query_4():
   '''Query to fetch list of users with any occassion on date entered as input '''
    try:
        print("Enter the date for which occassion has to checked :")
        date_input = input()
        cursor.execute("""select Name, PhoneNumber, emailId from UserDetails where month(birthday)=month('%s') or month(spousebirthday)=month('%s') and month(anniversary)=month('%s')"""%(date_input,date_input,date_input))
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        db_conn = pymysql.connect(unix_socket=socket_path, user=db_user, password=db_pass, db=db_name)
        cursor = db_conn.cursor()
        while True:
            print("Select the operations to perform:")
            print("1. Register Restaurant")
            print("2. Load User Feedback")
            print("3. Fetch the top rated restaurant")
            print("4. Top 2 basis on my input")
            print("5. List users with birthdays in next 7 days from the date specified")
            print("6. List users with any of there occasion in given month")
            print("7. Delete Restaurant")
            print("0. Exit")
            operation = input()
            # print(operation)
            if(operation=='1' or operation == 1):
                print("Selected: Register Restaurant")
                register_restaurant()
            if(operation == '2' or operation == 2):
                print("Selected: Load User Feedback")
                user_input()
            if(operation == '3' or operation== 3):
                print("Selected: Fetch top rated restaurant")
                query_1()
            if (operation == '4' or operation == 4):
                print("Selected: Top 2 on the basis of input")
                query_2()
            if (operation == '5' or operation == 5):
                print("Selected: List users with birthday")
                query_3()
            if (operation == '6' or operation == 6):
                print("Selected: List users with any occassion")
                query_4()
            if (operation == '7' or operation == 7):
                print("Selected: Delete Restaurant")
                delete_restaurant()
            if( operation == '0' or operation == 0):
                print("Thank You")
                cursor.close()
                db_conn.close()
                print (db_conn.ping())
                break

    except Exception as e:
        db_conn.close()
        print(e)
