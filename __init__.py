from health_tracker import HitPoints
from opsdroid.matchers import match_regex
import collections as col

def setup(opsdroid):
    logging.debug("Loaded health tracking module")


class Characters(col.UserDict):
    """
    https://gist.github.com/Integralist/f790b21acc5fa178830f060f649a04c4

    TODO: get some things sorted wrt to calling the attributes from
    the database

    """

    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
       super().__setitem__(key, HitPoints(value))

    def get_characters(self):
        for i, name in self.items():
            print(i, name.get_points())

Chars = Characters()

@match_regex(r'create character (?P<char_name>\d+) (?P<hit_point>\d+)')
async def create_character(opsdriod, config, message):
    match = message.regex
    char_name = match.group('char_name')
    hit_point = match.group('hit_point')
    Chars.__setitem__(char_name, hit_point)


@match_regex('print characters')
async  def print_characters(opsdroid, config, message):
    await message.respond(Chars.get_characters())
