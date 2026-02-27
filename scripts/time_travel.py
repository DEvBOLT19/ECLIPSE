class TimeTravel:
    def __init__(self, current_map, past_map):
        self.current_map = current_map
        self.past_map = past_map
        self.is_in_past = False

    def switch_time(self):
        self.is_in_past = not self.is_in_past
        return self.past_map if self.is_in_past else self.current_map
