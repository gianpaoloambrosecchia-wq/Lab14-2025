from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct s.*
                from stores s  """

        cursor.execute(query)

        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct o.*
                from orders o
                where o.store_id = %s """

        cursor.execute(query, (store.store_id,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select o1.order_id as o1, o2.order_id as o2, o1.quan + o2.quan as peso
                from (select o.order_id, o.order_date,sum(oi.quantity) as quan
                from orders o
                join order_items oi on oi.order_id = o.order_id 
                where o.store_id = %s
                group by o.order_id) o1
                join (select o.order_id, o.order_date,sum(oi.quantity) as quan
                from orders o
                join order_items oi on oi.order_id = o.order_id 
                where o.store_id = %s
                group by o.order_id) o2 on o1.order_date > o2.order_date
                where abs(datediff(o1.order_date, o2.order_date)) < %s
                group by o1.order_id, o2.order_id """

        cursor.execute(query, (store.store_id, store.store_id, k))

        for row in cursor:
            result.append((
                idMap[row["o1"]],
                idMap[row["o2"]],
                row["peso"]
            ))

        cursor.close()
        conn.close()
        return result