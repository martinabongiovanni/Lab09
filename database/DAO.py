from database.DB_connect import DBConnect
from model.airline import Airline
from model.airport import Airport
from model.flight import Flight
from model.rotta import Rotta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM airports"
        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllFlights():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM flights"
        cursor.execute(query)

        for row in cursor:
            result.append(Flight(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllAirlines():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM airlines"
        cursor.execute(query)

        for row in cursor:
            result.append(Airline(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRotteV1():
        '''
        Legge le rotte dal db senza aggregare i voli opposti sulla stessa tratta.
        Quindi la lista risultante avrà una entry per i voli A->B e un'altra per B->A.
        '''
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                SELECT f.ORIGIN_AIRPORT_ID as a1, f.DESTINATION_AIRPORT_ID as a2, SUM(f.DISTANCE) as totDistance, COUNT(*) as nVoli 
                FROM extflightdelays.flights f 
                GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                """)
        cursor.execute(query)

        for row in cursor:
            result.append(Rotta(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRotteV2():
        '''
        Leggo le rotta dal db aggregando i voli opposti sulla stessa tratta.
        Nella query quindi effettuo un join di due tabelle temporanee.
        Effettuo dei check sui NULL per non escluderli, perché non tutte le rotte hanno voli in entrambe le direzioni.
        COALESCE permette nella sommatoria di considerare i NULL come zero.
        In questo modo quindi ottengo:
            1. L'informazione sulla direzione del volo (A→B o B→A):
                i voli vengono aggregati indipendentemente dal senso, quindi ottengo una sola riga per la coppia (A, B) con dati combinati di andata e ritorno.
            2. Il numero totale di voli tra due aeroporti, in entrambe le direzioni:
                nVoli = voli da A→B + voli da B→A
            3. La somma delle distanze percorse nei due sensi:
                totDistance = somma di tutte le distanze da A→B e da B→A
        '''
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                SELECT T1.ORIGIN_AIRPORT_ID as a1, T1.DESTINATION_AIRPORT_ID as a2, COALESCE(T1.D, 0) + COALESCE(T2.D, 0) as totDistance, COALESCE(T1.N, 0) + COALESCE(T2.N, 0) as nVoli
                FROM (SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, SUM(f.DISTANCE) as D, COUNT(*) as N
                        FROM extflightdelays.flights f
                        GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) 
                        T1 LEFT JOIN
                        (SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, SUM(f.DISTANCE) as D, COUNT(*) as N
                            FROM extflightdelays.flights f
                            GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) T2
                        ON T1.ORIGIN_AIRPORT_ID = T2.DESTINATION_AIRPORT_ID 
                                AND T2.ORIGIN_AIRPORT_ID = T1.DESTINATION_AIRPORT_ID
                WHERE T1.ORIGIN_AIRPORT_ID < T2.ORIGIN_AIRPORT_ID 
                        OR T2.ORIGIN_AIRPORT_ID IS NULL 
                        OR T2.DESTINATION_AIRPORT_ID IS NULL
                    """)
        cursor.execute(query)

        for row in cursor:
            result.append(Rotta(**row))

        cursor.close()
        conn.close()
        return result