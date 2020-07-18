#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error

class Db():
    # Constructor...
    def __init__(self):
        
        database = "develop_covid_19_unit_db.db"
        try:
            self.conn = sqlite3.connect(database)
            print(sqlite3.version)
            
        except Error as e:
            print(e)
   
    def close_db(self):
               
        if self.conn is not None:
            
            self.conn.close()
   
    def insert_data(self, query):
        """
        Create a new Table        
        :param :
        :return: id
        """
       
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(query)
            user_id=cur.lastrowid
            self.conn.commit()
            
        else:
            print("insert faild")
            return 0

        return user_id

    def update_data(self, query):
        """

        : Update Table:
        :return:  id
        """
        # cur.execute('UPDATE employees SET name = "Rogers" where id = 2')

        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
            return 1
        else:
            print("Update faild")
            return 0
    
    def get_data_by_key(self, query):
        
        """       
        :param priority:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        if len(rows)>0:
            pass
            return rows[0]
        else:
            return None

    def get_data(self, query):
        
        """        
        :param query:
        :return: table data
        """
        cur = self.conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        

        return rows

#Insert tblDistrict.....

    def insert_district(self, district):
        """
        Create a new personInfo        
        :param personInfo:
        :return:
        """
        try:                              
                                                                               
            sql = ''' INSERT INTO tblDistrict(district,status)
                      VALUES(?,?) '''
            if self.conn is not None:
                cur = self.conn.cursor()
                cur.execute(sql, district)
                district_id=cur.lastrowid
                self.conn.commit()
                
            else:
                print("insert faild")
                return 0,""

            return district_id
            
        except:
            pass

    def get_all_district(self):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblDistrict where status = 1")
        
        districts = cur.fetchall()
        # print(rows)


        return districts

    def get_district_id_by_name(self,district):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblDistrict where status = 1 AND district = ? ",(district,))
        
        districts = cur.fetchall()
        if len(districts)>0:
            return districts[0][0]
        else:
            return 0
        

    def get_district_id(self,district_id):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblDistrict where status = 1 AND district_id = ? ",(district_id,))
        
        districts = cur.fetchall()
        # print(rows)


        return districts

    def get_district_details(self):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblDistrict where status = 1")
        
        districts = cur.fetchall()
        districtlst=[]
        for district in districts:
            thanas=self.get_thanas_by_district_id(district[0])
            new_district=(district,thanas)
            districtlst.append(new_district)
        # print(rows)


        return districtlst



    def update_district(self, district):
        """

        :param personInfo:
        :return:  id
        """
        
        sql = ''' UPDATE tblDistrict
                  SET district = ? ,
                      status = ?
                  WHERE district_id = ?'''
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql, district)
            self.conn.commit()
            
        else:
            print("Update faild")

#Insert tblThana.....

    def check_thana(self,district_id,thana):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblThana where status = 1 AND district_id = ?  AND thana = ? ",(district_id,thana,))
        
        thanas = cur.fetchall()
        if len(thanas)>0:
            return thanas[0][0]
        else:
            return 0;

    def insert_thana(self, thana):
        """
        Create a new personInfo        
        :param personInfo:
        :return:
        """
        try:
            district=(thana[0],1)
            district_id =self.get_district_id_by_name(thana[0])
            if district_id == 0:
                district_id =self.insert_district(district)

            thana_id =self.check_thana(district_id,thana[1])

            if thana_id == 0:
                thana_query=(district_id,thana[1],0,0,0,1)

                sql = ''' INSERT INTO tblThana(district_id,thana,longitude,latitude,covid19_medical_center,status)
                          VALUES(?,?,?,?,?,?) '''
                if self.conn is not None:
                    cur = self.conn.cursor()
                    cur.execute(sql, thana_query)
                    thana_id=cur.lastrowid
                    self.conn.commit()
                    
                else:
                    print("insert faild")
                    return 0,""

            return thana_id
            
        except:
            pass

    def get_all_thana(self):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblThana where status = 1")
        
        thanas = cur.fetchall()
        # print(rows)


        return thanas

    def get_thanas_by_district_id(self,district_id):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        try:
            if len(district_id)>2:
                district_id = self.get_district_id_by_name(district_id)
        except Exception as e:
            pass        
        
        cur.execute("SELECT * FROM tblThana where status = 1 AND district_id = ? ",(district_id,))
        
        thanas = cur.fetchall()
        # print(rows)


        return thanas

    def get_thana_id(self,thana_id):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblThana where status = 1 AND thana_id = ? ",(thana_id,))
        
        thanas = cur.fetchall()
        # print(rows)


        return thanas


    def update_thana(self, thana):
        """

        :param personInfo:
        :return:  id
        """

        sql = ''' UPDATE tblThana
                  SET district_id = ?,
                      thana = ?,
                      longitude = ?,
                      latitude = ?,
                      covid19_medical_center = ?,
                      status = ?
                  WHERE thana_id = ?'''
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql, thana)
            self.conn.commit()
            
        else:
            print("Update faild")


    def update_thana_lon_lat(self, thana):
        """

        :param personInfo:
        :return:  id
        """

        sql = ''' UPDATE tblThana
                  SET longitude = ?,
                      latitude = ?,
                      covid19_medical_center = ?,
                      status = ?
                  WHERE thana_id = ?'''
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql, thana)
            self.conn.commit()
            
        else:
            print("Update faild")


    def update_thana_covid19_medical_center(self, thana):
        """

        :param personInfo:
        :return:  id
        """

        sql = ''' UPDATE tblThana
                  SET covid19_medical_center = ?,
                      status = ?
                  WHERE thana_id = ?'''
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql, thana)
            self.conn.commit()
            
        else:
            print("Update faild")

# Create Table
    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)   
    
        
    # Create Database.......
    def createDb(self):

        hospital_table = """ CREATE TABLE IF NOT EXISTS tblHospital (
                                            hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL unique,
                                            hospital_name text NOT NULL,
                                            hospital_pic text,
                                            district  text NOT NULL,
                                            town text NOT NULL,
                                            proposal text NOT NULL,
                                            proposal_video_link text,
                                            facebook_group text,
                                            development_start_date REAL,
                                            development_end_date REAL,
                                            accept_date REAL,
                                            accept_proposal bool,
                                            stop bool,
                                            completed bool,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        user_table = """ CREATE TABLE IF NOT EXISTS tblUser (
                                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            key text NOT NULL,
                                            ciphered_text text NOT NULL,
                                            auth_id text NOT NULL unique,
                                            phone_number text NOT NULL unique,
                                            phone_number_verified bool NOT NULL,
                                            name text NOT NULL,
                                            gender text NOT NULL,
                                            nid text,
                                            profile_pic text,
                                            district  text,
                                            town text,
                                            village text,
                                            create_date REAL,
                                            collection integer NOT NULL,
                                            collection_number integer NOT NULL,
                                            donated integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        admin_table = """ CREATE TABLE IF NOT EXISTS tblAdmin  (
                                            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL unique,
                                            admin_type  text NOT NULL,
                                            access_all bool NOT NULL,
                                            create_date REAL,
                                            security_key  text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        volunteer_table = """ CREATE TABLE IF NOT EXISTS tblVolunteer  (
                                            volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL unique,
                                            hospital_id integer NOT NULL,
                                            email_id  text NOT NULL,
                                            village  text NOT NULL,
                                            profession  text NOT NULL,
                                            verified bool NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        meeting_table = """ CREATE TABLE IF NOT EXISTS tblMeeting  (
                                            meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            hospital_id integer NOT NULL,
                                            about_meeting  text NOT NULL,
                                            meeting_link  text NOT NULL,
                                            meeting_done bool NOT NULL,
                                            meeting_time REAL,
                                            status bool NOT NULL
                                        ); """

        meeting_attendance_table = """ CREATE TABLE IF NOT EXISTS tblMeetingAttendance  (
                                            meeting_attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            meeting_id integer NOT NULL,
                                            volunteer_id  integer NOT NULL,
                                            attend bool NOT NULL,
                                            status bool NOT NULL
                                        ); """

        video_message_table = """ CREATE TABLE IF NOT EXISTS tblVideoMessage  (
                                            video_message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            hospital_id integer NOT NULL,
                                            about_video  text NOT NULL,
                                            video_link  text NOT NULL,
                                            post_time REAL,
                                            status bool NOT NULL
                                        ); """

        collection_table = """ CREATE TABLE IF NOT EXISTS tblCollection  (
                                            collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL,
                                            hospital_id integer NOT NULL,
                                            name  text NOT NULL,
                                            phone_number  text NOT NULL,                                            
                                            photo  text NOT NULL,
                                            amount integer NOT NULL,
                                            collection_date REAL,
                                            status bool NOT NULL
                                        ); """

        donated_table = """ CREATE TABLE IF NOT EXISTS tblDonated  (
                                            donated_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL,
                                            hospital_id integer NOT NULL,
                                            account_name  text NOT NULL,
                                            to_account_number  text NOT NULL,  
                                            from_account_number  text NOT NULL,                                          
                                            delever_msg  text NOT NULL,
                                            amount integer NOT NULL,
                                            create_date REAL,
                                            received bool NOT NULL,
                                            status bool NOT NULL
                                        ); """

        received_money_table = """ CREATE TABLE IF NOT EXISTS tblReceivedMoney  (
                                            received_money_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            account_name  text NOT NULL,
                                            to_account_number  text NOT NULL,  
                                            from_account_number  text NOT NULL,                                          
                                            delever_msg  text NOT NULL,
                                            amount integer NOT NULL,
                                            received_date REAL,
                                            status bool NOT NULL
                                        ); """

        developer_table = """ CREATE TABLE IF NOT EXISTS tblDeveloper  (
                                            developer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL,
                                            hospital_id integer NOT NULL,
                                            work_start_date REAL,
                                            work_end_date REAL,                                         
                                            work_fedback  text NOT NULL,
                                            working bool NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        costing_table = """ CREATE TABLE IF NOT EXISTS tblCosting  (
                                            costing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            developer_id integer NOT NULL,
                                            hospital_id integer NOT NULL,
                                            item_name  text NOT NULL,
                                            item_count  integer NOT NULL,
                                            unit  text NOT NULL,
                                            cost integer NOT NULL,
                                            verified bool NOT NULL,
                                            paid bool NOT NULL,
                                            item_pic  text NOT NULL,
                                            paid_date REAL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        total_summary_table = """ CREATE TABLE IF NOT EXISTS tblTotalSummary   (
                                            total_summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            hospital_id integer NOT NULL,
                                            number_of_collection integer NOT NULL,
                                            collection integer NOT NULL,
                                            donated integer NOT NULL,
                                            costing integer NOT NULL,
                                            updated_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        notification_table = """ CREATE TABLE IF NOT EXISTS tblNotification   (
                                            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id integer NOT NULL,
                                            subject  text NOT NULL,
                                            notification  text NOT NULL,
                                            create_date REAL NOT NULL,
                                            read bool NOT NULL,
                                            status bool NOT NULL
                                        ); """
                                         
        
        # tblDistrict..........
        district_table = """ CREATE TABLE IF NOT EXISTS tblDistrict (
                                            district_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            district text NOT NULL UNIQUE,
                                            status bool NOT NULL
                                        ); """
        
        # tblThana..........
        thana_table = """ CREATE TABLE IF NOT EXISTS tblThana (
                                            thana_id INTEGER PRIMARY KEY AUTOINCREMENT,                                            
                                            district_id integer NOT NULL,
                                            thana text NOT NULL,                                            
                                            longitude float NOT NULL,                                            
                                            latitude float NOT NULL,
                                            covid19_medical_center bool NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        # tblThana..........
        village_table = """ CREATE TABLE IF NOT EXISTS tblVillage (
                                            village_id INTEGER PRIMARY KEY AUTOINCREMENT,                                            
                                            thana_id integer NOT NULL,
                                            village text NOT NULL,                                            
                                            longitude float NOT NULL,                                            
                                            latitude float NOT NULL,
                                            status bool NOT NULL
                                        ); """



        if self.conn is not None:        
            # create person info table
            self.create_table(district_table)
            self.create_table(thana_table)
            self.create_table(village_table)
            self.create_table(user_table)
            self.create_table(admin_table)                  
            self.create_table(hospital_table)
            self.create_table(volunteer_table)
            self.create_table(collection_table)
            self.create_table(donated_table)
            self.create_table(received_money_table)
            self.create_table(developer_table)
            self.create_table(costing_table)
            self.create_table(notification_table)
            self.create_table(total_summary_table)
            self.create_table(meeting_table)
            self.create_table(meeting_attendance_table)
            self.create_table(video_message_table)

    

        else:
            print("Error! cannot create the database connection.")

    