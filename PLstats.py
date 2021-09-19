import random
teams1=["Manchester City","Liverpool","Tottenham Hotspur","Chelsea","Arsenal"]
teams2=["Manchester United","Wolverhampton","Watford","Everton","West Ham United"]
teams3=["A.F.C Bournemouth","Leicester City","Crystal Palace","Brighton","Burnley"]
teams4=["Cardiff City","Newcastle United","Southampton","Fulham","Huddersfield Town"]
teams=teams1+teams2+teams3+teams4
homegoals=[3.21,2.21,1.95,1.63,1.95,1.79,1.32,1.16,1.30,1.26,1.18,1.24,1.07,0.89,0.98,0.92,1.03,0.97,0.96,0.74]
awaygoals=[2.37,2.21,1.95,1.63,1.95,1.79,1.32,1.16,1.30,1.26,1.18,1.24,1.07,0.89,0.98,0.92,1.03,0.97,0.96,0.74]
homeconcede=[0.71,1.00,1.26,1.00,0.97,0.74,1.28,1.68,1.27,1.79,1.61,1.45,1.45,1.42,1.55,1.81,1.24,1.47,2.23,1.53]
awayconcede=[0.71,1.00,1.26,1.00,0.97,0.74,1.28,1.68,1.27,1.79,1.61,1.45,1.45,1.42,1.55,1.81,1.24,1.47,2.23,1.53]
homewins=[16/19,12/19,13/19,11/19,15/19,15/19,4/10,7/19,10/19,7/19,6/19,7/19,7/19,7/19,7/19,4/10,7/19,4/19,2/9,6/19]
homelosses=[1/19,0,2/19,4/19,2/19,2/19,4/10,6/19,4/19,6/19,7/19,6/19,7/19,4/19,7/19,5/10,7/19,8/19,4/9,8/19]
awaywins=[16/19,9/19,10/19,10/19,4/19,10/19,3/9,4/19,3/19,3/19,4/19,5/19,4/19,2/19,7/19,0,4/19,3/19,0,3/19]
awaylosses=[1/19,5/19,5/19,6/19,11/19,4/19,3/9,13/19,10/19,10/19,9/19,9/19,9/19,12/19,5/19,7/19,11/19,8/19,8/10,11/19]
# not included prob of draw for a reason
hg=dict(zip(teams,homegoals))
ag=dict(zip(teams,awaygoals))
hc=dict(zip(teams,homeconcede))
ac=dict(zip(teams,awayconcede))
hw=dict(zip(teams,homewins))
hl=dict(zip(teams,homelosses))
aw=dict(zip(teams,awaywins))
al=dict(zip(teams,awaylosses))

def simulate(game):
    match=game.split(" v ")
    t1=0
    t2=0
    count=0
    team1=""
    team2=""
    for i in match:
        for j in teams:
            if i==j and count==0:
                team1=i
                count=1
            
            elif i==j and count==1:
                team2=i
                count=2

    print(team1+team2)
    t1goals=(hg.get(team1)+ac.get(team2))/2
    t2goals=(ag.get(team2)+hc.get(team1))/2
    print(str(t1goals)+":"+str(t2goals))
    winner=whowins(team1,team2)
    advantage=""
    goalratio=0
    if t1goals>t2goals:
        goalratio=round(t1goals/t2goals,0)
        advantage=team1
        
    elif t2goals>t1goals:
        goalratio=round(t2goals/t1goals,0)
        advantage=team2
        
    else:
        goalratio=1

    if goalratio==1:
        num=random.randrange(1,4)

    elif goalratio==2:
        num=random.randrange(1,5)

    else:
        num=random.randrange(1,6)

    if num==1:
        result=goalratio1()

    elif num==2:
        result=goalratio2()

    elif num==3:
        result=goalratio3()

    elif num==4:
        result=goalratio4()

    else:
        result=goalratio5()

    count=0
    for i in result:
        if count==0:
            low=i
            count=1
        else:
            high=i
    add=random.randrange(1,4)
    if winner=="team1" and advantage==team1:
        t1=high
        t2=low

    elif winner=="team1" and advantage==team2 and num>=3:
        t1=high-num+add
        t2=low

    elif winner=="team1" and advantage==team2 and num<3 and low<=2:
        t1=high-num+add
        t2=low

    elif winner=="team1" and advantage==team2 and num<3 and low>2:
        subtract=random.randrange(1,4)
        t1=high-subtract
        t2=low-subtract

    elif winner=="team2" and advantage==team2:
        t2=high
        t1=low

    elif winner=="team2" and advantage==team1 and num>=3:
        t2=high-num+add
        t1=low

    elif winner=="team2" and advantage==team1 and num<3 and low<=2:
        t2=high-num+add
        t1=low

    elif winner=="team2" and advantage==team1 and num<3 and low>2:
        subtract=random.randrange(1,4)
        t2=high-subtract
        t1=low-subtract
    
    elif winner=="draw":
        num=goalratio0()
        count=0
        for i in num:
            if count==0:
                low=i
                count=1
            else:
                high=i
        t1=high
        t2=low
            
    return winner+" "+(str(t1)+"-"+str(t2))
        
def whowins(team1,team2):
    winner=""
    probteam1=(hw.get(team1)+al.get(team2))/2
    probteam2=(aw.get(team2)+hl.get(team1))/2
    probdraw=1-probteam1-probteam2
    chancet1=probteam1*100
    chancet2=probteam2*100
    chancedraw=probdraw*100
    num=random.randrange(1,101)
    if num>=0 and num<=chancet1:
        winner="team1"
    elif num>chancet1 and num<=chancet1+chancet2:
        winner="team2"

    else:
        winner="draw"

    return winner

def goalratio0():
    prob=random.randrange(1,101)
    if prob<=60:
        num2=random.randrange(1,3)
        num1=num2

    elif prob>60 and prob<=75:
        num2=random.randrange(1,4)
        num1=num2
    else:
        num2=random.randrange(1,6)
        num1=num2
    return num1,num2

def goalratio1():
    num2=random.randrange(1,6)
    num1=num2-1
    return num1,num2

def goalratio2():
    num2=random.randrange(2,6)
    num1=num2-2
    return num1,num2

def goalratio3():
    num2=random.randrange(3,6)
    num1=num2-3
    return num1,num2

def goalratio4():
    num2=random.randrange(4,6)
    num1=num2-4
    return num1,num2

def goalratio5():
    num2=random.randrange(5,6)
    num1=num2-5
    return num1,num2


        
    
    









    
    
    
    
    
