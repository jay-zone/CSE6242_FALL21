########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv

#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "mcampo6"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "create table movies (id integer, title  text, score real)"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "create table movie_cast (movie_id integer, cast_id integer, cast_name text, birthday text, popularity real)"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)


    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path, encoding='utf8') as csvfile:
            myfile = csv.reader(csvfile)
            movielist = list(myfile)
            for movie in movielist:
                connection.execute('INSERT INTO movies values (?,?,?)',(movie[0], movie[1],movie[2]))


       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path, encoding='utf8') as f:
            myf = csv.reader(f)
            moviecast_list = list(myf)
            for moviecast in moviecast_list:
                connection.execute('INSERT INTO movie_cast values(?,?,?,?,?)',(moviecast[0],moviecast[1],moviecast[2],moviecast[3],moviecast[4]))
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "create table cast_bio (cast_id integer, cast_name text, birthday text, popularity real)"
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = "insert into cast_bio select distinct cast_id, cast_name, birthday, popularity from movie_cast"
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "create index movie_index ON movies(id)"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "create index cast_index ON movie_cast(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "create index cast_bio_index ON cast_bio(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """select printf('%0.02f', (select count(id) from movies where score > 50 and title like '%war%')*1.0/((select count(id) from movies)/100.0))"""
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = """
        select 
        cast_name, count(movie_id)
        from movie_cast
        where popularity > 10
        group by cast_name
        order by count(movie_id) desc,cast_name
        limit 5   
        
        
        
        
        
        """
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """
        select
        title as movie_title, printf('%.2f',CAST(movies.score as FLOAT)), count(cast_id) as cast_count
        from movies
        inner join movie_cast on movie_cast.movie_id = movies.id
        group by movies.title
        order by cast(movies.score as FLOAT) desc,count(cast_id), movies.title
        limit 5
               
        """
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """
        select cast_id, cast_name, printf('%0.2f',avg(CAST(score as FLOAT))) as average_score
        from movie_cast
        inner join movies on movies.id = movie_cast.movie_id
        where movies.score >= 25
        group by movie_cast.cast_id
        having count(movie_id) > 2
        order by avg(cast(score as float)) desc, cast_name
        limit 10
       
        """
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """
        create view good_collaboration
        as
        select
        z.cast_id1 as cast_member_id1,
        z.cast_id2 as cast_member_id2,
        count(movies.id) as movie_count,
        printf('%0.2f', avg(cast(score as float))) as average_movie_score
        from
        ((
        select 
        cast_id as cast_id1, movie_id
        from movie_cast) as x 
        inner join
        (
        select 
        cast_id as cast_id2, movie_id
        from movie_cast) as y
        ON x.movie_id = y.movie_id) as z
        inner join movies
        ON movies.id = z.movie_id
        where z.cast_id1 > z.cast_id2
        group by 
        z.cast_id1, z.cast_id2
        having count(z.movie_id) > 2 and avg(cast(movies.score as float)) >=40
        
        """
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """
        select x.cast_id as cast_id, cast_bio.cast_name as cast_name,
        printf('%0.2f', avg(cast(x.collaboration_score as float))) as collaboration_score
        from 
        (select
        cast_member_id1 as cast_id,
        average_movie_score as collaboration_score
        from good_collaboration
        union all
        select
        cast_member_id2 as cast_id,
        average_movie_score as collaboration_score 
        from good_collaboration
        ) as x
        inner join cast_bio
        on cast_bio.cast_id = x.cast_id
        group by x.cast_id
        order by collaboration_score desc, cast_name
        limit 5
        
        
        
        """
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = """
        CREATE VIRTUAL TABLE movie_overview USING fts4(id INTEGER, overview TEXT)
        
        
        
        """
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path, encoding='utf8') as f:
            reader = csv.reader(f)
            text_list = list(reader)

            for text in text_list:
                connection.execute("INSERT INTO movie_overview(id, overview) VALUES(?, ?)",(text[0],text[1]))


        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = """SELECT COUNT(id) FROM movie_overview WHERE overview MATCH '"fight"';"""
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = """select count(id) from movie_overview where overview match '"space" NEAR/5 "program"';"""
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
