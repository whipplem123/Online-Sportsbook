import mysql.connector as sql
import math
import sys

conn = sql.connect(user='thesportsbook', password='ultimate', host='cs252-lab6-mariadb.cuxhokshop3s.us-east-2.rds.amazonaws.com', database='lab6')
cursor = conn.cursor(buffered=True)

cursor.execute("select home_id, away_id, date from nba_schedule")

for (home_id, away_id, date) in cursor:
        cursor2 = conn.cursor(buffered=True)
        cursor3 = conn.cursor(buffered=True)
        cursor2.execute("select points_for, points_against from nba where team_id = %s", (home_id,))
        cursor3.execute("select points_for, points_against from nba where team_id = %s", (away_id,))
        homeDiff = 0.0
        awayDiff = 0.0
        over_under = 0.0
        homeML = 0
        awayML = 0
        for (points_for, points_against) in cursor2:
                over_under += points_for + points_against
                homeDiff = points_for - points_against

        for (points_for, points_against) in cursor3:
                over_under += points_for + points_against
                awayDiff = points_for - points_against

        homeSpread = math.floor(awayDiff - homeDiff - 3.0) + 0.5
        awaySpread = -1 * homeSpread

        if homeSpread <= 0:
                x = .5 - homeSpread * .03
                homeML = math.floor((-100 * x) / (1-x))
        else:
                x = .5 - homeSpread * .03
                homeML = math.floor((100 - 100 * x) / x)

		if awaySpread <= 0:
                x = .5 - awaySpread * .03
                awayML = math.floor((-100 * x) / (1-x))
        else:
                x = .5 - awaySpread * .03
                awayML = math.floor((100 - 100 * x) / x)

        over_under /= 2.0
        cursor4 = conn.cursor()
        cursor4.execute("update nba_schedule set home_spread = %s, home_money_line = %s, away_spread = %s, away_money_line = %s, over_under = %s where (home_id = %s and date = %s)", (homeSpread, homeML, awaySpread, awayML, over_under, home_id, date,))
        conn.commit()

conn.close()
