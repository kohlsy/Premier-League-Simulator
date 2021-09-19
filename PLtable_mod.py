import sys,os,time
import PLstats
from PyQt4 import QtCore, QtGui, uic,QtSql
from PLtable_auto import *
import sqlite3
import PLpoints_mod
import PLresults_mod
 
class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        for j in range(1,2,1):
            QtGui.QMainWindow.__init__(self, parent)
            self.setupUi(self)
            self.ui=Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowTitle("PL Simulation")
            self.connect(self.ui.actionPoints_Table,QtCore.SIGNAL("triggered()"),self.points)
            self.connect(self.ui.actionPL_Results,QtCore.SIGNAL("triggered()"),self.results)
            self.ui.btn_next.clicked.connect(self.nextweek)
            self.ui.btn_simulate.clicked.connect(self.simulate)
            dbfile="PLtable.db"
            self.conn=sqlite3.connect(dbfile)
            cursor=self.conn.cursor()
            cursor.execute("update PL_table set P=0,W=0,D=0,L=0,GF=0,GA=0,GD=0,Pts = 0")
            comma='"",' 
            statement="update PL_results set Match_1="+comma+"Match_2="+comma+"Match_3="+comma+"Match_4="+comma+"Match_5="+comma+"Match_6="+comma+"Match_7="+comma+"Match_8="+comma+"Match_9="+comma+"Match_10="+'""'
            cursor.execute(statement)
            print(statement)
            self.gameweek=0
            if os.path.exists(dbfile):
                db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(dbfile)
                db.open()
            else:
                QtQui.QMessageBox.critical(self,"Critical Error", "Database file was not fouNnd here")
                return None
            self.retrieve()
            for i in range(1,38,1):
               self.nextweek()
               self.simulate()
            cursor.execute("select team from PL_table order by Pts desc,GD desc,GF desc")
            self.conn.commit()
            fetch=cursor.fetchall()
            winner=fetch[0]
            team=""
            for i in winner:
                team=team+i
            setwinner="Insert into PL_winners (Winner) values ("+'"'+team+'")'
            print(setwinner)
            cursor.execute(setwinner)
            self.nextweek()

    def week(self):
        return self.gameweek

    def points(self):
        points = PLpoints_mod.MyForm(self)
        points.exec()

    def results(self):
        results = PLresults_mod.MyForm(self)
        results.exec()

    def retrieve(self):
        self.ui.listWidget.clear()
        cursor=self.conn.cursor()
        week=str(self.gameweek)
        cursor.execute("select Match_1,Match_2,Match_3,Match_4,Match_5,Match_6,Match_7,Match_8,Match_9,Match_10,Date from PL_fixtures where Game_Week='"+week+"'")
        self.conn.commit()
        row=cursor.fetchall()
        r=""
       # print(row)
        for r in row:
            match1,match2,match3,match4,match5,match6,match7,match8,match9,match10,date = r
            self.match1=match1
            self.match2=match2
            self.match3=match3
            self.match4=match4
            self.match5=match5
            self.match6=match6
            self.match7=match7
            self.match8=match8
            self.match9=match9
            self.match10=match10
        print(r)
        for i in r:
            self.fixture="\t"+i
            self.ui.listWidget.addItem(self.fixture)

    def nextweek(self):
        print("Next week")
        self.gameweek=self.gameweek+1
        self.ui.lbl_week.setText("Matchday "+str(self.gameweek))
        self.retrieve()

    def simulate(self):
        self.ui.listWidget.clear()
        cursor=self.conn.cursor()
        week=str(self.gameweek)
        
        cursor.execute("select Match_1,Match_2,Match_3,Match_4,Match_5,Match_6,Match_7,Match_8,Match_9,Match_10 from PL_fixtures where Game_Week='"+week+"'")
        self.conn.commit()
        row=cursor.fetchall()
       # print(row)
        for r in row:
           match1,match2,match3,match4,match5,match6,match7,match8,match9,match10= r
           self.match1=match1
           self.match2=match2
           self.match3=match3
           self.match4=match4
           self.match5=match5
           self.match6=match6
           self.match7=match7
           self.match8=match8
           self.match9=match9
           self.match10=match10
           print(r)
        count=1
        for i in r:
           if count!=11:
              data=PLstats.simulate(i)
              print(data)
              result=data.split(" ")
              winner=result[0]
              score=result[1]
              match=i.split(" v ")
              team1=match[0]
              team2=match[1]
              print(team1)
              print(team2)
              goals=score.split('-')
              print(goals)
              t1goals=int(goals[0])
              t2goals=int(goals[1])
              details=team1+" v "+team2+"  "+score
              print(details)
              cursor=self.conn.cursor()
              comma='"'
              matchno="Match_"+str(count)
              statement="update PL_results set "+matchno+"="+comma+details+comma+" where Game_Week="+str(self.gameweek)
              print("\n\n\n\n"+statement+"\n\n\n\n")
              cursor.execute(statement)
              spaces=40-len(i)
              
              if len(i)<30:
                 self.fixture="\t"+i+"\t\t"+score
                 time.sleep(0)
                 self.ui.listWidget.addItem(self.fixture)
                 print(self.fixture+"Test")

              else:
                 self.fixture="\t"+i+"\t"+score
                 time.sleep(0)
                 self.ui.listWidget.addItem(self.fixture)
                 print(self.fixture+"Test")

              if winner=="team1":
                 #SQL code for updating team1 in points table
                 cursor=self.conn.cursor()
                 GD1=t1goals-t2goals
                 GD2=t2goals-t1goals
                 comma='"'
                 print(t1goals)
                 print(t2goals)
                 statement1="update PL_table set P=P+1,W=W+1,GF=GF+"+str(t1goals)+",GA=GA+"+str(t2goals)+",GD=GD+"+str(GD1)+",Pts=Pts+3 where team="+comma+team1+comma
                 statement2="update PL_table set P=P+1,L=L+1,GF=GF+"+str(t2goals)+",GA=GA+"+str(t1goals)+",GD=GD+"+str(GD2)+" where team="+comma+team2+comma
                 cursor.execute(statement1)
                 cursor.execute(statement2)
                 self.conn.commit()

              elif winner=="team2":
                 #SQL code for updating team2 in points table
                 cursor=self.conn.cursor()
                 GD1=t2goals-t1goals
                 GD2=t1goals-t2goals
                 comma='"'
                 print(t1goals)
                 print(t2goals)
                 statement1="update PL_table set P=P+1,W=W+1,GF=GF+"+str(t2goals)+",GA=GA+"+str(t1goals)+",GD=GD+"+str(GD1)+",Pts=Pts+3 where team="+comma+team2+comma
                 statement2="update PL_table set P=P+1,L=L+1,GF=GF+"+str(t1goals)+",GA=GA+"+str(t2goals)+",GD=GD+"+str(GD2)+" where team="+comma+team1+comma
                 cursor.execute(statement1)
                 cursor.execute(statement2)
                 self.conn.commit()

              else:
                 #SQL code for draw and updating both teams' score by 1 point
                 cursor=self.conn.cursor()
                 GD=t2goals-t1goals
                 comma='"' 
                 statement1="update PL_table set P=P+1,D=D+1,GF=GF+"+str(t1goals)+",GA=GA+"+str(t2goals)+",GD=GD+"+str(GD)+",Pts=Pts+1 where team="+comma+team1+comma
                 statement2="update PL_table set P=P+1,D=D+1,GF=GF+"+str(t2goals)+",GA=GA+"+str(t1goals)+",GD=GD+"+str(GD)+",Pts=Pts+1 where team="+comma+team2+comma
                 cursor.execute(statement1)
                 cursor.execute(statement2)
                 self.conn.commit()

           else:
               pass
           
           count=count+1

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()

