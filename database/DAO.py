from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getRatings():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating 
                    from ratings r 
                    order by r.avg_rating DESC
                    """
        cursor.execute(query)

        for row in cursor:
            result.append((row["avg_rating"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodiA(r1, r2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.*
                    from names n, role_mapping rm, movie m, ratings r 
                    where n.id = rm.name_id 
                    and rm.movie_id = m.id 
                    and m.id = r.movie_id 
                    and r.avg_rating BETWEEN %s and %s
                    and n.date_of_birth is not null
                                        """
        cursor.execute(query, (r1, r2, ))

        for row in cursor:
            result.append(Attore(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(r1, r2, mappaA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.a1, t1.a2, m.worlwide_gross_income as income
                    from (select rm1.name_id as a1, rm2. name_id as a2, rm1.movie_id 
                    from role_mapping rm1, role_mapping rm2
                    where rm1.movie_id = rm2.movie_id 
                    and rm1.name_id > rm2.name_id ) as t1, movie m, ratings r
                    where t1.movie_id = m.id 
                    and m.id = r.movie_id 
                    and r.avg_rating BETWEEN %s and %s
                    and m.worlwide_gross_income is not null
                                                            """
        cursor.execute(query, (r1, r2, ))

        for row in cursor:
            if row["a1"] in mappaA and row["a2"] in mappaA:
                a1 = mappaA[row["a1"]]
                a2 = mappaA[row["a2"]]
                result.append((a1, a2, row["income"]))

        cursor.close()
        conn.close()
        return result

