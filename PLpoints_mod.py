import sys
import os
import sqlite3
from PLpoints_auto import *
from PyQt4 import QtSql, QtCore, QtGui, uic 
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dbfile="PLtable.db"
        self.conn=sqlite3.connect("PLtable.db")
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

    def retrieve(self):
        tablemodel=QtSql.QSqlQueryModel()
        tablemodel.setQuery("select * from PL_table order by Pts desc , GD desc")
        self.ui.tv_Data.setModel(tablemodel)
        
if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
