import mysql.connector as sql
from mysql.connector import errorcode

date = raw_input("Enter the date of the game: ")
homeID = raw_input("Enter the 3-letter abbreviation for the home team: ")
awayID = raw_input("Enter the 3-letter abbreviation for the away team: ")
homeScore = input("Enter the home team's score: ")
awayScore = input("Enter the away team's score: ")

homeWon = True
if awayScore > homeScore:
	homeWon = False

conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
cursor = conn.cursor(buffered=True)

#######################################################################################################################################################
# UPDATE NBA STANDINGS
cursor.execute("select team_id, wins from nba where team_id = %s", (homeID,))
for (team_id, wins) in cursor:
	if homeWon:
		# Update the home team's points for
		cursor2 = conn.cursor(buffered=True)
		cursor2.execute("update nba set points_for = (points_for * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (homeScore, homeID,))
		# Update the home team's points against
		cursor2.execute("update nba set points_against = (points_against * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (awayScore, homeID,))
		# Update the away team's points for
		cursor2.execute("update nba set points_for = (points_for * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (awayScore, awayID,))
		# Update the away team's points against
		cursor2.execute("update nba set points_against = (points_against * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (homeScore, awayID,))
		# Add a win to the home team's standings
		cursor2.execute("update nba set wins = wins + 1 where team_id = %s", (homeID,))
		# Add a loss to the away team's standings
		cursor2.execute("update nba set losses = losses + 1 where team_id = %s", (awayID,))

		# Commit changes
		conn.commit()

	else:
                # Update the home team's points for
                cursor2 = conn.cursor(buffered=True)
                cursor2.execute("update nba set points_for = (points_for * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (homeScore, homeID,))
                # Update the home team's points against
                cursor2.execute("update nba set points_against = (points_against * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (awayScore, homeID,))
                # Update the away team's points for
                cursor2.execute("update nba set points_for = (points_for * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (awayScore, awayID,))
                # Update the away team's points against
                cursor2.execute("update nba set points_against = (points_against * (wins + losses) + %s) / (wins + losses + 1) where team_id = %s", (homeScore, awayID,))
		# Add a win to the away team's standings
                cursor2.execute("update nba set wins = wins + 1 where team_id = %s", (awayID,))
                # Add a loss to the home team's standings
                cursor2.execute("update nba set losses = losses + 1 where team_id = %s", (homeID,))

                # Commit changes
                conn.commit()

	print("Updated standings")

####################################################################################################################################################
# UPDATE BETS

# First, determine if home team covered spread
homeCovered = False
homeSpread = 0.0
cursor.execute("select home_spread from nba_schedule where date = %s and home_id = %s", (date, homeID,))
for (home_spread) in cursor:
	homeSpread = home_spread[0]

if (awayScore - homeScore) > homeSpread:
	homeCovered = False
else:
	homeCovered = True

# Next, determine if game went over or under
over = True
overUnder = 0.0
cursor.execute("select over_under from nba_schedule where date = %s and home_id = %s", (date, homeID,))
for over_under in cursor:
	overUnder = over_under[0]
if homeScore + awayScore > overUnder:
	over = True
else:
	over = False

# Next, pull home and away money lines from schedule
homeML = 0
awayML = 0
cursor.execute("select home_money_line, away_money_line from nba_schedule where date = %s and home_id = %s", (date, homeID,))
for (home_money_line, away_money_line) in cursor:
	homeML = home_money_line
	awayML = away_money_line

# Finally, update bets in bets table
cursor.execute("select * from bets where date = %s and (team_id = %s or team_id = %s)", (date, homeID, awayID,))
for (username, date, bet_type, risk, team_id) in cursor:
	cursor2 = conn.cursor(buffered=True)
	if bet_type == 'S':
		# Spread bet
		if (team_id == homeID and homeCovered) or (team_id == awayID and not homeCovered):
			# Winning bet
			cursor2.execute("update users set balance = balance + %s where username = %s", (risk, username,))
		else:
			# Losing bet
			cursor2.execute("update users set balance = balance - %s where username = %s", (risk, username,))
	elif bet_type == 'M':
		# Money line bet
		if team_id == homeID and homeWon:
			# Winning bet on home team
			payout = 0.0
			if homeML > 0:
				# Underdog
				payout = risk * homeML / 100.0
			else:
				# Favorite
				payout = risk * 100.0 / (-1.0 * homeML)

			cursor2.execute("update users set balance = balance + %s where username = %s", (payout, username,))

		elif team_id == homeID and not homeWon:
			cursor2.execute("update users set balance = balance - %s where username = %s", (risk, username,))

		elif team_id == awayID and homeWon:
			cursor2.execute("update users set balance = balance - %s where username = %s", (risk, username,))
		else:
			# Winning bet on away team
			payout = 0.0
			if awayML > 0:
				# Underdog
				payout = risk * awayML / 100.0
			else:
				# Favorite
				payout = risk * 100.0 / (-1.0 * awayML)

			cursor2.execute("update users set balance = balance + %s where username = %s", (payout, username,))

	elif bet_type == 'O':
		if over:
			cursor2.execute("update users set balance = balance + %s where username = %s", (risk, username,))
		else:
			cursor2.execute("update users set balance = balance - %s where username = %s", (risk, username,))
	elif bet_type == 'U':
		if over:
			cursor2.execute("update users set balance = balance - %s where username = %s", (risk, username,))
		else:
			cursor2.execute("update users set balance = balance + %s where username = %s", (risk, username,))

	# Remove bet from table
	cursor2.execute("delete from bets where date = %s and username = %s and bet_type = %s and risk = %s and team_id = %s limit 1", (date, username, bet_type, risk, team_id,))

print("Updated bets")

####################################################################################################################################################
# REMOVE GAME FROM NBA SCHEDULE
cursor.execute("delete from nba_schedule where date = %s and home_id = %s", (date, homeID,))
conn.commit()
print("Updated schedule")

####################################################################################################################################################
# UPDATE LINES FOR UPCOMING SCHEDULE
execfile("LineCreator.py")
print("Updated lines")


conn.close()

