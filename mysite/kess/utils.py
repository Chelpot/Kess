from .models import Tile
from datetime import datetime

def log_user_action(request, current_user, action="a fait quelque chose"):
    if not current_user.is_staff:
        tile_event = Tile()
        tile_event.name = current_user.name
        tile_event.time = datetime.strftime(datetime.now(), '%H:%M %d %b %Y')
        tile_event.avatar = current_user.avatar
        tile_event.action = action
        tile_event.save()


def is_ascii(s):
    if not all(ord(c) < 255 for c in s):
        raise ValidationError("Charactère(s) interdit(s) dans le pseudo, veuillez en choisir un autre")
