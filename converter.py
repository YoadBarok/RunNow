import math


class Converter:

    def __init__(self, distance, time):
        self.distance = distance
        self.time = time

    def convert_to_speed(self):
        speed = round((self.distance / self.time) * 60, 2)
        return speed

    def convert_to_pace(self):
        pace_in_seconds = (self.time * 60) / self.distance
        pace_tuple = divmod(pace_in_seconds, 60)
        if math.floor(pace_tuple[1]) < 10:
            output_pace = f"{math.floor(pace_tuple[0])}:0{math.floor(pace_tuple[1])}"
        else:
            output_pace = f"{math.floor(pace_tuple[0])}:{math.floor(pace_tuple[1])}"
        return output_pace

    @staticmethod
    def convert_to_seconds(time):
        minutes = float(time.split(":")[0])
        seconds = float(time.split(":")[1])
        total_seconds = minutes * 60 + seconds
        return total_seconds
