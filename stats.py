import urllib2
from BeautifulSoup import BeautifulSoup

class Goalie:

	def __init__(self, row):

		cols = row.findAll('td')
		self.invalid = False

		if not len(cols) > 1:
			self.invalid = True
			return

		self.name = cols[1].getText()
		self.team = cols[2].getText()
		self.games_played = int(cols[3].getText())
		self.games_started = int(cols[4].getText())
		self.wins = int(cols[5].getText())
		self.losses = int(cols[6].getText())
		self.ot = int(cols[7].getText())
		self.shots_against = int(cols[8].getText())
		self.goals_against = int(cols[9].getText())
		self.gaa = float(cols[10].getText())
		self.saves = int(cols[11].getText())
		self.save_percentage = float(cols[12].getText())
		self.shutouts = int(cols[13].getText())


class Player:

	def __init__(self, row):

		cols = row.findAll('td')
		self.invalid = False

		if not len(cols) > 1:
			self.invalid = True
			return

		self.name = cols[1].getText()
		self.team = cols[2].getText()
		self.pos = cols[3].getText()
		self.games_played = int(cols[4].getText())
		self.goals = int(cols[5].getText())
		self.assists = int(cols[6].getText())
		self.points = int(cols[7].getText())
		self.plus_minus = cols[8].getText()
		self.pims = int(cols[9].getText())
		self.ppg = int(cols[10].getText())
		self.ppp = int(cols[11].getText())
		self.shg = int(cols[12].getText())
		self.shp = int(cols[13].getText())
		self.gwg = int(cols[14].getText())
		self.otg = int(cols[15].getText())
		self.shots = int(cols[16].getText())

goalies = []
left_wings = []
right_wings = []
centermen = []
defense = []

for p in range(4):
	page = urllib2.urlopen('http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLGAGALL&viewName=summary&pg=%d' % (p + 1)).read()

	soup = BeautifulSoup(page)
	rows = soup.findAll('table')[4].findAll('tr')

	for row in rows:
		goalie = Goalie(row)

		if goalie.invalid:
			continue

		goalies.append(goalie)

for p in range(12):
	page = urllib2.urlopen('http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLSASAll&viewName=summary&pg=%d' % (p + 1)).read()

	soup = BeautifulSoup(page)
	rows = soup.findAll('table')[4].findAll('tr')

	for row in rows:
		player = Player(row)

		if player.invalid:
			continue

		if player.pos == 'D':
			defense.append(player)
		if player.pos == 'L':
			left_wings.append(player)
		if player.pos == 'R':
			right_wings.append(player)
		if player.pos == 'C':
			centermen.append(player)

def calc_avg(players, _attr):
	current = 0
	num = 0
	for player in players:
		if hasattr(player, _attr):
			try:
				item = float(getattr(player, _attr))
			except:
				continue
			current += item
			num += 1

	return float(current) / float(num)


def calc(groups, cats):
	avgs = {}

	for players in groups:
		for item in cats:
			avgs[item] = calc_avg(players, item)

	for players in groups:
		for player in players:
			total = 0.0
			for cat in cats:
				val = float(getattr(player, cat)) / float(avgs.get(cat))
				setattr(player, '%s__val' % cat, val)
				total += val
			setattr(player, 'total_val', total)


PLAYER_GROUPS = [left_wings, right_wings, centermen, defense]
PLAYER_CATS = ['goals', 'assists', 'plus_minus', 'pims', 'ppp', 'shots']

GOALIE_GROUPS = [goalies]
GOALIE_CATS = ['wins', 'gaa', 'save_percentage', 'shutouts']

calc(PLAYER_GROUPS, PLAYER_CATS)
calc(GOALIE_GROUPS, GOALIE_CATS)

left_wings = sorted(left_wings, key=lambda player: player.total_val, reverse=True)
right_wings = sorted(right_wings, key=lambda player: player.total_val, reverse=True)
defense = sorted(defense, key=lambda player: player.total_val, reverse=True)
goalies = sorted(goalies, key=lambda player: player.total_val, reverse=True)
centermen = sorted(centermen, key=lambda player: player.total_val, reverse=True)

for group in ['left_wings', 'right_wings', 'defense', 'goalies', 'centermen']:
	group_list = eval(group)
	player_file = open('%s.txt' % group, 'w')

	for player in group_list:
		player_file.write('%s : %s\n' % (player.name, player.total_val))








