def set_name(self, match, user_data=None):
    self.name = match.group(1)
    return f"Приятно познакомиться, {self.name}!"