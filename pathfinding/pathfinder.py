import os
import json
import heapq
import logging
from typing import Union
import pandas as pd


class PathFinder:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Chemins vers les fichiers de données
    # TIME_TABLE_PATH = "C:/Users/33758/Documents/Projects/T-AIA-901/backend/path_finder/data/timetables_formatted.csv"
    TIME_TABLE_PATH = os.path.join(BASE_DIR, "data", "timetables_formatted.csv")
    GRAPH_PATH = os.path.join(BASE_DIR, "data", "graph.json")
    STATIONS_CITIES_PATH = os.path.join(BASE_DIR, "data", "stations_cities.csv")

    @staticmethod
    def check_data_exists() -> None:
        if not os.path.exists(PathFinder.TIME_TABLE_PATH):
            raise FileNotFoundError("timetables_formatted.csv is missing")

        if not os.path.exists(PathFinder.GRAPH_PATH):
            PathFinder.generate_graph()

    @staticmethod
    def generate_graph() -> None:
        # Load the timetable csv
        # df = pd.read_csv(PathFinder.TIME_TABLE_PATH, sep="\t", encoding="ISO-8859-1")
        df = pd.read_csv(PathFinder.TIME_TABLE_PATH, sep="\t", encoding="utf-8")

        # Build the graph
        graph = {}

        for index, row in df.iterrows():
            # We add the stations to the graph if they are not already in it and add a key for the other station
            # with the duration as value
            if row["gare_a_city"] not in graph:
                graph[row["gare_a_city"]] = {}
            graph[row["gare_a_city"]][row["gare_b_city"]] = row["duree"]

            if row["gare_b_city"] not in graph:
                graph[row["gare_b_city"]] = {}
            graph[row["gare_b_city"]][row["gare_a_city"]] = row["duree"]

        try:
            # Save the graph
            with open(PathFinder.GRAPH_PATH, "w", encoding="utf-8") as f:
                json.dump(graph, f, ensure_ascii=False, indent=4)
        except IOError:
            raise IOError("Unable to write the graph to file")

    @staticmethod
    def generate_station_city_csv() -> None:
        # Load the timetable csv
        df = pd.read_csv(PathFinder.TIME_TABLE_PATH, sep="\t", encoding="ISO-8859-1")

        # Isolate gare_a_city with gare_a and gare_b_city with gare_b into two different dataframes
        df_a = df[["gare_a", "gare_a_city"]]
        df_b = df[["gare_b", "gare_b_city"]]

        # gare_a and gare_b must be uppercase
        df_a.loc[:, "gare_a"] = df_a["gare_a"].str.upper()
        df_b.loc[:, "gare_b"] = df_b["gare_b"].str.upper()

        # Combine the two dataframes into one with columns gare and city
        df_a.columns = ["gare", "city"]
        df_b.columns = ["gare", "city"]
        df_c = pd.concat([df_a, df_b])

        # Remove duplicates
        df_c = df_c.drop_duplicates()

        # Save the dataframe to csv
        df_c.to_csv(PathFinder.STATIONS_CITIES_PATH, sep=";", index=False)

    @staticmethod
    def get_graph() -> dict:
        with open(PathFinder.GRAPH_PATH, "r") as f:
            graph = json.load(f)
        return graph

    @staticmethod
    def generate_response_dict(
        path: list = None,
        duration_between_stations: list = None,
        total_duration: int = 0,
    ) -> dict:
        response_dict = {
            "path": path if path else [],
            "departure": path[0] if path else None,
            "arrival": path[-1] if path else None,
            "duration_between_stations": (
                duration_between_stations if duration_between_stations else []
            ),
            "total_duration": total_duration,
        }
        return response_dict

    @staticmethod
    def compute_shortest_path(graph: dict, start: str, end: str) -> dict | None:
        # Set the distance to all stations to infinity
        distances = {station: float("inf") for station in graph}

        # Distance from the start to itself is 0
        distances[start] = 0

        # We set the priority queue with the start station
        priority_queue = [(0, start)]

        # Create a dictionary to stortr(e)e the previous station in the path
        previous_station = {station: None for station in graph}

        while priority_queue:
            # Pop the station with the shortest distance from the heap, so we consider it first
            current_distance, current_station = heapq.heappop(priority_queue)

            # If the current station is the destination, return the shortest distance
            if current_station == end:
                path = []
                duration_between_stations = []
                while current_station is not None:
                    path.append(current_station)
                    previous = previous_station[current_station]
                    if previous:
                        duration_between_stations.append(
                            graph[current_station][previous]
                        )
                    current_station = previous_station[current_station]
                path.reverse()
                duration_between_stations.reverse()
                return PathFinder.generate_response_dict(
                    path, duration_between_stations, distances[end]
                )

            # Skip if the current station is already visited
            if current_distance > distances[current_station]:
                continue

            # Explore neighbors
            for neighbor, weight in graph[current_station].items():
                distance = current_distance + weight

                # If a shorter path is found, update the distance and add to the priority queue
                if distance < distances[neighbor]:
                    # The fastest way to reach the neighbor is from the current station, so we just assign
                    # the distance to the current_station + the weight of the edge between the current station
                    # and the neighbor to the neighbor
                    distances[neighbor] = distance
                    previous_station[neighbor] = current_station
                    # We add the neighbor to the priority queue with the distance as priority
                    # It means that the neighbor will be explored before the other stations if the distance is shorter
                    # than the other stations
                    heapq.heappush(priority_queue, (distance, neighbor))

        # If no path is found, return empty dict
        return PathFinder.generate_response_dict(["UNKNOWN"])

    @staticmethod
    def minutes_to_hours(minutes: int) -> str:
        return f"{minutes} minutes"

    @staticmethod
    def check_alternative(city: str) -> str:
        df = pd.read_csv(PathFinder.STATIONS_CITIES_PATH, sep=";", encoding="utf-8")

        df = df[df["gare"] == city]

        if df.empty:
            return city
        return df["city"].iloc[0]

    @staticmethod
    def get_shortest_path_between_cities(
        trip: list, empty_object_when_error: bool = True
    ) -> Union[list, None]:
        results = []

        try:
            PathFinder.check_data_exists()

            # Uppercase each word in the trip
            trip = [station.upper() for station in trip]

            # We want to send trip order by pair
            # ex: ["Nantes", "Lyon", "Paris"] -> [["Nantes", "Lyon"], ["Lyon", "Paris"]]
            trip_order = [trip[i : i + 2] for i in range(len(trip) - 1)]

            if len(trip_order) == 0:
                return (
                    [PathFinder.generate_response_dict(["UNKNOWN"])]
                    if empty_object_when_error
                    else None
                )

            for i, step in enumerate(trip_order):
                for city in step:

                    # If city name is not recognized based on graph's keys
                    if city not in PathFinder.get_graph():
                        # We look for an alternative in the train_stations.csv
                        if (alternative := PathFinder.check_alternative(city)) != city:
                            step[step.index(city)] = alternative
                        # If alternative is equal to the city name, we consider that we can't provide a path and
                        # return None (can be managed as an error then)
                        else:
                            return (
                                [PathFinder.generate_response_dict(["UNKNOWN"])]
                                if empty_object_when_error
                                else None
                            )

                results.append(
                    PathFinder.compute_shortest_path(
                        PathFinder.get_graph(), step[0], step[1]
                    )
                )

            return results
        except Exception as e:
            logging.error(f"{e} not found in the graph")
            return (
                [PathFinder.generate_response_dict(["UNKNOWN"])]
                if empty_object_when_error
                else None
            )
            
    """ 
    cette fonction a pour but de formater la response avec le chemin le plus court et ses correspondance
    """
    @staticmethod
    def format_response_nlp(shortest_path):
        # Vérifier si shortest_path est une liste non vide
        if shortest_path:
            # get path info
            path_info = shortest_path[0]
            # if no departure or no arrival
            if path_info["departure"] == "UNKNOWN" or path_info["arrival"] == "UNKNOWN" or path_info["total_duration"] == 0:
                return {"error": "Aucun chemin trouvé pour ce trajet. Veuillez recommencer."}
            # create clean dict
            formatted_response = {
                "departure": path_info["departure"],
                "arrival": path_info["arrival"],
                "total_duration": path_info["total_duration"],
                "steps": []
            }
            # for each step
            for i, station in enumerate(path_info["path"][:-1]):
                # create dict for step
                step = {
                    "from": station,
                    "to": path_info["path"][i + 1],
                    "duration": path_info["duration_between_stations"][i]
                }
                # push to steps array
                formatted_response["steps"].append(step)

            return formatted_response
        else:
            # if shortest_path is empty
            return {"error": "Aucun chemin trouvé pour ce trajet. Veuillez recommencer."}


# Si le code est exécuté en tant que script principal, générez le graphique et le CSV des villes des stations
if __name__ == "__main__":
    PathFinder.generate_graph()
    PathFinder.generate_station_city_csv()

    # Exemple de voyage
    trip = ["paris", "marseille"]

    # Obtenez le chemin le plus court
    shortest_paths = PathFinder.get_shortest_path_between_cities(trip)
    print("shortest_paths")
    
    # Formater la réponse au format JSON
    formatted_response = PathFinder.format_response_nlp(shortest_paths)
    # Imprimer ou renvoyer la réponse formatée
    print(formatted_response)
        
    # keys = shortest_paths.keys()
    # print(keys)

    # print(shortest_paths)

    # Affichez le chemin le plus court
    for i, path in enumerate(shortest_paths):
        formatted_durations = [
            f"{duration} minutes" for duration in path["duration_between_stations"]
        ]
        print(
            f"Shortest path between {path['departure']} and {path['arrival']}: {[station for station in path['path']]} with total duration {path['total_duration']} minutes"
        )

        for j, city in enumerate(path["path"][:-1]):
            print(f"{city} - {path['path'][j+1]}: {formatted_durations[j]}")
        print()
