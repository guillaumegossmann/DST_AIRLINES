from pymongo import MongoClient
from functions import FlightProcessor

# Connexion à MongoDB
client = MongoClient(host="localhost", port=27017, username="dstairlines", password="dstairlines")
db = client.app_data

flightprocessor = FlightProcessor()

def today_all_flights_append():
    # Requête API pour récupérer les vols "landed" (aviationstack)
    flight_info = flightprocessor.get_flights_landed()

    if flight_info and 'data' in flight_info:
        all_flights = flight_info['data']

        if all_flights:
            # Traiter la liste des vols et insérer dans la collection MongoDB
            result = flightprocessor.process_flight_AS_list(all_flights, db.all_flights)

            # Résumé des opérations
            print(f"{result['vols traités']} vols traités et insérés dans la base de données.")
            if result["vols échoués"]:
                print(f"{result['vols échoués']} vols ont échoué et n'ont pas été insérés.")

            return result
        else:
            return {"error": "Aucun vol trouvé.", "details": all_flights}, 404
    else:
        return {"error": "Aucun vol trouvé ou problème API AS", "details": flight_info}

today_all_flights_append()
