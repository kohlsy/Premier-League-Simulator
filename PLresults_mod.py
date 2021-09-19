import sys
import os
import sqlite3
from PLresults_auto import *
from PyQt4 import QtSql, QtCore, QtGui, uic 
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dbfile="PLtable.db"
        self.ui.btn_next.clicked.connect(self.nextweek)
        self.ui.btn_prev.clicked.connect(self.prevweek)
        self.conn=sqlite3.connect("PLtable.db")
        s=self.getWeek()
        print(s)
        self.resultweek=self.getWeek()
        #this is where we will bind the event handlers
        
#This is where we will insert the functions (defs)

        if os.path.exists(dbfile):
            db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(dbfile)
            db.open()
            print("GO")
        else:
            QtQui.QMessageBox.critical(self,"Critical Error", "Database file was not found here")
            print("STOP")
            return None
        self.retrieve()

    def getWeek(self):
        cursor=self.conn.cursor()
        cursor.execute("select Game_Week from PL_results where Match_1="+'""')
        self.conn.commit()
        row=cursor.fetchall()
        if row==[]:
            return 38
        else:
            for i in row[0]:
                print(i)
            return i-1

    def retrieve(self):
        self.ui.listWidget.clear()
        cursor=self.conn.cursor()
        week=str(self.resultweek)
        self.ui.lbl_week.setText("Matchday "+week)
        cursor.execute("select Match_1,Match_2,Match_3,Match_4,Match_5,Match_6,Match_7,Match_8,Match_9,Match_10 from PL_results where Game_Week='"+week+"'")
        self.conn.commit()
        row=cursor.fetchall()
        r=""
        print(row)
        for r in row:
            match1,match2,match3,match4,match5,match6,match7,match8,match9,match10 = r
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
            self.fixture=i.split("  ")
            print(self.fixture)
            if len(self.fixture[0])<30:
                self.ui.listWidget.addItem("\t"+self.fixture[0]+"\t\t"+self.fixture[1])
            else:
                self.ui.listWidget.addItem("\t"+self.fixture[0]+"\t"+self.fixture[1])

    def nextweek(self):
        print("Next week")
        self.resultweek=self.resultweek+1
        self.ui.lbl_week.setText("Matchday "+str(self.resultweek))
        self.retrieve()

    def prevweek(self):
        print("Previous week")
        self.resultweek=self.resultweek-1
        self.ui.lbl_week.setText("Matchday "+str(self.resultweek))
        self.retrieve()
        
if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
