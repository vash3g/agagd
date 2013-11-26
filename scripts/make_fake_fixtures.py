# A simple script to generate fake data
import sys, random, json, hashlib

USAGE = 'Usage: python make_fake_fixtures.py [num_of_members] [num_of_games] [num_of_tournaments] [num_of_online_games]'
GIVEN_NAMES = [ 'bruce', 'malcolm', 'kobe', 'peter', 'kaylee', 'inara', ]
LAST_NAMES = [ 'lee', 'reynolds', 'bryant', 'parker', 'frye', 'serra', ]
CHAPTER_CODES = ['FFLY', 'NBAG', 'DEAD', 'BEEF']
COUNTRY_CODES = ['USA', 'CAN', 'JPN', 'KOR', 'CHN', 'TWN'] #these, oddly, are not the FK in the member table.
COUNTRY_NAMES = ['An awesome country', 'A cool country', 'Canada', 'United States of Awesome', 'Donnybrookistan']
SERVERS = ['JGS', 'KGS', 'LOLGS']
import datetime as dt

if len(sys.argv) != 5:
    print USAGE
    quit()

try:
    member_count = int(sys.argv[1])
    game_count = int(sys.argv[2])
    tourney_count = int(sys.argv[3])
    online_game_count = int(sys.argv[4])
except ValueError:
    print USAGE
    quit()

members = []
for member_id in range(member_count):
    first_name = random.choice(GIVEN_NAMES)
    last_name = random.choice(LAST_NAMES)
    members.append({
        'pk': member_id,
        'model': 'agagd_core.member',
        'fields': {
            'member_id': member_id,
            'legacy_id': '',
            'full_name': '%s %s' % (first_name, last_name),
            'given_names': first_name,
            'family_name': last_name,
            'join_date': None,
            'city': 'Seattle',
            'state': 'WA',
            'region': 'some region',
            'country': random.choice(COUNTRY_NAMES),
            'chapter': random.choice(CHAPTER_CODES),
            'chapter_id': 'MAYBE_FK',
            'occupation': '',
            'citizen': 'yes',
            'password': 'hallo!',
            'last_changed': None
        }
    })

tournaments = []
for tourney_id in range(tourney_count):
    tournaments.append({
        'pk': 'T%s' % str(tourney_id),
        'model': 'agagd_core.tournament',
        'fields': {
            'total_players': random.randint(4,20),
            'city': '',
            'elab_date': '2013-07-01',
            'description': '',
            'wall_list': '',
            'state': '',
            'rounds': random.randint(2,5),
            'tournament_date': '2013-07-01'
        }
    })

games = []
for game_id in range(game_count):
    p1 = random.choice(members)['pk']
    p2 = random.choice(filter(lambda m: m['pk'] != p1, members))['pk']
    date = dt.date.today() - dt.timedelta(days = random.randint(2,20))
    games.append({
        'pk': game_id,
        'model': 'agagd_core.game',
        'fields': {
            'pin_player_2': p2,
            'tournament_code': random.choice(tournaments)['pk'],
            'rated': '',
            'elab_date': date.strftime("%Y-%m-%d"),
            'handicap': random.randint(0, 2),
            'online': '',
            'color_2': '',
            'sgf_code': '',
            'komi': 0.0,
            'pin_player_1': p1,
            'rank_1': '',
            'result': '',
            'rank_2': '',
            'game_date': date.strftime("%Y-%m-%d"),
            'exclude': '',
            'round': '',
            'color_1': ''
        }
    })

chapters = [] 
for i, chap_code in enumerate(CHAPTER_CODES):
    chapters.append({
        'pk': i,
        'model': 'agagd_core.chapters',
        'fields': {
            'member_id': i,
            'code': chap_code,
            'name': random.choice(['Firefly Go Club', 'NBA Go Club', 'some other club']),
            'contact_text': random.choice(['Some contact info would go here.', '']),
            'contact': 'Some guy',
            'meeting_city': 'Seattle',
            'url': 'www.localhost-is-best-host.com',
        }
    }) 

countries = []
for i, count_name in enumerate(COUNTRY_NAMES): 
    countries.append({
        'pk': i,
        'model': 'agagd_core.country',
        'fields': {
            'country_code': random.choice(COUNTRY_CODES),
            'country_descr': count_name,
        }
    }) 

servers = []
for i, srv_name in enumerate(SERVERS): 
    servers.append({
        'pk': srv_name,
        'model': 'ratings.server',
        'fields': {
            'name': srv_name,
            'homepage': 'www.%s.com' % srv_name.lower(),
            'api_key':  hashlib.sha224(srv_name).hexdigest(),
            'game_url_root': 'not-a-url://www.%s.com/games' % srv_name.lower
            }
        })

online_players = []
alphabet = 'abcdefghijklmnopqrstuvwxyz' * 20
nicks = {}
for i in range(member_count):
    mem = random.choice(members)['pk']
    nick = random.sample(alphabet, 12)
    if nick in nicks:
        continue
    nicks.add(nick)
    online_player.append({
        'pk': i,
        'model': 'ratings.online_player',
        'fields': {
            'server': random.choice(SERVERS),
            'server_secret_key': hashlib.sha224(nick).hexdigest(),
            'nickname': nick,
            'pin_player': mem,
            }
        })

online_games = []
for i in range(online_game_count):
    pass 


print json.dumps(members + tournaments + games + chapters + countries + servers + online_players, indent=4)
