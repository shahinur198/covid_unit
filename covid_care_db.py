#!/usr/bin/python
 
import psycopg2

class Db():
    # Constructor...
    def __init__(self):

        database = "dailycaredb"
        try:
            self.conn = psycopg2.connect(database = "dailycaredb", user = "postgres", password = "test123", host = "127.0.0.1", port = "5432")
            # self.conn = psycopg2.connect(database = "dailycaredb", user = "postgres", password = "T198rainer", host = "34.70.222.159", port = "5432")

            # print(sqlite3.version)
            
        except Exception as e:
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
            user_id = cur.fetchone()[0]
            self.conn.commit()
            
        else:
            print("insert faild")
            return 0

        return user_id
   
    def multi_queries(self, querys):
        """
        Create a new Table        
        :param :
        :return: id
        """
       
        if self.conn is not None:
            cur = self.conn.cursor()

            for query in querys:                
                cur.execute(query)

            self.conn.commit()
            
        else:
            print("insert faild")
            return 0

        return 1

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
                                                                               
            sql = " INSERT INTO tblDistrict(district,status) VALUES('"+district[0]+"','1') RETURNING district_id "
            if self.conn is not None:
                cur = self.conn.cursor()
                cur.execute(sql)
                district_id = cur.fetchone()[0]
                # district_id= cur.fetchone()[0]
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
        cur.execute("SELECT * FROM tblDistrict where status = '1'")
        
        districts = cur.fetchall()
        # print(rows)


        return districts

    def get_district_id_by_name(self,district):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblDistrict where district = '"+district+"' ")
        
        districts = cur.fetchall()
        # print(districts)
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
        cur.execute("SELECT * FROM tblDistrict where status = '1' AND district_id = '"+district_id+"' ")
        
        districts = cur.fetchall()
        # print(rows)


        return districts

    def get_district_details(self):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblDistrict where status = '1'")
        
        districts = cur.fetchall()
        districtlst=[]
        for district in districts:
            thanas=self.get_thanas_by_district_id(str(district[0]))
            new_district=(district,thanas)
            districtlst.append(new_district)
        # print(rows)


        return districtlst



    def update_district(self, district):
        """

        :param personInfo:
        :return:  id
        """
        
        sql = " UPDATE tblDistrict SET district = '"+district[0]+"' , status = '"+district[1]+"' WHERE district_id = '"+district[2]+"'"
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            
        else:
            print("Update faild")

#Insert tblThana.....

    def check_thana(self,district_id,thana):
        
        """        
        :param labelling:
        :return:
        """
        sq="SELECT * FROM tblThana where status = '1' AND district_id = '"+district_id+"'  AND thana = '"+thana+"' "
        # print(sq)
        cur = self.conn.cursor()
        cur.execute(sq)
        
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
        # try:
        district=(thana[0],1)
        district_id =self.get_district_id_by_name(thana[0])
        print("district_id",district_id)
        if district_id == 0:
            district_id =self.insert_district(district)
        print("district_id",district_id)

        thana_id =self.check_thana(str(district_id),thana[1])

        if thana_id == 0:
            # thana_query=(district_id,thana[1],0,0,1)

            sql = " INSERT INTO tblThana(district_id,thana,longitude,latitude,status) VALUES("
            sql = sql + "'"+str(district_id)+"','"+thana[1]+"','0','0','1') RETURNING thana_id"
            if self.conn is not None:
                cur = self.conn.cursor()
                cur.execute(sql)
                thana_id= cur.fetchone()[0]
                self.conn.commit()
                
            else:
                print("insert faild")
                return 0,""

            return thana_id
            
        # except:
        #     pass

    def get_all_thana(self):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblThana where status = '1'")
        
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
                # print(district_id)
                district_id = self.get_district_id_by_name(district_id)
                # print(district_id)
        except Exception as e:
            pass        
        
        cur.execute("SELECT * FROM tblThana where status = '1' AND district_id = '"+str(district_id)+"' ")
        
        thanas = cur.fetchall()
        # print(rows)


        return thanas

    def get_thana_id(self,thana_id):
        
        """        
        :param labelling:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tblThana where status = '1' AND thana_id = '"+thana_id+"' ")
        
        thanas = cur.fetchall()
        # print(rows)


        return thanas


    def update_thana(self, thana):
        """

        :param personInfo:
        :return:  id
        """

        sql = " UPDATE tblThana SET district_id = '"+thana[0]+"', thana = '"+thana[1]+"', longitude = '"+thana[1]+"',"
        sql = sql + " latitude = '"+thana[3]+"', status = '"+thana[4]+"' WHERE thana_id = '"+thana[5]+"'"
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            
        else:
            print("Update faild")


    def update_thana_lon_lat(self, thana):
        """

        :param personInfo:
        :return:  id
        """

        sql = " UPDATE tblThana SET longitude = '"+thana[0]+"', latitude = '"+thana[1]+"', status = '"+thana[2]+"' "
        sql = sql+ "  WHERE thana_id = '"+thana[3]+"' "
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(sql)
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
        # print()
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except Exception as e:
            print(e)   
    
    # Drop Table
    def drop_table(self, table_name):
        """ Drop Table
        """
        # print("create_table")
        try:
            c = self.conn.cursor()
            query="DROP TABLE IF EXISTS "+table_name+";"
            c.execute(query)
            self.conn.commit()

        except Exception as err:
            print(err)     
    
        
    # Create Database.......
    def createDb(self):
        
        user_table = """ CREATE TABLE IF NOT EXISTS tblUser (
                                            user_id serial PRIMARY KEY,
                                            key text NOT NULL,
                                            ciphered_text text NOT NULL,
                                            client_token text NOT NULL,
                                            phone_number text NOT NULL unique,
                                            phone_number_verified bool NOT NULL,
                                            name text NOT NULL,
                                            gender text NOT NULL,
                                            profile_pic text,
                                            district_id  integer,
                                            thana_id integer,
                                            village_id integer,                                        
                                            home_longitude REAL NOT NULL,                                            
                                            home_latitude REAL NOT NULL,                                      
                                            client_device bool NOT NULL,                                          
                                            fbuid text NOT NULL unique,
                                            create_date REAL, 
                                            status bool NOT NULL
                                        ); """

        admin_table = """ CREATE TABLE IF NOT EXISTS tblAdmin  (
                                            admin_id serial PRIMARY KEY,
                                            user_id integer NOT NULL unique,
                                            admin_type  text NOT NULL,
                                            access integer NOT NULL,
                                            create_date REAL,
                                            security_key  text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        user_bank_account_table = """ CREATE TABLE IF NOT EXISTS tblUserBankAccount  (
                                            user_bank_account_id serial PRIMARY KEY,
                                            user_id integer NOT NULL unique,
                                            bank_name  text NOT NULL, 
                                            bank_account_info text NOT NULL,
                                            bank_account text NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        account_balance_table = """ CREATE TABLE IF NOT EXISTS tblAccountBalance  (
                                            account_balance_id serial PRIMARY KEY,                                            
                                            user_id integer NOT NULL unique,
                                            received  REAL NOT NULL,
                                            pay  REAL NOT NULL,
                                            update_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        payment_request_table = """ CREATE TABLE IF NOT EXISTS tblPaymentRequest  (
                                            payment_request_id serial PRIMARY KEY,                                            
                                            user_id integer NOT NULL,
                                            transaction_id  text NOT NULL unique,
                                            transaction_url  text NOT NULL,
                                            create_date REAL NOT NULL,
                                            done bool NOT NULL,
                                            status bool NOT NULL
                                        ); """

        received_money_table = """ CREATE TABLE IF NOT EXISTS tblReceivedMoney  (
                                            received_money_id serial PRIMARY KEY,                                            
                                            user_id integer NOT NULL,
                                            transaction_id  text NOT NULL unique,
                                            paymentID  text NOT NULL,
                                            createTime  REAL NOT NULL,
                                            updateTime  REAL NOT NULL,
                                            trxID  text NOT NULL,
                                            transactionStatus  text NOT NULL,
                                            amount  REAL NOT NULL,
                                            currency  text NOT NULL,
                                            intent  text NOT NULL,
                                            merchantInvoiceNumber  text NOT NULL,
                                            payment_medium  text NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        pay_doctor_fee_table = """ CREATE TABLE IF NOT EXISTS tblPayDoctorFee  (
                                            pay_doctor_fee_id serial PRIMARY KEY,                                            
                                            user_id integer NOT NULL,                                            
                                            doctor_appointment_id integer NOT NULL,
                                            daily_care_charge  REAL NOT NULL,    
                                            vat_tax  REAL NOT NULL,
                                            pay_date REAL NOT NULL,
                                            status bool NOT NULL,
                                            UNIQUE(doctor_appointment_id)
                                        ); """    

        withdrawal_request_table = """ CREATE TABLE IF NOT EXISTS tblWithdrawalRequest  (
                                            withdrawal_request_id serial PRIMARY KEY,                                            
                                            user_id integer NOT NULL,
                                            withdrawal_amount  REAL NOT NULL,
                                            request_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        withdrawal_money_table = """ CREATE TABLE IF NOT EXISTS tblWithdrawalMoney  (
                                            withdrawal_money_id serial PRIMARY KEY,                                            
                                            withdrawal_request_id integer NOT NULL,                                            
                                            user_id integer NOT NULL,
                                            withdrawal_amount  REAL NOT NULL,
                                            processing_fee  REAL NOT NULL, 
                                            withdrawal_detail  text NOT NULL,                                             
                                            bank_transaction_id text NOT NULL, 
                                            withdrawal_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # doctor_type = 0(outside doctor), 1(Examine Doctor), 2(Duty doctor), 3(Daily Care Doctor)

        doctor_table = """ CREATE TABLE IF NOT EXISTS tblDoctor  (
                                            doctor_id serial PRIMARY KEY,
                                            name  text NOT NULL,
                                            bmdc  text NOT NULL,
                                            degree  text NOT NULL,
                                            specialist  text NOT NULL,
                                            doctor_designation  text,
                                            doctor_workplace  text,
                                            fee_first_time integer NOT NULL,
                                            fee_next_time integer NOT NULL,
                                            doctor_pic text,
                                            doctor_type integer NOT NULL, 
                                            practicing_year REAL NOT NULL, 
                                            about_doctor  text,
                                            create_date REAL,
                                            status bool NOT NULL,
                                            posting_district_id  integer,
                                            posting_thana_id integer
                                        ); """

        doctor_joining_table = """ CREATE TABLE IF NOT EXISTS tblDoctorJoining  (
                                            doctor_joining_id serial PRIMARY KEY,
                                            user_id integer NOT NULL UNIQUE,
                                            doctor_id integer NOT NULL UNIQUE,
                                            joining_date REAL,  
                                            status bool NOT NULL
                                        ); """

        doctor_query_table = """ CREATE TABLE IF NOT EXISTS tblDoctorQuery  (
                                            doctor_query_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            query_msg  text NOT NULL,
                                            create_date REAL,  
                                            status bool NOT NULL
                                        ); """

        # visiting = 0-stop visiting/ 1- offline / 2-online/3-online-offline-both
        visiting_place_table = """ CREATE TABLE IF NOT EXISTS tblVisitingPlace  (
                                            visiting_place_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            district text NOT NULL,
                                            town text NOT NULL,
                                            place text NOT NULL,
                                            schedule text NOT NULL,
                                            one_day_max_patient integer, 
                                            contract_number text, 
                                            visiting integer NOT NULL,     
                                            daily_care_chamber bool NOT NULL,     
                                            status bool NOT NULL
                                        ); """

        doctor_visiting_session_table = """ CREATE TABLE IF NOT EXISTS tblDoctorVisitingSession  (
                                            doctor_visiting_session_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,                         
                                            start_time REAL NOT NULL,                                            
                                            end_time REAL NOT NULL, 
                                            visiting_place_id integer NOT NULL,   
                                            next_time REAL,
                                            next_place integer,
                                            status bool NOT NULL
                                        ); """


        patient_table = """ CREATE TABLE IF NOT EXISTS tblPatient  (
                                            patient_id serial PRIMARY KEY,
                                            phone_number text NOT NULL,
                                            patient_name text NOT NULL,
                                            age  REAL NOT NULL,
                                            gender text NOT NULL,
                                            hight REAL,
                                            weight REAL, 
                                            blood_group text,                                         
                                            profile_pic text,
                                            district_id integer,
                                            town_id integer,
                                            village_id integer, 
                                            mahalla_id integer,
                                            daily_care_center_id integer NOT NULL,                                             
                                            nid text,   
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        doctor_message_table = """ CREATE TABLE IF NOT EXISTS tblDoctorMessage  (
                                            doctor_message_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            patient_id  integer NOT NULL,
                                            message  text NOT NULL,
                                            view bool NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        patient_connection_table = """ CREATE TABLE IF NOT EXISTS tblPatientConnection  (
                                            patient_connection_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            patient_id integer NOT NULL,
                                            family_id integer NOT NULL,
                                            guardian bool NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        primary_test_table = """ CREATE TABLE IF NOT EXISTS tblPrimaryTest (
                                            primary_test_id serial PRIMARY KEY,
                                            primary_test text NOT NULL,
                                            unit text NOT NULL,
                                            lower_range REAL NOT NULL,
                                            uper_rage REAL NOT NULL,
                                            standard REAL NOT NULL,
                                            about_test text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        patient_dptr_table = """ CREATE TABLE IF NOT EXISTS tblPatientDPTR  (
                                            patient_dptr_id serial PRIMARY KEY,
                                            patient_id integer NOT NULL,
                                            primary_test_id integer NOT NULL,
                                            test_value REAL NOT NULL,
                                            report integer NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        patient_covid_test_table = """ CREATE TABLE IF NOT EXISTS tblPatientCovidTest  (
                                            patient_covid_test_id serial PRIMARY KEY,
                                            patient_id integer NOT NULL,
                                            covid_positive_date REAL,
                                            covid_negative_date REAL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_symptom_group_save_table = """ CREATE TABLE IF NOT EXISTS tblPatientSymptomGroupSave  (
                                            patient_symptom_group_save_id serial PRIMARY KEY,
                                            patient_id  integer NOT NULL,
                                            patient_appointment_id integer NOT NULL,
                                            create_date REAL NOT NULL
                                        ); """

        patient_test_report_table = """ CREATE TABLE IF NOT EXISTS tblPatientTestReport  (
                                            patient_test_report_id serial PRIMARY KEY,
                                            medical_test_rx_id integer NOT NULL, 
                                            patient_treatment_id integer NOT NULL,                                           
                                            report_urls text NOT NULL,
                                            create_date REAL,
                                            view bool NOT NULL,                                           
                                            doctor_report text,
                                            status bool NOT NULL
                                        ); """

        prescription_backup_table = """ CREATE TABLE IF NOT EXISTS tblPrescriptionBackup  (
                                            prescription_backup_id serial PRIMARY KEY,
                                            prescription_id integer NOT NULL,
                                            chief_complaints_prescription_id integer NOT NULL,  
                                            on_examination_prescription_id integer NOT NULL,                                          
                                            disease_identify_prescription_id integer NOT NULL,
                                            lab_test_prescription_id integer NOT NULL,                                             
                                            medicine_prescription_id integer NOT NULL,
                                            nutrition_prescription_id integer NOT NULL,
                                            bad_nutrition_prescription_id integer NOT NULL,
                                            exercise_prescription_id integer NOT NULL,                                             
                                            extend_prescription_id integer NOT NULL,
                                            start_date REAL,
                                            end_date REAL,
                                            status bool NOT NULL
                                        ); """ 

        patient_treatment_table = """ CREATE TABLE IF NOT EXISTS tblPatientTreatment  (
                                            patient_treatment_id serial PRIMARY KEY,
                                            prescription_id integer NOT NULL,
                                            chief_complaints_prescription_id integer NOT NULL, 
                                            on_examination_prescription_id integer NOT NULL,                                          
                                            disease_identify_prescription_id integer NOT NULL,
                                            lab_test_prescription_id integer NOT NULL,                                             
                                            medicine_prescription_id integer NOT NULL,
                                            nutrition_prescription_id integer NOT NULL,
                                            bad_nutrition_prescription_id integer NOT NULL,
                                            exercise_prescription_id integer NOT NULL,                                             
                                            extend_prescription_id integer NOT NULL,
                                            treatment_running bool NOT NULL,                                            
                                            prescription_file text NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """ 

        treatment_start_table = """ CREATE TABLE IF NOT EXISTS tblTreatmentStart  (
                                            treatment_start_id serial PRIMARY KEY,
                                            patient_treatment_id integer NOT NULL,
                                            start_treatment REAL NOT NULL,
                                            stop_treatment REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        treatment_result_msg_table = """ CREATE TABLE IF NOT EXISTS tblTreatmentResultMsg  (
                                            treatment_result_msg_id serial PRIMARY KEY,
                                            treatment_result_msg text,
                                            status bool NOT NULL
                                        ); """

        # treatment_result: -1=result down, 0= no change, 1= improve

        patient_treatment_result_table = """ CREATE TABLE IF NOT EXISTS tblPatientTreatmentResult  (
                                            patient_treatment_result_id serial PRIMARY KEY,
                                            patient_treatment_id integer NOT NULL,
                                            treatment_result integer NOT NULL,  
                                            treatment_result_msg_id text,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """
                                        
        public_treatment_table = """ CREATE TABLE IF NOT EXISTS tblPublicTreatment  (
                                            public_treatment_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            patient_appointment_id integer NOT NULL, 
                                            doctor_appointment_id integer NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        disease_table = """ CREATE TABLE IF NOT EXISTS tblDisease  (
                                            disease_id serial PRIMARY KEY,
                                            disease  text NOT NULL,
                                            disease_en  text,
                                            approved bool NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        previous_disease_table = """ CREATE TABLE IF NOT EXISTS tblPreviousDisease  (
                                            previous_disease_id serial PRIMARY KEY,
                                            disease_id integer NOT NULL,
                                            present bool NOT NULL,
                                            medicine bool NOT NULL,                                            
                                            body_area text NOT NULL,
                                            measure integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        previous_disease_group_table = """ CREATE TABLE IF NOT EXISTS tblPreviousDiseaseGroup  (
                                            previous_disease_group_id serial PRIMARY KEY,                                            
                                            patient_appointment_id integer NOT NULL,                                            
                                            previous_disease_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_appointment_table = """ CREATE TABLE IF NOT EXISTS tblPatientAppointment  (
                                            patient_appointment_id serial PRIMARY KEY,
                                            patient_id  integer NOT NULL,
                                            title text, 
                                            gender  bool NOT NULL,
                                            age REAL NOT NULL,  
                                            done bool NOT NULL,
                                            parent_appointment_id integer NOT NULL,
                                            daily_care_center_id integer NOT NULL, 
                                            examin_doctor_id integer NOT NULL,               
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """ 

        change_examine_doctor_table = """ CREATE TABLE IF NOT EXISTS tblChangeExamineDoctor  (
                                            change_examine_doctor_id serial PRIMARY KEY,
                                            patient_appointment_id integer NOT NULL,
                                            prv_examin_doctor_id integer NOT NULL, 
                                            new_examin_doctor_id integer NOT NULL,    
                                            change_cause text,   
                                            done bool NOT NULL,      
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        doctor_appointment_table = """ CREATE TABLE IF NOT EXISTS tblDoctorAppointment  (
                                            doctor_appointment_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            patient_id  integer NOT NULL,
                                            patient_appointment_id integer NOT NULL, 
                                            doctor_fee integer NOT NULL,
                                            appointment_time REAL NOT NULL,
                                            doctor_visited bool NOT NULL,  
                                            paid bool NOT NULL,  
                                            connecting bool NOT NULL, 
                                            room_name text,  
                                            online bool NOT NULL,
                                            user_id  integer NOT NULL,               
                                            create_date REAL,  
                                            present bool NOT NULL, 
                                            visiting_place_id integer NOT NULL, 
                                            outside bool NOT NULL, 
                                            status bool NOT NULL
                                        ); """ 

        outside_rx_table = """ CREATE TABLE IF NOT EXISTS tblOutsideRx  (
                                            outside_rx_id serial PRIMARY KEY,                                             
                                            user_id integer NOT NULL,                                                 
                                            doctor_appointment_id integer NOT NULL,                                            
                                            prescription_file text NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """


        prescription_table = """ CREATE TABLE IF NOT EXISTS tblPrescription  (
                                            prescription_id serial PRIMARY KEY,
                                            doctor_appointment_id integer NOT NULL,
                                            chief_complaints_prescription_id integer NOT NULL, 
                                            on_examination_prescription_id integer NOT NULL,                                          
                                            disease_identify_prescription_id integer NOT NULL,
                                            lab_test_prescription_id integer NOT NULL,                                             
                                            medicine_prescription_id integer NOT NULL,
                                            nutrition_prescription_id integer NOT NULL,
                                            bad_nutrition_prescription_id integer NOT NULL,
                                            exercise_prescription_id integer NOT NULL,                                             
                                            extend_prescription_id integer NOT NULL,
                                            visited_date REAL,
                                            next_visit integer,                                            
                                            modified_date REAL,                                             
                                            create_date REAL,
                                            treatment bool NOT NULL,                                            
                                            prescription_file text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        chief_complaints_prescription_table = """ CREATE TABLE IF NOT EXISTS tblChiefComplaintsPrescription  (
                                            chief_complaints_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """  

        on_examination_prescription_table = """ CREATE TABLE IF NOT EXISTS tblOnExaminationPrescription  (
                                            on_examination_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        disease_identify_prescription_table = """ CREATE TABLE IF NOT EXISTS tblDiseaseIdentifyPrescription  (
                                            disease_identify_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        lab_test_prescription_table = """ CREATE TABLE IF NOT EXISTS tblLabTestPrescription  (
                                            lab_test_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """ 

        medicine_prescription_table = """ CREATE TABLE IF NOT EXISTS tblMedicinePrescription  (
                                            medicine_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """ 

        nutrition_prescription_table = """ CREATE TABLE IF NOT EXISTS tblNutritionPrescription  (
                                            nutrition_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        bad_nutrition_prescription_table = """ CREATE TABLE IF NOT EXISTS tblBadNutritionPrescription  (
                                            bad_nutrition_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        exercise_prescription_table = """ CREATE TABLE IF NOT EXISTS tblExercisePrescription  (
                                            exercise_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        extend_prescription_table = """ CREATE TABLE IF NOT EXISTS tblExtendPrescription  (
                                            extend_prescription_id serial PRIMARY KEY,
                                            doctor_id  integer ,                                              
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        chief_complaints_table = """ CREATE TABLE IF NOT EXISTS tblChiefComplaints  (
                                            chief_complaints_id serial PRIMARY KEY,
                                            chief_complaints  text UNIQUE,
                                            status bool NOT NULL
                                        ); """  
        

        chief_complaints_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblChiefComplaintsRxGroup  (
                                            chief_complaints_rx_group_id serial PRIMARY KEY,                                            
                                            chief_complaints_prescription_id integer NOT NULL,                                            
                                            chief_complaints_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        on_examination_table = """ CREATE TABLE IF NOT EXISTS tblOnExamination  (
                                            on_examination_id serial PRIMARY KEY,
                                            on_examination  text UNIQUE,
                                            examination_report  text,
                                            status bool NOT NULL
                                        ); """  
        

        on_examination_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblOnExaminationRxGroup  (
                                            on_examination_rx_group_id serial PRIMARY KEY,                                            
                                            on_examination_prescription_id integer NOT NULL,                                            
                                            on_examination_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        disease_identify_table = """ CREATE TABLE IF NOT EXISTS tblDiseaseIdentifyRx  (
                                            disease_identify_rx_id serial PRIMARY KEY,
                                            disease_id integer NOT NULL,
                                            body_part_id integer,
                                            stage integer,
                                            status bool NOT NULL
                                        ); """

        disease_identify_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblDiseaseIdentifyRxGroup  (
                                            disease_identify_rx_group_id serial PRIMARY KEY,                                            
                                            disease_identify_prescription_id integer NOT NULL,                                            
                                            disease_identify_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """


        # quantity miligram per day
        nutrition_rx_table = """ CREATE TABLE IF NOT EXISTS tblNutritionRx  (
                                            nutrition_rx_id serial PRIMARY KEY, 
                                            food_element_id integer NOT NULL,
                                            min_quantity REAL NOT NULL,      
                                            max_quantity REAL NOT NULL,                                            
                                            how_many_days integer NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        nutrition_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblNutritionRxGroup  (
                                            nutrition_rx_group_id serial PRIMARY KEY,                                            
                                            nutrition_prescription_id integer NOT NULL,                                            
                                            nutrition_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """


        # quantity_level miligram per day max can be taken
        bad_nutrition_rx_table = """ CREATE TABLE IF NOT EXISTS tblBadNutritionRx  (
                                            bad_nutrition_rx_id serial PRIMARY KEY, 
                                            food_element_id integer NOT NULL,
                                            max_quantity REAL NOT NULL,                                            
                                            how_many_days integer NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        bad_nutrition_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblBadNutritionRxGroup  (
                                            bad_nutrition_rx_group_id serial PRIMARY KEY,                                            
                                            bad_nutrition_prescription_id integer NOT NULL,                                            
                                            bad_nutrition_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        medicine_rx_table = """ CREATE TABLE IF NOT EXISTS tblMedicineRx  (
                                            medicine_rx_id serial PRIMARY KEY, 
                                            medicine_id integer NOT NULL,
                                            daily_schedule_id integer NOT NULL,
                                            befor_eating_id integer NOT NULL,
                                            days_number integer NOT NULL,
                                            days_unit text NOT NULL,
                                            medicine_extra_guide_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        medicine_extra_guide_table = """ CREATE TABLE IF NOT EXISTS tblMedicineExtraGuide  (
                                            medicine_extra_guide_id serial PRIMARY KEY,
                                            extra_guide text UNIQUE,
                                            status bool NOT NULL
                                        ); """    

        medicine_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblMedicineRxGroup  (
                                            medicine_rx_group_id serial PRIMARY KEY,                                            
                                            medicine_prescription_id integer NOT NULL,                                            
                                            medicine_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        exercise_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblExerciseRxGroup  (
                                            exercise_rx_group_id serial PRIMARY KEY,                                             
                                            exercise_prescription_id integer NOT NULL,                                          
                                            exercise_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """


        exercise_table = """ CREATE TABLE IF NOT EXISTS tblExercise (
                                            exercise_id serial PRIMARY KEY,
                                            exercise text NOT NULL,
                                            exercise_guide text NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        exercise_schedule_table = """ CREATE TABLE IF NOT EXISTS tblExerciseSchedule (
                                            exercise_schedule_id serial PRIMARY KEY,
                                            exercise_schedule text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        exercise_rx_table = """ CREATE TABLE IF NOT EXISTS tblExerciseRx  (
                                            exercise_rx_id serial PRIMARY KEY, 
                                            exercise_id integer NOT NULL,
                                            exercise_schedule_id integer NOT NULL,                                    
                                            how_many_days integer NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        extend_rx_table = """ CREATE TABLE IF NOT EXISTS tblExtendRx  (
                                            extend_rx_id serial PRIMARY KEY,
                                            extend_guide text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        extend_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblExtendRxGroup  (
                                            extend_rx_group_id serial PRIMARY KEY,                                              
                                            extend_prescription_id integer NOT NULL,                                            
                                            extend_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        lab_test_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblLabTestRxGroup  (
                                            lab_test_rx_group_id serial PRIMARY KEY,                                              
                                            lab_test_prescription_id integer NOT NULL,                                            
                                            lab_test_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_lab_test_report_url_table = """ CREATE TABLE IF NOT EXISTS tblPatientLabTestReportUrl  (
                                            patient_lab_test_report_url_id serial PRIMARY KEY,                                              
                                            prescription_id integer NOT NULL,                                            
                                            lab_test_report_url text NOT NULL,
                                            report_view_by_doctor bool NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_lab_test_report_table = """ CREATE TABLE IF NOT EXISTS tblPatientLabTestReport  (
                                            patient_lab_test_report_id serial PRIMARY KEY,                                              
                                            prescription_id integer NOT NULL,                                            
                                            lab_test_report_id integer NOT NULL,  
                                            efective_value integer, 
                                            status bool NOT NULL
                                        ); """ 


        reminded_rx_table = """ CREATE TABLE IF NOT EXISTS tblRemindedRx  (
                                            reminded_rx_id serial PRIMARY KEY,
                                            reminded_guide text NOT NULL,
                                            reminded_time REAL NOT NULL,                                            
                                            period integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        reminded_rx_group_table = """ CREATE TABLE IF NOT EXISTS tblRemindedRxGroup  (
                                            reminded_rx_group_id serial PRIMARY KEY,                                            
                                            reminded_prescription_id integer NOT NULL,                                            
                                            reminded_rx_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        covid_hospital_table = """ CREATE TABLE IF NOT EXISTS tblCovidHospital  (
                                            covid_hospital_id serial PRIMARY KEY,
                                            covid_hospital  text NOT NULL,                                             
                                            icu_bed integer NOT NULL,                                       
                                            longitude REAL NOT NULL,                                            
                                            latitude REAL NOT NULL, 
                                            address text NOT NULL, 
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        movement_location_table = """ CREATE TABLE IF NOT EXISTS tblMovementLocation  (
                                            movement_location_id serial PRIMARY KEY,        
                                            longitude REAL NOT NULL,                                            
                                            latitude REAL NOT NULL,
                                            covid integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        notification_table = """ CREATE TABLE IF NOT EXISTS tblNotification   (
                                            notification_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            subject  text NOT NULL,
                                            notification  text NOT NULL,
                                            create_date REAL NOT NULL,
                                            read bool NOT NULL,
                                            status bool NOT NULL
                                        ); """


        medicine_dosage_forms_table = """ CREATE TABLE IF NOT EXISTS tblMedicineDosageForms (
                                            medicine_dosage_forms_id serial PRIMARY KEY,
                                            dosage_form text NOT NULL,
                                            detail text NOT NULL,
                                            short_form text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        medicine_table = """ CREATE TABLE IF NOT EXISTS tblMedicine (
                                            medicine_id serial PRIMARY KEY,
                                            generic_medicine_name text NOT NULL,
                                            brand_medicine_name text NOT NULL,
                                            medicine_dosage_form text NOT NULL,
                                            strength text NOT NULL,
                                            brand_name text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        medicine_details_table = """ CREATE TABLE IF NOT EXISTS tblMedicineDetails (
                                            medicine_details_id serial PRIMARY KEY,
                                            medicine_id integer NOT NULL,
                                            brand_name text NOT NULL,
                                            uses text NOT NULL,
                                            side_effects text NOT NULL,
                                            history text NOT NULL,
                                            image_url text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        daily_schedule_table = """ CREATE TABLE IF NOT EXISTS tblDailySchedule (
                                            daily_schedule_id serial PRIMARY KEY,
                                            daily_schedule text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        befor_eating_table = """ CREATE TABLE IF NOT EXISTS tblBeforEating (
                                            befor_eating_id serial PRIMARY KEY,
                                            befor_eating text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        extend_table = """ CREATE TABLE IF NOT EXISTS tblExtend (
                                            extend_id serial PRIMARY KEY,
                                            extend text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        daily_care_center_table = """ CREATE TABLE IF NOT EXISTS tblDailyCareCenter  (
                                            daily_care_center_id serial PRIMARY KEY,
                                            daily_care_center  text NOT NULL,                                        
                                            district_id integer NOT NULL,                                            
                                            thana_id integer NOT NULL, 
                                            place text NOT NULL,                                       
                                            longitude REAL NOT NULL,                                            
                                            latitude REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        about_cost_table = """ CREATE TABLE IF NOT EXISTS tblAboutCost  (
                                            about_cost_id serial PRIMARY KEY,
                                            about_cost  text NOT NULL unique,
                                            status bool NOT NULL
                                        ); """
        
        daily_care_center_cost_table = """ CREATE TABLE IF NOT EXISTS tblDailyCareCenterCost (
                                            daily_care_center_cost_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            daily_care_center_id integer NOT NULL,
                                            about_cost_id integer NOT NULL,
                                            cost REAL NOT NULL,
                                            approved_user_id integer NOT NULL,
                                            approved bool NOT NULL,
                                            paid bool NOT NULL,
                                            date_time REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        # 'Duty Doctor' 'Examine Doctor' 'Health Worker' 

        employee_designation_table = """ CREATE TABLE IF NOT EXISTS tblEmployeeDesignation  (
                                            employee_designation_id serial PRIMARY KEY,
                                            designation  text NOT NULL unique,
                                            about_designation  text NOT NULL,
                                            qualifications text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        employee_designation_grade_table = """ CREATE TABLE IF NOT EXISTS tblEmployeeDesignationGrade  (
                                            employee_designation_grade_id serial PRIMARY KEY,
                                            designation_grade  text NOT NULL unique,
                                            grade_value  integer NOT NULL
                                        ); """

        # review 3=accepted 1= waiting 2=cancel
        employee_application_table = """ CREATE TABLE IF NOT EXISTS tblEmployeeApplication  (
                                            employee_application_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            employee_designation_id integer NOT NULL,
                                            application  text NOT NULL,
                                            cv_pdf  text NOT NULL,
                                            review integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        employee_table = """ CREATE TABLE IF NOT EXISTS tblEmployee  (
                                            employee_id serial PRIMARY KEY,
                                            user_id integer NOT NULL unique,
                                            cv_pdf  text NOT NULL,
                                            is_admin bool NOT NULL,
                                            employee_designation_id integer NOT NULL,
                                            joining_date text NOT NULL,
                                            resignation_date text NOT NULL,
                                            create_date REAL NOT NULL,
                                            posted bool NOT NULL
                                        ); """

        employee_duty_table = """ CREATE TABLE IF NOT EXISTS tblEmployeeDuty  (
                                            employee_duty_id serial PRIMARY KEY,
                                            employee_duty text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        employee_posting_table = """ CREATE TABLE IF NOT EXISTS tblEmployeePosting  (
                                            employee_posting_id serial PRIMARY KEY,
                                            employee_id integer NOT NULL,
                                            daily_care_center_id integer NOT NULL,
                                            employee_designation_id integer NOT NULL,
                                            employee_designation_grade_id integer NOT NULL,
                                            posting_date REAL NOT NULL,
                                            closing_date REAL NOT NULL,
                                            basic_salary REAL NOT NULL,
                                            house_rent REAL NOT NULL,
                                            house_maintenance_allowan REAL NOT NULL,
                                            medical_allowan REAL NOT NULL,
                                            posting_notes text NOT NULL,
                                            employee_duty_id integer NOT NULL,
                                            approved bool NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        device_table = """ CREATE TABLE IF NOT EXISTS tblDevice  (
                                            device_id serial PRIMARY KEY,
                                            device_mac_id text NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        employee_present_table = """ CREATE TABLE IF NOT EXISTS tblEmployeePresent  (
                                            employee_present_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            employee_posting_id integer NOT NULL,
                                            office_in REAL NOT NULL,
                                            office_in_lat REAL NOT NULL,
                                            office_in_lon REAL NOT NULL,
                                            office_out REAL NOT NULL,
                                            office_out_lat REAL NOT NULL,
                                            office_out_lon REAL NOT NULL,
                                            device_id integer NOT NULL,
                                            present REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        employee_leave_table = """ CREATE TABLE IF NOT EXISTS tblEmployeeLeave  (
                                            employee_leave_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            employee_posting_id integer NOT NULL,
                                            employee_leave_start_date REAL NOT NULL,
                                            employee_leave_end_date REAL NOT NULL,
                                            leave_days REAL NOT NULL,
                                            aproved bool NOT NULL,
                                            aproved_user_id integer NOT NULL,
                                            aproved_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        pay_employee_salary_table = """ CREATE TABLE IF NOT EXISTS tblPayEmployeeSalary  (
                                            pay_employee_salary_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            employee_posting_id integer NOT NULL,
                                            office_day integer NOT NULL,
                                            present REAL NOT NULL,
                                            off_day integer NOT NULL,
                                            leave_day REAL NOT NULL,
                                            salary REAL NOT NULL,
                                            salary_month integer NOT NULL,
                                            salary_date REAL NOT NULL,
                                            paid bool NOT NULL,
                                            paid_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        employee_querymsg_table = """ CREATE TABLE IF NOT EXISTS tblEmployeeQuerymsg  (
                                            employee_querymsg_id serial PRIMARY KEY,
                                            sender_user_id integer NOT NULL,
                                            employee_id integer NOT NULL,
                                            msg text NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        examin_doctor_table = """ CREATE TABLE IF NOT EXISTS tblExaminDoctor  (
                                            examin_doctor_id serial PRIMARY KEY,
                                            employee_id integer NOT NULL,
                                            doctor_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            resign_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            posted bool NOT NULL
                                        ); """ 

        duty_doctor_table = """ CREATE TABLE IF NOT EXISTS tblDutyDoctor  (
                                            duty_doctor_id serial PRIMARY KEY,
                                            employee_id integer NOT NULL,
                                            doctor_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            resign_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            posted bool NOT NULL
                                        ); """ 

        daily_care_doctor_table = """ CREATE TABLE IF NOT EXISTS tblDailyCareDoctor  (
                                            daily_care_doctor_id serial PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            resign_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            posted bool NOT NULL
                                        ); """

        health_worker_table = """ CREATE TABLE IF NOT EXISTS tblHealthWorker  (
                                            health_worker_id serial PRIMARY KEY,
                                            employee_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            resign_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            posted bool NOT NULL
                                        ); """ 

        accountant_table = """ CREATE TABLE IF NOT EXISTS tblAccountant  (
                                            accountant_id serial PRIMARY KEY,
                                            employee_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            resign_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            posted bool NOT NULL
                                        ); """

        daily_care_fee_collection_table = """ CREATE TABLE IF NOT EXISTS tblDailyCareFeeCollection  (
                                            daily_care_fee_collection_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            daily_care_charge_id integer NOT NULL,
                                            doctor_appointment_id integer NOT NULL,
                                            daily_care_fee REAL NOT NULL,
                                            collection_date REAL NOT NULL,
                                            deposit_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        diabetes_test_fees_collection_table = """ CREATE TABLE IF NOT EXISTS tblDiabetesTestFeesCollection  (
                                            diabetes_test_fees_collection_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,                                            
                                            daily_care_center_id integer NOT NULL,
                                            patient_id integer NOT NULL,  
                                            blood_sugar_test_type_id integer NOT NULL, 
                                            sugar_level REAL NOT NULL,  
                                            diabetes_status integer NOT NULL,  
                                            diabetes_test_fees REAL NOT NULL,
                                            collection_date REAL NOT NULL,
                                            deposit_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        doctor_fees_collection_table = """ CREATE TABLE IF NOT EXISTS tblDoctorFeesCollection  (
                                            doctor_fees_collection_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            doctor_id integer NOT NULL,
                                            doctor_appointment_id integer NOT NULL,
                                            doctor_fees REAL NOT NULL,
                                            collection_date REAL NOT NULL,
                                            deposit_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        about_transaction_table = """ CREATE TABLE IF NOT EXISTS tblAboutTransaction  (
                                            about_transaction_id serial PRIMARY KEY,           
                                            about_transaction  text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        collection_from_employee_table = """ CREATE TABLE IF NOT EXISTS tblCollectionFromEmployee  (
                                            collection_from_employee_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            daily_care_center_id integer NOT NULL,
                                            from_user_id integer NOT NULL,
                                            employee_duty_id integer NOT NULL,
                                            amount REAL NOT NULL,                                            
                                            about_transaction_id integer NOT NULL,
                                            collection_date REAL NOT NULL,
                                            deposit_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        deposit_center_collection_table = """ CREATE TABLE IF NOT EXISTS tblDepositCenterCollection  (
                                            deposit_center_collection_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            daily_care_center_id integer NOT NULL,
                                            from_user_id integer NOT NULL,
                                            amount REAL NOT NULL,
                                            collection_date REAL NOT NULL,
                                            deposit_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        doctor_fee_back_table = """ CREATE TABLE IF NOT EXISTS tblDoctorFeeBack  (
                                            doctor_fee_back_id serial PRIMARY KEY,
                                            doctor_appointment_id integer NOT NULL,
                                            back_fee REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        help_question_table = """ CREATE TABLE IF NOT EXISTS tblHelpQuestion  (
                                            help_question_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,                                            
                                            help_type  text NOT NULL,                                            
                                            message  text NOT NULL,
                                            answered bool NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        body_area_table = """ CREATE TABLE IF NOT EXISTS tblBodyArea  (
                                            body_area_id serial PRIMARY KEY,
                                            body_area text NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        body_part_table = """ CREATE TABLE IF NOT EXISTS tblBodyPart  (
                                            body_part_id serial PRIMARY KEY,
                                            body_part text NOT NULL,
                                            outer_inner bool NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        doctor_specialty_table = """ CREATE TABLE IF NOT EXISTS tblDoctorSpecialty  (
                                            doctor_specialty_id serial PRIMARY KEY,
                                            doctor_specialty text NOT NULL,
                                            about text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        doctor_degree_table = """ CREATE TABLE IF NOT EXISTS tblDoctorDegree  (
                                            doctor_degree_id serial PRIMARY KEY,
                                            doctor_degree text NOT NULL,
                                            about text NOT NULL,
                                            status bool NOT NULL
                                        ); """



        # Histroy Taking.................start........... 


        occupation_table = """ CREATE TABLE IF NOT EXISTS tblOccupation (
                                            occupation_id serial PRIMARY KEY,
                                            occupation text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        education_table = """ CREATE TABLE IF NOT EXISTS tblEducation (
                                            education_id serial PRIMARY KEY,
                                            education text NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        religious_table = """ CREATE TABLE IF NOT EXISTS tblReligious (
                                            religious_id serial PRIMARY KEY,
                                            religious text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        hobbies_table = """ CREATE TABLE IF NOT EXISTS tblHobbies (
                                            hobbies_id serial PRIMARY KEY,
                                            hobbies text NOT NULL,  
                                            status bool NOT NULL
                                        ); """

        social_history_table = """ CREATE TABLE IF NOT EXISTS tblSocialHistory (
                                            social_history_id serial PRIMARY KEY,
                                            patient_id integer NOT NULL,
                                            occupation_id integer,
                                            education_id integer,
                                            religious_id integer NOT NULL,
                                            hobbies_id integer,
                                            marital_status bool NOT NULL,
                                            married_date text,
                                            widowed_date text,
                                            divorced_date text,
                                            childrens integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # habits_status = not(0)/irregular(1)/regular(2)                                      
        # Dosage integer = 0....... 10

        patient_good_habits_history_table = """ CREATE TABLE IF NOT EXISTS tblPatientGoodHabitsHistory (
                                            patient_good_habits_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            good_habits_id integer NOT NULL,
                                            habits_status integer NOT NULL,
                                            dosage integer NOT NULL, 
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_bad_habits_history_table = """ CREATE TABLE IF NOT EXISTS tblPatientBadHabitsHistory (
                                            patient_bad_habits_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            bad_habits_id integer NOT NULL,
                                            habits_status integer NOT NULL,
                                            dosage integer NOT NULL, 
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """


        medicine_reaction_table = """ CREATE TABLE IF NOT EXISTS tblMedicineReaction (
                                            medicine_reaction_id serial PRIMARY KEY, 
                                            medicine_reaction text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        medication_allergies_table = """ CREATE TABLE IF NOT EXISTS tblMedicationAllergies (
                                            medication_allergies_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            medicine_id integer NOT NULL,
                                            medicine_reaction_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        injuries_table = """ CREATE TABLE IF NOT EXISTS tblInjuries (
                                            injuries_id serial PRIMARY KEY, 
                                            injuries text NOT NULL,
                                            status bool NOT NULL
                                        ); """

       
        # injuries_status = mejor/minor

        injuries_history_table = """ CREATE TABLE IF NOT EXISTS tblInjuriesHistory (
                                            injuries_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            injuries_id integer NOT NULL,
                                            body_part_id integer NOT NULL,
                                            injuries_status bool NOT NULL,
                                            injuries_date text NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        medical_history_table = """ CREATE TABLE IF NOT EXISTS tblMedicalHistory  (
                                            medical_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            disease_id integer NOT NULL,
                                            present bool NOT NULL,
                                            medicine bool NOT NULL,                                            
                                            body_part_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """


        rx_history_table = """ CREATE TABLE IF NOT EXISTS tblRxHistory  (
                                            rx_history_id serial PRIMARY KEY,
                                            patient_id integer NOT NULL,
                                            medical_history_id integer NOT NULL,                                                 
                                            rx_pic text NOT NULL,
                                            rx_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        report_history_table = """ CREATE TABLE IF NOT EXISTS tblReportHistory  (
                                            report_history_id serial PRIMARY KEY,
                                            patient_id integer NOT NULL,          
                                            rx_history_id integer NOT NULL,                                           
                                            lab_test_id integer NOT NULL,                                            
                                            report_urls text NOT NULL,                                            
                                            report text NOT NULL,
                                            report_date REAL NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL
                                        ); """

        

        surgical_table = """ CREATE TABLE IF NOT EXISTS tblSurgical (
                                            surgical_id serial PRIMARY KEY, 
                                            surgical_name text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # surgical_status = mejor/minor


        surgical_history_table = """ CREATE TABLE IF NOT EXISTS tblSurgicalHistory (
                                            surgical_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,          
                                            rx_history_id integer NOT NULL,
                                            surgical_id integer NOT NULL,
                                            body_part_id integer NOT NULL,
                                            surgical_status bool NOT NULL,
                                            surgical_date text NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # per_days...kotodin por por (1din,7din,30din....)
        medications_history_table = """ CREATE TABLE IF NOT EXISTS tblMedicationsHistory  (
                                            medications_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            medicine_id integer NOT NULL,
                                            start_date text NOT NULL,
                                            per_days integer NOT NULL,
                                            number_of_time integer NOT NULL,
                                            how_many_days integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        family_table = """ CREATE TABLE IF NOT EXISTS tblFamily (
                                            family_id serial PRIMARY KEY, 
                                            family text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        family_history_table = """ CREATE TABLE IF NOT EXISTS tblFamilyHistory  (
                                            family_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            disease_id integer NOT NULL,
                                            family_id integer NOT NULL,                                            
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        misbehavior_table = """ CREATE TABLE IF NOT EXISTS tblMisbehavior (
                                            misbehavior_id serial PRIMARY KEY, 
                                            misbehavior text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        ever_misbehavior_history_table = """ CREATE TABLE IF NOT EXISTS tblEverMisbehaviorHistory  (
                                            ever_misbehavior_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            misbehavior_id integer NOT NULL,
                                            misbehavior_level integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        delivery_mode_table = """ CREATE TABLE IF NOT EXISTS tblDeliveryMode (
                                            delivery_mode_id serial PRIMARY KEY, 
                                            delivery_mode text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        baby_condition_table = """ CREATE TABLE IF NOT EXISTS tblBabyCondition (
                                            baby_condition_id serial PRIMARY KEY, 
                                            baby_condition text NOT NULL, 
                                            status bool NOT NULL
                                        ); """


        patient_delivery_history_table = """ CREATE TABLE IF NOT EXISTS tblPatientDeliveryHistory  (
                                            patient_delivery_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            delivery_mode_id integer NOT NULL,
                                            delivery_date text NOT NULL,
                                            nth_delivery integer NOT NULL,
                                            baby_gendar bool NOT NULL,
                                            baby_live bool NOT NULL,
                                            baby_condition_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_pregnancy_history_table = """ CREATE TABLE IF NOT EXISTS tblPatientPregnancyHistory  (
                                            patient_pregnancy_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            first_menstrual_age REAL NOT NULL,
                                            menstrual_priod integer NOT NULL,
                                            menstrual_cycle integer NOT NULL,
                                            lmp text NOT NULL,
                                            edd text NOT NULL,
                                            marrid_age REAL NOT NULL,
                                            para REAL NOT NULL,
                                            gravida REAL NOT NULL,
                                            last_child_age REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        child_development_table = """ CREATE TABLE IF NOT EXISTS tblChildDevelopment (
                                            child_development_id serial PRIMARY KEY, 
                                            child_development text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        child_development_history_table = """ CREATE TABLE IF NOT EXISTS tblChildDevelopmentHistory  (
                                            child_development_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            child_development_id integer NOT NULL,
                                            growth integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        child_sensory_concerns_table = """ CREATE TABLE IF NOT EXISTS tblChildSensoryConcerns (
                                            child_sensory_concerns_id serial PRIMARY KEY, 
                                            child_sensory_concerns text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        child_sensory_concerns_history_table = """ CREATE TABLE IF NOT EXISTS tblChildSensoryConcernsHistory  (
                                            child_sensory_concerns_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            child_sensory_concerns_id integer NOT NULL,
                                            concern bool NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        
        temperament_table = """ CREATE TABLE IF NOT EXISTS tblTemperament (
                                            temperament_id serial PRIMARY KEY, 
                                            temperament text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        temperament_history_table = """ CREATE TABLE IF NOT EXISTS tblTemperamentHistory  (
                                            temperament_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            temperament_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        
        menstrual_table = """ CREATE TABLE IF NOT EXISTS tblMenstrual (
                                            menstrual_id serial PRIMARY KEY, 
                                            menstrual text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        menstrual_history_table = """ CREATE TABLE IF NOT EXISTS tblMenstrualHistory  (
                                            menstrual_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            menstrual_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        travel_table = """ CREATE TABLE IF NOT EXISTS tblTravel (
                                            travel_id serial PRIMARY KEY, 
                                            travel text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        travel_history_table = """ CREATE TABLE IF NOT EXISTS tblTravelHistory  (
                                            travel_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            travel_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        birth_table = """ CREATE TABLE IF NOT EXISTS tblBirth (
                                            birth_id serial PRIMARY KEY, 
                                            birth text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        birth_history_table = """ CREATE TABLE IF NOT EXISTS tblBirthHistory  (
                                            birth_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            birth_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        feeding_table = """ CREATE TABLE IF NOT EXISTS tblFeeding (
                                            feeding_id serial PRIMARY KEY, 
                                            feeding text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        feeding_history_table = """ CREATE TABLE IF NOT EXISTS tblFeedingHistory  (
                                            feeding_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            feeding_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        allergy_substance_table = """ CREATE TABLE IF NOT EXISTS tblAllergySubstance (
                                            allergy_substance_id serial PRIMARY KEY, 
                                            allergy_substance text NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        allergy_reaction_table = """ CREATE TABLE IF NOT EXISTS tblAllergyReaction (
                                            allergy_reaction_id serial PRIMARY KEY, 
                                            allergy_reaction text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        allergy_history_table = """ CREATE TABLE IF NOT EXISTS tblAllergyHistory  (
                                            allergy_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,
                                            allergy_substance_id integer NOT NULL,
                                            allergy_reaction_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

                                        

        # End History taking....................
        

        symptom_table = """ CREATE TABLE IF NOT EXISTS tblSymptom  (
                                            symptom_id serial PRIMARY KEY,
                                            symptom  text NOT NULL,
                                            body_part_id  integer,
                                            approved bool NOT NULL,
                                            create_date REAL,
                                            status bool NOT NULL,
                                            symptom_en  text NOT NULL
                                        ); """

        patient_symptom_table = """ CREATE TABLE IF NOT EXISTS tblPatientSymptom  (
                                            patient_symptom_id serial PRIMARY KEY,                                  
                                            patient_appointment_id integer NOT NULL,    
                                            symptom_id integer NOT NULL,
                                            measure integer NOT NULL,
                                            symptom_days integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """                                 
        
        general_examination_table = """ CREATE TABLE IF NOT EXISTS tblGeneralExamination (
                                            general_examination_id serial PRIMARY KEY, 
                                            general_examination text NOT NULL,
                                            status bool NOT NULL
                                        ); """                                   
        
        general_diagnosis_data_table = """ CREATE TABLE IF NOT EXISTS tblGeneralDiagnosisData (
                                            general_diagnosis_data_id serial PRIMARY KEY, 
                                            general_examination_id integer NOT NULL,
                                            general_diagnosis_data text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        general_examination_datas_table = """ CREATE TABLE IF NOT EXISTS tblGeneralExaminationDatas  (
                                            general_examination_datas_id serial PRIMARY KEY, 
                                            patient_appointment_id integer NOT NULL,
                                            general_diagnosis_data_id integer NOT NULL,
                                            diagnosis_data_url text NOT NULL,
                                            create_date REAL NOT NULL,
                                            by_doctor bool NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        systemic_examination_table = """ CREATE TABLE IF NOT EXISTS tblSystemicExamination (
                                            systemic_examination_id serial PRIMARY KEY,
                                            systemic_examination text NOT NULL, 
                                            status bool NOT NULL
                                        ); """                                    
        
        systemic_diagnosis_data_table = """ CREATE TABLE IF NOT EXISTS tblSystemicDiagnosisData (
                                            systemic_diagnosis_data_id serial PRIMARY KEY,                                           
                                            body_part_id integer NOT NULL,
                                            systemic_examination_id integer NOT NULL, 
                                            systemic_diagnosis_data text NOT NULL,
                                            status bool NOT NULL
                                        ); """ 
                

        systemic_examination_datas_table = """ CREATE TABLE IF NOT EXISTS tblSystemicExaminationDatas (
                                            systemic_examination_datas_id serial PRIMARY KEY, 
                                            patient_appointment_id integer NOT NULL, 
                                            systemic_diagnosis_data_id integer NOT NULL,
                                            diagnosis_data_url text NOT NULL,
                                            create_date REAL NOT NULL,
                                            by_doctor bool NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        examination_report_table = """ CREATE TABLE IF NOT EXISTS tblExaminationReport  (
                                            examination_report_id serial PRIMARY KEY,
                                            examination_report text NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_examination_report_table = """ CREATE TABLE IF NOT EXISTS tblPatientExaminationReport  (
                                            patient_examination_report_id serial PRIMARY KEY, 
                                            patient_appointment_id integer NOT NULL,                                            
                                            examination_report_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            by_doctor bool NOT NULL,
                                            status bool NOT NULL
                                        ); """

        lab_test_table = """ CREATE TABLE IF NOT EXISTS tblLabTest (
                                            lab_test_id serial PRIMARY KEY,
                                            lab_test text NOT NULL,
                                            normal_lower_range integer, 
                                            normal_uper_range integer, 
                                            normal_range_description text, 
                                            units text,
                                            status bool NOT NULL
                                        ); """

        lab_test_comment_table = """ CREATE TABLE IF NOT EXISTS tblLabTestComment (
                                            lab_test_comment_id serial PRIMARY KEY,
                                            comment text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        lab_test_report_table = """ CREATE TABLE IF NOT EXISTS tblLabTestReport (
                                            lab_test_report_id serial PRIMARY KEY,
                                            lab_test_id integer, 
                                            result REAL, 
                                            lab_test_comment_id integer,
                                            status bool NOT NULL
                                        ); """ 

        lab_test_report_history_table = """ CREATE TABLE IF NOT EXISTS tblLabTestReportHistory  (
                                            lab_test_report_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,                                            
                                            lab_test_id integer NOT NULL,
                                            patient_test_report_id integer NOT NULL, 
                                            result integer NOT NULL,
                                            comments text NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        vaccine_table = """ CREATE TABLE IF NOT EXISTS tblVaccine (
                                            vaccine_id serial PRIMARY KEY,
                                            vaccine text NOT NULL,
                                            about_vaccine text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        vaccine_history_table = """ CREATE TABLE IF NOT EXISTS tblVaccineHistory  (
                                            vaccine_history_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,                                            
                                            vaccine_id integer NOT NULL,
                                            patient_age REAL NOT NULL, 
                                            vaccine_date text NOT NULL, 
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        # Daily Care and data collection....

        
        care_package_table = """ CREATE TABLE IF NOT EXISTS tblCarePackage (
                                            care_package_id serial PRIMARY KEY,
                                            package_name text NOT NULL,
                                            package_fee integer NOT NULL,
                                            number_of_visit integer NOT NULL,
                                            interval integer NOT NULL,
                                            duration integer NOT NULL,
                                            repeated bool NOT NULL,
                                            status bool NOT NULL
                                        ); """ 
        
        care_registration_table = """ CREATE TABLE IF NOT EXISTS tblCareRegistration (
                                            care_registration_id serial PRIMARY KEY,
                                            user_id integer NOT NULL,
                                            daily_care_center_id integer NOT NULL,
                                            patient_id integer NOT NULL,
                                            care_package_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            end_date REAL,
                                            next_care_time REAL NOT NULL,
                                            conformed bool NOT NULL,
                                            status bool NOT NULL
                                        ); """ 
        
        care_bill_collection_table = """ CREATE TABLE IF NOT EXISTS tblCareBillCollection (
                                            care_bill_collection_id serial PRIMARY KEY,
                                            care_registration_id integer NOT NULL,
                                            bill REAL NOT NULL,
                                            from_date REAL NOT NULL,
                                            to_date REAL NOT NULL,
                                            collection_date REAL NOT NULL,
                                            collected bool NOT NULL,
                                            collecter_user_id integer NOT NULL,
                                            deposit_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 
        
        daily_care_report_public_acces_table = """ CREATE TABLE IF NOT EXISTS tblDailyCareReportPublicAcces (
                                            daily_care_report_public_acces_id serial PRIMARY KEY, 
                                            acces_code text NOT NULL UNIQUE,
                                            user_id integer NOT NULL,
                                            patient_id integer NOT NULL,
                                            start_date REAL NOT NULL,
                                            end_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        daily_data_topic_table = """ CREATE TABLE IF NOT EXISTS tblDailyDataTopic  (
                                            daily_data_topic_id serial PRIMARY KEY,  
                                            daily_data_topic_code int NOT NULL UNIQUE,
                                            topic text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        daily_visit_comments_table = """ CREATE TABLE IF NOT EXISTS tblDailyVisitComments  (
                                            daily_visit_comments_id serial PRIMARY KEY, 
                                            comments text NOT NULL,
                                            call_doctor bool NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_visit_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyVisit  (
                                            patient_daily_visit_id serial PRIMARY KEY, 
                                            care_registration_id integer NOT NULL,                                            
                                            health_worker_id integer NOT NULL,  
                                            daily_visit_comments_id integer NOT NULL,
                                            monitoring_doctor_id integer NOT NULL, 
                                            view_monitoring_doctor bool NOT NULL,
                                            total_effective_value REAL NOT NULL,
                                            max_effective_value REAL NOT NULL, 
                                            number_of_effect integer NOT NULL,   
                                            visit_date REAL NOT NULL,
                                            lat REAL NOT NULL,
                                            lan REAL NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        doctor_response_table = """ CREATE TABLE IF NOT EXISTS tblDoctorResponse  (
                                            doctor_response_id serial PRIMARY KEY, 
                                            doctor_response text NOT NULL,
                                            emergency_call integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        monitoring_doctor_response_table = """ CREATE TABLE IF NOT EXISTS tblMonitoringDoctorResponse  (
                                            monitoring_doctor_response_id serial PRIMARY KEY,
                                            patient_daily_visit_id integer NOT NULL,
                                            doctor_response_id integer NOT NULL,
                                            patient_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_medicine_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyMedicine (
                                            patient_daily_medicine_id serial PRIMARY KEY,
                                            patient_daily_visit_id integer NOT NULL,
                                            medicine_id integer NOT NULL,
                                            medicine_taken integer NOT NULL,
                                            medicine_need integer NOT NULL,
                                            report_date REAL,
                                            non_prescribe bool NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_daily_bp_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyBp  (
                                            patient_daily_bp_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,
                                            systolic integer NOT NULL, 
                                            diastolic integer NOT NULL,
                                            effective_value REAL NOT NULL,         
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        bp_effect_table = """ CREATE TABLE IF NOT EXISTS tblBpEffect  (
                                            bp_effect_id serial PRIMARY KEY,  
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,  
                                            gender bool NOT NULL,  
                                            systolic integer NOT NULL, 
                                            diastolic integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        blood_sugar_test_type_table = """ CREATE TABLE IF NOT EXISTS tblBloodSugarTestType  (
                                            blood_sugar_test_type_id serial PRIMARY KEY, 
                                            test_name text NOT NULL,
                                            how_to_test text NOT NULL,
                                            test_unit text NOT NULL,
                                            normal REAL NOT NULL, 
                                            prediabetes REAL NOT NULL,  
                                            diabetes REAL NOT NULL,               
                                            status bool NOT NULL
                                        ); """

        patient_daily_blood_sugar_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyBloodSugar  (
                                            patient_daily_blood_sugar_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL, 
                                            blood_sugar_test_type_id integer NOT NULL, 
                                            sugar_level REAL NOT NULL,  
                                            diabetes_status integer NOT NULL,
                                            effective_value REAL NOT NULL,                            
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        blood_sugar_effect_table = """ CREATE TABLE IF NOT EXISTS tblBloodSugarEffect  (
                                            blood_sugar_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,   
                                            blood_sugar_test_type_id REAL NOT NULL,
                                            sugar_level REAL NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_pulse_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyPulse  (
                                            patient_daily_pulse_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,  
                                            pulse_level REAL NOT NULL,  
                                            effective_value REAL NOT NULL,                             
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        pulse_effect_table = """ CREATE TABLE IF NOT EXISTS tblPulseEffect  (
                                            pulse_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            pulse_level integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_oxygen_saturation_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyOxygenSaturation  (
                                            patient_daily_oxygen_saturation_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,  
                                            oxygen_saturation REAL NOT NULL,
                                            effective_value REAL NOT NULL,                               
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        oxygen_saturation_effect_table = """ CREATE TABLE IF NOT EXISTS tblOxygenSaturationEffect  (
                                            oxygen_saturation_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            oxygen_saturation integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_temparature_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyTemparature  (
                                            patient_daily_temparature_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,  
                                            temparature REAL NOT NULL,
                                            effective_value REAL NOT NULL,                               
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        temparature_effect_table = """ CREATE TABLE IF NOT EXISTS tblTemparatureEffect  (
                                            temparature_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            temparature REAL NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_taken_food_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyTakenFood  (
                                            patient_daily_taken_food_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL, 
                                            food_id integer NOT NULL, 
                                            amount REAL NOT NULL,  
                                            food_process_id integer NOT NULL,
                                            effective_value REAL NOT NULL,                             
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        food_effect_table = """ CREATE TABLE IF NOT EXISTS tblFoodEffect  (
                                            food_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            food_id integer NOT NULL,
                                            amount integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # normal_load = hours per day
        workload_table = """ CREATE TABLE IF NOT EXISTS tblWorkload  (
                                            workload_id serial PRIMARY KEY, 
                                            work text NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        # workload = hours per day
        patient_daily_workload_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyWorkload  (
                                            patient_daily_Workload_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL, 
                                            workload_id integer NOT NULL, 
                                            workload REAL NOT NULL,  
                                            effective_value integer NOT NULL,                            
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        Workload_effect_table = """ CREATE TABLE IF NOT EXISTS tblWorkloadEffect  (
                                            workload_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            workload_id integer NOT NULL, 
                                            workload REAL NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        good_habits_table = """ CREATE TABLE IF NOT EXISTS tblGoodHabits (
                                            good_habits_id serial PRIMARY KEY,
                                            habits text NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_daily_good_habits_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyGoodHabits (
                                            patient_daily_good_habits_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,                                           
                                            good_habits_id integer NOT NULL,
                                            days integer NOT NULL,
                                            how_much REAL NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        good_habits_effect_table = """ CREATE TABLE IF NOT EXISTS tblGoodHabitsEffect  (
                                            good_habits_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            good_habits_id integer NOT NULL,
                                            how_mucha_perday REAL NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        bad_habits_table = """ CREATE TABLE IF NOT EXISTS tblBadHabits (
                                            bad_habits_id serial PRIMARY KEY,
                                            habits text NOT NULL,
                                            status bool NOT NULL
                                        ); """


        patient_daily_bad_habits_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyBadHabits (
                                            patient_daily_bad_habits_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,                                           
                                            bad_habits_id integer NOT NULL,
                                            days integer NOT NULL,
                                            how_much REAL NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        bad_habits_effect_table = """ CREATE TABLE IF NOT EXISTS tblBadHabitsEffect  (
                                            bad_habits_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            bad_habits_id integer NOT NULL,
                                            how_mucha_perday REAL NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_symptom_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailySymptom  (
                                            patient_daily_symptom_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            symptom_id integer NOT NULL,
                                            measure integer NOT NULL,
                                            symptom_days integer NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # effect age in month
        symptom_effect_table = """ CREATE TABLE IF NOT EXISTS tblSymptomEffect  (
                                            symptom_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            symptom_id integer NOT NULL,
                                            measure integer NOT NULL, 
                                            symptom_days REAL NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        urine_info_table = """ CREATE TABLE IF NOT EXISTS tblUrineInfo  (
                                            urine_info_id serial PRIMARY KEY, 
                                            urine_info text NOT NULL, 
                                            normal bool NOT NULL,  
                                            status bool NOT NULL
                                        ); """

        patient_daily_urine_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyUrine  (
                                            patient_daily_urine_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            urine_info_id integer NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        urine_effect_table = """ CREATE TABLE IF NOT EXISTS tblUrineEffect  (
                                            urine_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            urine_info_id integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

                                        
        stool_info_table = """ CREATE TABLE IF NOT EXISTS tblStoolInfo  (
                                            stool_info_id serial PRIMARY KEY, 
                                            stool_info text NOT NULL, 
                                            normal bool NOT NULL,  
                                            status bool NOT NULL
                                        ); """

        patient_daily_stool_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyStool  (
                                            patient_daily_stool_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            stool_info_id integer NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        stool_effect_table = """ CREATE TABLE IF NOT EXISTS tblStoolEffect  (
                                            stool_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            stool_info_id integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        weight_height_child_graph_table = """ CREATE TABLE IF NOT EXISTS tblWeightHeightChildGraph  (
                                            weight_height_child_graph_id serial PRIMARY KEY,                                  
                                            gender bool NOT NULL, 
                                            age REAL NOT NULL,   
                                            weight REAL NOT NULL,  
                                            height REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        weight_height_adult_graph_table = """ CREATE TABLE IF NOT EXISTS tblWeightHeightAdultGraph  (
                                            weight_height_adult_graph_id serial PRIMARY KEY,                                  
                                            gender bool NOT NULL,  
                                            height REAL NOT NULL,
                                            from_weight REAL NOT NULL,
                                            to_weight REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_weight_height_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyWeightHeight  (
                                            patient_daily_weight_height_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            weight REAL NOT NULL,  
                                            height REAL NOT NULL,    
                                            bmi REAL NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # effective_value_under=1,effective_value_over=0.3
        weight_height_effect_table = """ CREATE TABLE IF NOT EXISTS tblWeightHeightEffect  (
                                            weight_height_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,   
                                            height REAL NOT NULL, 
                                            healthy_bmi REAL NOT NULL,  
                                            under_weight_bmi REAL NOT NULL,
                                            over_weight_bmi REAL NOT NULL, 
                                            obese_bmi REAL NOT NULL, 
                                            extremely_obese_bmi REAL NOT NULL,
                                            effective_value_under REAL NOT NULL,
                                            effective_value_over REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_walk_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyWalk  (
                                            patient_daily_walk_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            walking_minutes REAL NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            report_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        walk_effect_table = """ CREATE TABLE IF NOT EXISTS tblWalkEffect  (
                                            walk_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            walk_hour integer NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_sleep_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailySleep  (
                                            patient_daily_sleep_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            sleeping_minutes REAL NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            report_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        sleep_effect_table = """ CREATE TABLE IF NOT EXISTS tblSleepEffect  (
                                            sleep_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            sleep_hour integer NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        tension_table = """ CREATE TABLE IF NOT EXISTS tblTension  (
                                            tension_id serial PRIMARY KEY,                                  
                                            tension text NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        patient_daily_tension_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyTension  (
                                            patient_daily_tension_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            tension_id integer NOT NULL,    
                                            tension_level integer NOT NULL,
                                            effective_value REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        tension_effect_table = """ CREATE TABLE IF NOT EXISTS tblTensionEffect  (
                                            tension_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            tension_id integer NOT NULL,    
                                            tension_level integer NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        eating_method_table = """ CREATE TABLE IF NOT EXISTS tblEatingMethod   (
                                            eating_method_id serial PRIMARY KEY,                                  
                                            eating_method text NOT NULL,                                   
                                            side_effect text NOT NULL, 
                                            effective_value REAL NOT NULL,  
                                            status bool NOT NULL
                                        ); """ 

        patient_daily_eating_method_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyEatingMethod  (
                                            patient_daily_eating_method_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,    
                                            eating_method_id integer NOT NULL,  
                                            effective_value REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        water_effect_table = """ CREATE TABLE IF NOT EXISTS tblWaterEffect  (
                                            water_effect_id serial PRIMARY KEY, 
                                            from_age integer NOT NULL,  
                                            to_age integer NOT NULL,   
                                            gender bool NOT NULL,  
                                            water REAL NOT NULL,
                                            effective_value REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_water_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyWater  (
                                            patient_daily_water_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL, 
                                            water REAL NOT NULL,
                                            effective_value REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        patient_daily_food_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyFood  (
                                            patient_daily_food_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,
                                            cooking_food_id integer NOT NULL,
                                            food_amount REAL NOT NULL, 
                                            healthy_point REAL NOT NULL, 
                                            eating_date REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 
        
        patient_daily_food_element_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyFoodElement  (
                                            patient_daily_food_element_id serial PRIMARY KEY, 
                                            patient_daily_visit_id integer NOT NULL,  
                                            food_element_id integer NOT NULL,  
                                            amount REAL NOT NULL, 
                                            taken_date REAL NOT NULL,  
                                            status bool NOT NULL
                                        ); """

        patient_daily_exercise_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyExercise  (
                                            patient_daily_exercise_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,
                                            exercise_rx_id integer NOT NULL,
                                            exercise_done REAL NOT NULL,
                                            exercise_date REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 

        patient_daily_extend_table = """ CREATE TABLE IF NOT EXISTS tblPatientDailyExtend  (
                                            patient_daily_extend_id serial PRIMARY KEY,                                  
                                            patient_daily_visit_id integer NOT NULL,
                                            extend_rx_id integer NOT NULL,
                                            extend_done REAL NOT NULL, 
                                            extend_date REAL NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """ 


                                         
        #............Food Elements ..............




        food_session_table = """ CREATE TABLE IF NOT EXISTS tblFoodSession (
                                            food_session_id serial PRIMARY KEY,
                                            session_name text NOT NULL,                                            
                                            start_month integer NOT NULL,                                            
                                            end_month integer NOT NULL,
                                            status bool NOT NULL
                                        ); """


        food_type_table = """ CREATE TABLE IF NOT EXISTS tblFoodType (
                                            food_type_id serial PRIMARY KEY,
                                            food_type text NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # price per kg/pice/litter  local_food=1 means it's get localy
        food_table = """ CREATE TABLE IF NOT EXISTS tblFood (
                                            food_id serial PRIMARY KEY,
                                            food_type_id integer NOT NULL,
                                            food text NOT NULL,
                                            about_food text NOT NULL,
                                            avg_price REAL,                                            
                                            food_session_id integer NOT NULL,
                                            local_food bool NOT NULL,
                                            food_image_url text NOT NULL,
                                            status bool NOT NULL
                                        ); """
                                        
        food_element_table = """ CREATE TABLE IF NOT EXISTS tblFoodElement (
                                            food_element_id serial PRIMARY KEY,
                                            food_element text NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        # disease wise food element


        
        food_element_disease_wise_take_table = """ CREATE TABLE IF NOT EXISTS tblFoodElementDiseaseWiseTake (
                                            food_element_disease_wise_take_id serial PRIMARY KEY,
                                            disease_id integer NOT NULL,
                                            food_element_id integer NOT NULL,
                                            min_amount REAL, 
                                            max_amount REAL, 
                                            status bool NOT NULL
                                        ); """

        food_element_disease_wise_avoid_table = """ CREATE TABLE IF NOT EXISTS tblFoodElementDiseaseWiseAvoid (
                                            food_element_disease_wise_avoid_id serial PRIMARY KEY,
                                            disease_id integer NOT NULL,
                                            food_element_id integer NOT NULL,
                                            max_amount REAL, 
                                            status bool NOT NULL
                                        ); """ 


        food_element_dependence_table = """ CREATE TABLE IF NOT EXISTS tblFoodElementDependence (
                                            food_element_dependence_id serial PRIMARY KEY,
                                            food_element_id integer NOT NULL,
                                            depend_food_element_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """

        food_element_antonomus_table = """ CREATE TABLE IF NOT EXISTS tblFoodElementAntonomus (
                                            food_element_antonomus_id serial PRIMARY KEY,
                                            food_element_id integer NOT NULL,
                                            antonomus_food_element_id integer NOT NULL, 
                                            status bool NOT NULL
                                        ); """

        # quantity miligram
        food_nutrition_table = """ CREATE TABLE IF NOT EXISTS tblFoodNutrition  (
                                            food_nutrition_id serial PRIMARY KEY, 
                                            food_id integer NOT NULL,                                            
                                            food_element_id integer NOT NULL,
                                            food_quantity REAL NOT NULL,
                                            element_quantity REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # quantity miligram per day
        patient_nutrition_table = """ CREATE TABLE IF NOT EXISTS tblPatientNutrition  (
                                            patient_nutrition_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,                                            
                                            food_element_id integer NOT NULL,
                                            min_quantity REAL NOT NULL,      
                                            max_quantity REAL NOT NULL,                                            
                                            how_many_days integer NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # quantity_level miligram per day max can be taken
        patient_bad_nutrition_table = """ CREATE TABLE IF NOT EXISTS tblPatientBadNutrition  (
                                            patient_bad_nutrition_id serial PRIMARY KEY, 
                                            patient_id integer NOT NULL,                                            
                                            food_element_id integer NOT NULL,
                                            quantity_level REAL NOT NULL,                                            
                                            how_many_days integer NOT NULL,  
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        
        food_processing_table = """ CREATE TABLE IF NOT EXISTS tblFoodProcessing  (
                                            food_processing_id serial PRIMARY KEY, 
                                            food_processing text NOT NULL,                                     
                                            process_point integer NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        cooking_food_table = """ CREATE TABLE IF NOT EXISTS tblCookingFood  (
                                            cooking_food_id serial PRIMARY KEY, 
                                            titile_food text NOT NULL,                                     
                                            food_processing_id integer NOT NULL,   
                                            cooking_food_amount REAL NOT NULL, 
                                            healthy_point REAL NOT NULL,                                    
                                            number_of_peoples integer NOT NULL,                                   
                                            eating_family_id integer NOT NULL,
                                            have_change bool NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        cooking_food_iteam_table = """ CREATE TABLE IF NOT EXISTS tblCookingFoodIteam  (
                                            cooking_food_iteam_id serial PRIMARY KEY, 
                                            cooking_food_id integer NOT NULL,  
                                            food_id integer NOT NULL,  
                                            amount REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        cooking_food_element_table = """ CREATE TABLE IF NOT EXISTS tblCookingFoodElement  (
                                            cooking_food_element_id serial PRIMARY KEY, 
                                            cooking_food_id integer NOT NULL,  
                                            food_element_id integer NOT NULL, 
                                            food_element_amount REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """  

        eating_family_table = """ CREATE TABLE IF NOT EXISTS tblEatingFamily (
                                            eating_family_id serial PRIMARY KEY,
                                            status bool NOT NULL
                                        ); """ 

        family_member_table = """ CREATE TABLE IF NOT EXISTS tblFamilyMember (
                                            family_member_id serial PRIMARY KEY, 
                                            eating_family_id integer NOT NULL, 
                                            patient_id integer NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """

        # Non registered patient fees for Duty Doctor (MBBS) 100 1
        # Non registered patient fees for Examine Doctor (DMF) 50 2
        # Appointment report print 30 3
        # Daily care charge 30 4
        # Diabetes test fees 25 5 

        daily_care_charge_table = """ CREATE TABLE IF NOT EXISTS tblDailyCareCharge  (
                                            daily_care_charge_id serial PRIMARY KEY,  
                                            about_charge text NOT NULL,         
                                            daily_care_charge integer NOT NULL,         
                                            charge_type integer NOT NULL,
                                            active_date REAL NOT NULL,
                                            stop_date REAL NOT NULL,
                                            create_date REAL NOT NULL,
                                            status bool NOT NULL
                                        ); """





        # tblDistrict..........
        district_table = """ CREATE TABLE IF NOT EXISTS tblDistrict (
                                            district_id serial PRIMARY KEY,
                                            district text NOT NULL UNIQUE,
                                            status bool NOT NULL
                                        ); """
        
        # tblThana..........
        thana_table = """ CREATE TABLE IF NOT EXISTS tblThana (
                                            thana_id serial PRIMARY KEY,                                            
                                            district_id integer NOT NULL,
                                            thana text NOT NULL,                                            
                                            longitude float NOT NULL,                                            
                                            latitude float NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        # tblThana..........
        village_table = """ CREATE TABLE IF NOT EXISTS tblVillage (
                                            village_id serial PRIMARY KEY,                                            
                                            thana_id integer NOT NULL,
                                            village text NOT NULL,                                            
                                            longitude float NOT NULL,                                            
                                            latitude float NOT NULL,                                           
                                            user_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """
        
        # tblThana..........
        mahalla_table = """ CREATE TABLE IF NOT EXISTS tblMahalla (
                                            mahalla_id serial PRIMARY KEY,                                            
                                            village_id integer NOT NULL,
                                            mahalla text NOT NULL,                                            
                                            longitude float NOT NULL,                                            
                                            latitude float NOT NULL,                                          
                                            user_id integer NOT NULL,
                                            status bool NOT NULL
                                        ); """



        if self.conn is not None:        
            # create person info table 
                   
 
            # self.drop_table("tblPatientDailyExercise")
            # self.drop_table("tblPatientTreatment")
            # self.drop_table("tblPrescription")
            # self.drop_table("tblDiabetesTestFeesCollection")
            # self.drop_table("tblDailyCareFeeCollection")
            # self.drop_table("tblPatientDailyFood")
            # self.drop_table("tblPatientDailyMedicine")
            # self.drop_table("tblDoctorJoining")
            # self.drop_table("tblDoctor")
            # self.drop_table("tblMedicine")
            # self.drop_table("tblMedicineDosageForms")
            # self.drop_table("tblCarePackage")
            # self.drop_table("tblCareRegistration")
            # self.drop_table("tblMedicineRx")
            
            

            self.create_table(help_question_table)
            self.create_table(district_table)
            self.create_table(thana_table)
            self.create_table(village_table)
            self.create_table(mahalla_table)
            self.create_table(user_table)
            self.create_table(admin_table)
            self.create_table(doctor_specialty_table)
            self.create_table(doctor_degree_table)

            self.create_table(account_balance_table) 

            self.create_table(user_bank_account_table)
            self.create_table(payment_request_table)
            self.create_table(received_money_table)
            self.create_table(pay_doctor_fee_table)
            self.create_table(withdrawal_request_table)
            self.create_table(withdrawal_money_table)

            self.create_table(doctor_table)
            self.create_table(doctor_joining_table)
            self.create_table(doctor_query_table)
            self.create_table(doctor_visiting_session_table)
            self.create_table(visiting_place_table)
            self.create_table(patient_table)
            self.create_table(patient_connection_table) 
            self.create_table(patient_covid_test_table)
            self.create_table(doctor_appointment_table)
            self.create_table(rx_history_table)
            self.create_table(report_history_table)
            self.create_table(patient_treatment_table)
            self.create_table(prescription_backup_table)
            self.create_table(treatment_result_msg_table)
            self.create_table(patient_treatment_result_table)
            self.create_table(public_treatment_table)
            self.create_table(treatment_start_table)
            self.create_table(symptom_table)
            self.create_table(disease_table)
            # self.create_table(symptom_group_table)
            self.create_table(patient_symptom_group_save_table);

            self.create_table(vaccine_table)
            self.create_table(vaccine_history_table)
            self.create_table(disease_identify_table)
            self.create_table(disease_identify_rx_group_table)
            
            self.create_table(previous_disease_table)
            self.create_table(patient_symptom_table)                                      
            self.create_table(previous_disease_group_table)

            self.create_table(primary_test_table)
            self.create_table(patient_dptr_table)

            
            self.create_table(medicine_rx_table)
            self.create_table(medicine_extra_guide_table)

            self.create_table(nutrition_rx_table)
            self.create_table(nutrition_rx_group_table)
            self.create_table(bad_nutrition_rx_table)
            self.create_table(bad_nutrition_rx_group_table)


            self.create_table(chief_complaints_table)
            self.create_table(chief_complaints_rx_group_table)
            self.create_table(on_examination_table)
            self.create_table(on_examination_rx_group_table)

            self.create_table(extend_rx_table)

            self.create_table(reminded_rx_table)

            self.create_table(outside_rx_table)

            self.create_table(medicine_rx_group_table)
            self.create_table(exercise_rx_group_table)
            self.create_table(extend_rx_group_table)

            self.create_table(lab_test_rx_group_table)
            self.create_table(patient_lab_test_report_url_table)
            self.create_table(patient_lab_test_report_table)
            self.create_table(lab_test_comment_table)
            self.create_table(lab_test_report_table)

            self.create_table(prescription_table)
            
            self.create_table(reminded_rx_group_table)


            self.create_table(patient_test_report_table)
              
            self.create_table(daily_care_center_table)
            self.create_table(about_cost_table)
            self.create_table(daily_care_center_cost_table)
            self.create_table(employee_application_table)                   
            self.create_table(employee_table)            
            self.create_table(employee_designation_table)
            self.create_table(employee_designation_grade_table) 
            self.create_table(employee_posting_table)
            self.create_table(employee_querymsg_table)
            self.create_table(employee_duty_table) 
            self.create_table(daily_care_fee_collection_table)
            self.create_table(diabetes_test_fees_collection_table)
         
    
            self.create_table(covid_hospital_table)
            self.create_table(movement_location_table)            
            
            self.create_table(notification_table) 

            self.create_table(medicine_dosage_forms_table)
            self.create_table(medicine_table)
            self.create_table(daily_schedule_table)  
            self.create_table(befor_eating_table)

            self.create_table(chief_complaints_prescription_table)  
            self.create_table(on_examination_prescription_table)
            self.create_table(disease_identify_prescription_table)  
            self.create_table(lab_test_prescription_table)  
            self.create_table(medicine_prescription_table)  
            self.create_table(nutrition_prescription_table)  
            self.create_table(nutrition_prescription_table)  
            self.create_table(bad_nutrition_prescription_table)  
            self.create_table(exercise_prescription_table)  
            self.create_table(exercise_prescription_table)  
            self.create_table(extend_prescription_table)

            
            self.create_table(food_element_table)
            self.create_table(food_nutrition_table)
            self.create_table(food_session_table)
            self.create_table(food_type_table)
            self.create_table(food_table)
            self.create_table(food_processing_table)
            self.create_table(cooking_food_table)
            self.create_table(cooking_food_element_table)
            self.create_table(eating_family_table)
            self.create_table(family_member_table)
            self.create_table(cooking_food_iteam_table)
            self.create_table(patient_daily_food_table)
            self.create_table(patient_daily_food_element_table) 
            self.create_table(patient_daily_exercise_table) 
            self.create_table(patient_daily_extend_table) 
            self.create_table(patient_nutrition_table)
            self.create_table(patient_bad_nutrition_table)
            self.create_table(food_element_dependence_table)
            self.create_table(food_element_antonomus_table)
            self.create_table(food_element_disease_wise_take_table)
            self.create_table(food_element_disease_wise_avoid_table)
            self.create_table(exercise_table) 
            self.create_table(exercise_schedule_table)
            self.create_table(exercise_rx_table)
            self.create_table(extend_table)

            self.create_table(doctor_message_table)

            self.create_table(body_area_table)
            self.create_table(body_part_table)

            self.create_table(care_package_table)
            # self.create_table(health_condition_table)    
            self.create_table(care_registration_table)
            self.create_table(daily_care_report_public_acces_table)
            self.create_table(care_bill_collection_table)
            self.create_table(doctor_fees_collection_table)
            self.create_table(about_transaction_table)
            self.create_table(collection_from_employee_table)

            self.create_table(occupation_table)
            self.create_table(education_table)
            self.create_table(religious_table)
            self.create_table(hobbies_table)
            self.create_table(social_history_table)
            self.create_table(medicine_reaction_table)
            self.create_table(medication_allergies_table)
            self.create_table(surgical_table)
            self.create_table(surgical_history_table)
            self.create_table(injuries_table)
            self.create_table(injuries_history_table)
            self.create_table(medical_history_table)
            self.create_table(medications_history_table)
            self.create_table(family_table)
            self.create_table(family_history_table)
            self.create_table(misbehavior_table)
            self.create_table(ever_misbehavior_history_table)
            self.create_table(delivery_mode_table)
            self.create_table(baby_condition_table)
            self.create_table(patient_pregnancy_history_table)
            self.create_table(patient_delivery_history_table)
            self.create_table(child_development_table)
            self.create_table(child_development_history_table)
            self.create_table(child_sensory_concerns_table)
            self.create_table(child_sensory_concerns_history_table)
            self.create_table(temperament_table)
            self.create_table(temperament_history_table)
            self.create_table(patient_good_habits_history_table)
            self.create_table(patient_bad_habits_history_table) 

            self.create_table(menstrual_table)
            self.create_table(menstrual_history_table)
            self.create_table(travel_table)
            self.create_table(travel_history_table)
            self.create_table(birth_table)
            self.create_table(birth_history_table)
            self.create_table(feeding_table)
            self.create_table(feeding_history_table)

            self.create_table(allergy_substance_table)
            self.create_table(allergy_reaction_table)
            self.create_table(allergy_history_table)           

            self.create_table(general_examination_table)
            self.create_table(examination_report_table)
            self.create_table(patient_examination_report_table)
            self.create_table(general_diagnosis_data_table)
            self.create_table(systemic_examination_table)
            self.create_table(systemic_examination_datas_table)
            self.create_table(lab_test_table)
            self.create_table(lab_test_report_history_table) 
            self.create_table(general_examination_datas_table)
            self.create_table(systemic_diagnosis_data_table)
            self.create_table(patient_appointment_table)
            self.create_table(change_examine_doctor_table)
            self.create_table(patient_daily_medicine_table)
            self.create_table(daily_data_topic_table)   
            self.create_table(patient_daily_visit_table)   
            self.create_table(patient_daily_pulse_table)   
            self.create_table(patient_daily_oxygen_saturation_table)   
            self.create_table(patient_daily_temparature_table)   
            self.create_table(patient_daily_taken_food_table)   
            self.create_table(workload_table)   
            self.create_table(patient_daily_workload_table) 
            self.create_table(good_habits_table)
            self.create_table(patient_daily_good_habits_table)
            self.create_table(bad_habits_table)
            self.create_table(patient_daily_bad_habits_table)
            self.create_table(patient_daily_symptom_table)   
            self.create_table(urine_info_table)   
            self.create_table(patient_daily_urine_table)   
            self.create_table(stool_info_table)   
            self.create_table(patient_daily_stool_table)   
            self.create_table(weight_height_child_graph_table)    
            self.create_table(weight_height_adult_graph_table)   
            self.create_table(patient_daily_weight_height_table)   
            self.create_table(patient_daily_walk_table) 
            self.create_table(patient_daily_sleep_table)   
            self.create_table(tension_table)
            self.create_table(eating_method_table)
            self.create_table(patient_daily_eating_method_table)
            self.create_table(water_effect_table) 
            self.create_table(patient_daily_water_table)  
            self.create_table(patient_daily_tension_table) 
            self.create_table(daily_visit_comments_table)   
            self.create_table(patient_daily_blood_sugar_table)   
            self.create_table(blood_sugar_test_type_table)   
            self.create_table(patient_daily_bp_table)    
            self.create_table(monitoring_doctor_response_table)   
            self.create_table(doctor_response_table)
            self.create_table(examin_doctor_table)
            self.create_table(duty_doctor_table)
            self.create_table(daily_care_doctor_table)
            self.create_table(health_worker_table)


            self.create_table(pulse_effect_table)   
            self.create_table(oxygen_saturation_effect_table)   
            self.create_table(temparature_effect_table)   
            self.create_table(food_effect_table) 
            self.create_table(Workload_effect_table)   
            self.create_table(good_habits_effect_table)   
            self.create_table(bad_habits_effect_table)   
            self.create_table(symptom_effect_table)   
            self.create_table(urine_effect_table)   
            self.create_table(stool_effect_table)     
            self.create_table(weight_height_effect_table)   
            self.create_table(walk_effect_table)  
            self.create_table(sleep_effect_table)
            self.create_table(tension_effect_table) 
            self.create_table(blood_sugar_effect_table)  
            self.create_table(bp_effect_table)
            self.create_table(daily_care_charge_table)

            


        else:
            print("Error! cannot create the database connection.")

    