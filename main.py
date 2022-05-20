import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt

KeyStats = ["FULLNAME", "POS", "PPG","APG","RPG","GP"]

def StatLeaders():
    StatSelection = input("choose a stat you would like to see the leader of?(PPG,APG,RPG,GP)").upper()
    PlayerStats = pd.read_csv('Stats.csv')
    PlayerStats = PlayerStats.sort_values(by=[StatSelection], ascending=True)
    x = PlayerStats[StatSelection].idxmax()
    for i in range(len(KeyStats)):
        i = KeyStats[i]
        print(i,PlayerStats.loc[x][i])

def Top10Statleaders():
    FULLNAME = "FULLNAME"
    StatSelection = input("choose a stat you would like to see the leaders of?(PPG,APG,RPG)").upper()
    PlayerStats = pd.read_csv('Stats.csv')
    for i in range(len(PlayerStats)):
        GP = PlayerStats.loc[i]["GP"]
        if GP < 40:
            PlayerStats = PlayerStats.drop([i])
        else:
            pass
    PlayerStats = PlayerStats.sort_values(by=[StatSelection], ascending=False)
    PlayerStats = PlayerStats[["FULLNAME",StatSelection,"POS","GP"]].head(10)
    print(PlayerStats)

def SearchPlayer():# find a players stats and display the there best 5 statical catergories
    stats = ["PPG","APG","RPG","TOPG","GP","MPG","FTA","FT%","2PA", "2P%","3PA","3P%","SPG","BPG","ORTG","DRTG"]#list of important stats
    PlayerStats = pd.read_csv('Stats.csv')#create a dataframe with all the players stats
    findPlayer = input("please enter player first and last name with a space inbetween") #getting players name that user wants to find
    player = PlayerStats.loc[PlayerStats.FULLNAME == findPlayer]#finding the players stats that the user inputted
    HigherMeansBetter = ["PPG", "APG", "GP", "FTA", "FT%","2PA","2P%","3PA","3P%","SPG","BPG","ORTG"] #stats that are higher are better
    Top5ForPlayerIndex = []
    Top5ForPlayersColumnName = []
    NewIndex = []
    FinalData = []

    for i in range(len(PlayerStats)):
        NewIndex.append(i)

    for i in range(len(HigherMeansBetter)): #adding new index values to sorted dataframe
        SortedStats = PlayerStats.sort_values(HigherMeansBetter[i], ascending=False)
        SortedStats["UpdatedIndex"] = NewIndex
        Rating = (SortedStats[SortedStats.FULLNAME == findPlayer]["UpdatedIndex"]).values[0]
        del SortedStats["UpdatedIndex"]

        if len(Top5ForPlayerIndex) < 5: #seeing how long list is and if it is less than five goes straight into best stat list
            Top5ForPlayerIndex.append(Rating)
            Top5ForPlayersColumnName.append(HigherMeansBetter[i])

        #getting lowest stat in player index list
        LowestRanking = max(Top5ForPlayerIndex)

        if len(Top5ForPlayerIndex) == 5:   #if list is == 5 removing stat that has the highest index.
            if Rating < LowestRanking:
                for l in range(len(Top5ForPlayerIndex)):
                    if Top5ForPlayerIndex[l] >= LowestRanking:
                        Top5ForPlayerIndex.pop(l)
                        Top5ForPlayersColumnName.pop(l)
                        Top5ForPlayerIndex.append(Rating)
                        Top5ForPlayersColumnName.append(HigherMeansBetter[i])

        else:
            for L in range(len(Top5ForPlayerIndex)):
                TemporaryRating = Top5ForPlayerIndex[L]
                if TemporaryRating > Rating:
                    Top5ForPlayerIndex.pop(L)
                    Top5ForPlayersColumnName.pop(L)
                    Top5ForPlayerIndex.append(Rating)
                    Top5ForPlayersColumnName.append(HigherMeansBetter[L])

    for h in range(len(Top5ForPlayerIndex)):
        print((Top5ForPlayersColumnName[h]),(PlayerStats[PlayerStats.FULLNAME == findPlayer][Top5ForPlayersColumnName[h]]).values[0])

def TeamStatistics():
    UniqueTeam = None
    PlayerStats = pd.read_csv("Stats.csv")
    StatsToFindForTeam = ["PPG","APG","RPG", "BPG","SPG"]
    TeamSelection = input("type the team you would like to see the stats of")
    Teams = []
    IndivualStats = []
    GP = []
    TeamStats = []
    for i in range(len(PlayerStats)): #finding all the teams in the dataframe
        UniqueTeam = True
        CurrentTeam = PlayerStats.TEAM[i]
        for i in range(len(Teams)):
            if Teams[i] == CurrentTeam:
                UniqueTeam = False
        if UniqueTeam == True:
            Teams.append(CurrentTeam)

    for i in range(len(StatsToFindForTeam)):
        TotalStat = 0
        PercentStats = 0
        Percentage = 0
        PlayerInTeam = (PlayerStats.loc[PlayerStats['TEAM'] == TeamSelection][StatsToFindForTeam[i]])
        GP = (PlayerStats.loc[PlayerStats['TEAM'] == TeamSelection]["GP"])

        for j in range(len(PlayerInTeam)):

            if StatsToFindForTeam[i] != "2P%" or StatsToFindForTeam[i] != "3P%":
                TemporaryPlayerStat = PlayerInTeam.iloc[j]
                GamesPlayedByPlayer = GP.iloc[j]
                TotalStat = (GamesPlayedByPlayer * TemporaryPlayerStat) + TotalStat

        if TotalStat > 0:
            TotalStat /= 62
            print(StatsToFindForTeam[i], round(TotalStat))

def ListTotals(List):
    total = 0
    for val in List:
        total += val
    return total

#graph players rating out of 3 catergories using a algorithm
def ComparePlayersAndGraph():
    StatOrder = True
    PlayerStats = pd.read_csv("Stats.csv")
    PlayerSelection1 = input("Select first player for comparison")
    PlayerSelection2 = input("Select Second player for comparison")
    Catergories = ["Scoring", "Defense", "Three Point Shooting","Playmaking"]
    Stats = [["PPG", "2P%", "3P%", "FT%"],["SPG","BPG","DRTG"],["3P%", "3PA"],["APG", "TOPG", "AST%"]]
    TenPercentOfDb = len(PlayerStats)/10
    P1StatsRanking = []
    OverallRating1 = []
    P2StatsRanking =[]
    OverallRating2 = []
    Players = [PlayerSelection1, PlayerSelection2]
    NewIndex = []

    for i in range(len(PlayerStats)):
        NewIndex.append(i)
#Player 1 stat calculation
    for i in range(len(Stats)):
        StatCategory = Stats[i]
        for i in range(len(StatCategory)):
            if StatCategory[i] == "TOPG":
                StatOrder = False
            else:
                StatOrder = True
            SortedStats = PlayerStats.sort_values(StatCategory[i], ascending=StatOrder)
            SortedStats["UpdatedIndex"] = NewIndex
            Rating = (SortedStats[SortedStats.FULLNAME == PlayerSelection1]["UpdatedIndex"]).values[0]
            del SortedStats["UpdatedIndex"]
            P1StatsRanking.append(Rating)

    for i in range(len(P1StatsRanking)):
        StatRating = round(P1StatsRanking[i]/TenPercentOfDb)
        OverallRating1.append(StatRating)

    for i in range(len(Stats)):
        CategoryLength =  len(Stats[i])
        StatOverallRating = OverallRating1[0:CategoryLength]
        StatTotals = ListTotals(StatOverallRating)
        StatTotals = round(StatTotals/CategoryLength)
        OverallRating1.append(StatTotals)
        del OverallRating1[0:CategoryLength]

#Player 2 stat calculation
    for i in range(len(Stats)):
        StatCategory = Stats[i]
        for i in range(len(StatCategory)):
            if StatCategory[i] == "TOPG":
                StatOrder = False
            else:
                StatOrder = True
            SortedStats = PlayerStats.sort_values(StatCategory[i], ascending=StatOrder)
            SortedStats["UpdatedIndex"] = NewIndex
            Rating = (SortedStats[SortedStats.FULLNAME == PlayerSelection2]["UpdatedIndex"]).values[0]
            del SortedStats["UpdatedIndex"]
            P2StatsRanking.append(Rating)

    for i in range(len(P2StatsRanking)):
        StatRating = round(P2StatsRanking[i]/TenPercentOfDb)
        OverallRating2.append(StatRating)

    for i in range(len(Stats)):
        CategoryLength =  len(Stats[i])
        StatOverallRating = OverallRating2[0:CategoryLength]
        StatTotals = ListTotals(StatOverallRating)
        StatTotals = round(StatTotals/CategoryLength)
        OverallRating2.append(StatTotals)
        del OverallRating2[0:CategoryLength]

    w = 0.4

    bar1 = np.arange(len(Catergories))
    bar2 = [i+w for i in bar1]
    YValues = [2,4,6,8,10]

    GraphTitle = (PlayerSelection1 + " VS " + PlayerSelection2)
    plt.bar(bar1,OverallRating1,w,label=PlayerSelection1,tick_label=Catergories)
    plt.bar(bar2,OverallRating2,w,label=PlayerSelection2)
    plt.yticks(YValues)
    plt.legend(bbox_to_anchor=(0.65,1.15))
    plt.show()

run = True
while run:
    print("choose a function that you would like to run (GraphTwoPlayers,PlayersBestStats,TeamStatistics,StatLeaders)")
    print("Or Type Quit to end the code")
    FunctionSelection = input()

    if FunctionSelection == "GraphTwoPlayers":
        ComparePlayersAndGraph()
    elif FunctionSelection == "PlayersBestStats":
        SearchPlayer()
    elif FunctionSelection == "TeamStatistics":
        TeamStatistics()
    elif FunctionSelection == "StatLeaders":
        Top10Statleaders()
    elif FunctionSelection == "Quit":
        run = False
    else:
        print("Try entering the command again a spelling error may have occured")