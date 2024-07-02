from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct Country
                    from go_retailers
                    order by Country asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailersInCountry(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from go_retailers
                    where Country = %s
                    order by Retailer_name asc"""

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdges(year, country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select count(distinct ds1.Product_number) as n, r1.Retailer_code as retailer1, r2.Retailer_code as retailer2
                    from go_sales.go_retailers r1, go_sales.go_daily_sales ds1, go_sales.go_retailers r2, go_sales.go_daily_sales ds2 
                    where YEAR(ds1.Date)=%s and YEAR(ds2.Date)=%s and r1.Country=%s and r2.Country=%s
                    and r1.Retailer_code=ds1.Retailer_code and r2.Retailer_code=ds2.Retailer_code and r1.Retailer_code!=r2.Retailer_code
                    and ds1.Product_number=ds2.Product_number 
                    group by r1.Retailer_code, r2.Retailer_code"""

        cursor.execute(query, (year, year, country, country,))

        for row in cursor:
            result.append( (row["retailer1"], row["retailer2"], row["n"]) )
        print(result)

        cursor.close()
        conn.close()
        return result