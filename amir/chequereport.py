import gi
from gi.repository import Gtk

from sqlalchemy import or_
from sqlalchemy.orm.util import outerjoin
from sqlalchemy.sql import between, and_
from sqlalchemy.sql.functions import sum

from database import *
from dateentry import *
from share import share
from helpers import get_builder
from gi.repository import Gdk
from converter import *
from datetime import datetime, timedelta
import dateentry
import class_document
import dbconfig
import subjects

dbconf = dbconfig.dbConfig()
config = share.config

class ChequeReport:
    def __init__(self):
        self.builder = get_builder("chequereport")
        self.window = self.builder.get_object("windowChequeReport")
        
        self.treeviewIncoming = self.builder.get_object("treeviewIncoming")
        self.treeviewOutgoing = self.builder.get_object("treeviewOutgoing")
        self.treeviewDeleted = self.builder.get_object("treeviewDeleted")
        self.treestoreIncoming = Gtk.TreeStore(str, str, str, str, str, str, str, str, str, str, str, str, str)
        self.treestoreOutgoing = Gtk.TreeStore(str, str, str, str, str, str, str, str, str, str, str, str, str)
        self.treestoreDeleted = Gtk.TreeStore(str, str, str, str, str, str, str, str, str, str, str, str, str)
        self.treeviewIncoming.set_model(self.treestoreIncoming)
        self.treeviewOutgoing.set_model(self.treestoreOutgoing)
        self.treeviewDeleted.set_model(self.treestoreDeleted)

        column = Gtk.TreeViewColumn(_("ID"), Gtk.CellRendererText(), text = 0)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(0)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("ID"), Gtk.CellRendererText(), text = 0)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(0)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("ID"), Gtk.CellRendererText(), text = 0)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(0)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Amount"), Gtk.CellRendererText(), text = 1)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Amount"), Gtk.CellRendererText(), text = 1)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Amount"), Gtk.CellRendererText(), text = 1)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Write Date"), Gtk.CellRendererText(), text = 2)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(2)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Write Date"), Gtk.CellRendererText(), text = 2)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(2)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Write Date"), Gtk.CellRendererText(), text = 2)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(2)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Due Date"), Gtk.CellRendererText(), text = 3)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Due Date"), Gtk.CellRendererText(), text = 3)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Due Date"), Gtk.CellRendererText(), text = 3)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Serial"), Gtk.CellRendererText(), text = 4)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(4)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Serial"), Gtk.CellRendererText(), text = 4)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(4)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Serial"), Gtk.CellRendererText(), text = 4)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(4)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Clear"), Gtk.CellRendererText(), text = 5)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(5)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Clear"), Gtk.CellRendererText(), text = 5)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(5)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Clear"), Gtk.CellRendererText(), text = 5)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(5)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)
        
        column = Gtk.TreeViewColumn(_("Customer Name"), Gtk.CellRendererText(), text = 6)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(6)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Customer Name"), Gtk.CellRendererText(), text = 6)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(6)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Customer Name"), Gtk.CellRendererText(), text = 6)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(6)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Account"), Gtk.CellRendererText(), text = 7)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(7)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Account"), Gtk.CellRendererText(), text = 7)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(7)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Account"), Gtk.CellRendererText(), text = 7)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(7)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Transaction ID"), Gtk.CellRendererText(), text = 8)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(8)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Transaction ID"), Gtk.CellRendererText(), text = 8)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(8)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Transaction ID"), Gtk.CellRendererText(), text = 8)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(8)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Note Book ID"), Gtk.CellRendererText(), text = 9)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(9)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Note Book ID"), Gtk.CellRendererText(), text = 9)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(9)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Note Book ID"), Gtk.CellRendererText(), text = 9)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(9)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Description"), Gtk.CellRendererText(), text = 10)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(10)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Description"), Gtk.CellRendererText(), text = 10)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(10)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Description"), Gtk.CellRendererText(), text = 10)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(10)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)

        column = Gtk.TreeViewColumn(_("Bill ID"), Gtk.CellRendererText(), text = 12)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(12)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Bill ID"), Gtk.CellRendererText(), text = 12)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(12)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Bill ID"), Gtk.CellRendererText(), text = 12)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(12)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)
        
        column = Gtk.TreeViewColumn(_("Order"), Gtk.CellRendererText(), text = 13)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(13)
        column.set_sort_indicator(True)
        self.treeviewIncoming.append_column(column)
        column = Gtk.TreeViewColumn(_("Order"), Gtk.CellRendererText(), text = 13)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(13)
        column.set_sort_indicator(True)
        self.treeviewOutgoing.append_column(column)
        column = Gtk.TreeViewColumn(_("Order"), Gtk.CellRendererText(), text = 13)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(13)
        column.set_sort_indicator(True)
        self.treeviewDeleted.append_column(column)
        
        self.treeviewIncoming.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self.treeviewOutgoing.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self.treeviewDeleted.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        #self.treestore.set_sort_func(0, self.sortGroupIds)
        # self.treestore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.window.show_all()
        self.builder.connect_signals(self)

        self.dateFromEntry = self.builder.get_object("dateFromSearchentry")
        self.dateToEntry = self.builder.get_object("dateToSearchentry")
        if share.config.datetypes[share.config.datetype] == "jalali":
            self.dateToEntry.set_placeholder_text("1396:1:1")
            self.dateFromEntry.set_placeholder_text("1396:1:1")
        else:
            self.dateToEntry.set_placeholder_text("1:1:2018")
            self.dateFromEntry.set_placeholder_text("1:1:2018")

        self.dateFromEntry = self.builder.get_object("dateFromSearchentry")
        self.dateToEntry = self.builder.get_object("dateToSearchentry")
        if share.config.datetypes[share.config.datetype] == "jalali":
            self.dateToEntry.set_placeholder_text("1396:1:1")
            self.dateFromEntry.set_placeholder_text("1396:1:1")
        else:
            self.dateToEntry.set_placeholder_text("1:1:2018")
            self.dateFromEntry.set_placeholder_text("1:1:2018")

        self.showResult()
        self.date_entry = dateentry.DateEntry()
        self.current_time = self.date_entry.getDateObject()

    def searchFilter(self, sender=None):
        box = self.builder.get_object("idSearchentry")
        chequeId = box.get_text()

        box = self.builder.get_object("serialSearchentry")
        chqSerial = box.get_text()

        box = self.builder.get_object("amountFromSearchentry")
        amountFrom = box.get_text()

        box = self.builder.get_object("amountToSearchentry")
        amountTo = box.get_text()

        box = self.builder.get_object("dateFromSearchentry")
        dateFrom = box.get_text()

        box = self.builder.get_object("dateToSearchentry")
        dateTo = box.get_text()
        self.showResult(chequeId, chqSerial, amountFrom, amountTo, dateFrom, dateTo)

    def showResult(self, chequeId=None, chqSerial=None, amountFrom=None, amountTo=None, dateFrom=None, dateTo=None):
        self.treestoreIncoming.clear()
        self.treestoreOutgoing.clear()
        result = config.db.session.query(Cheque, Customers)
        result = result.filter(Customers.custId == Cheque.chqCust)
        # Apply filters
        if chequeId:
            result = result.filter(Cheque.chqId == chequeId)
        if chqSerial:
            result = result.filter(Cheque.chqSerial == chqSerial)
        if amountFrom:
            result = result.filter(Cheque.chqAmount >= amountFrom)
        if amountTo:
            result = result.filter(Cheque.chqAmount <= amountTo)
        if share.config.datetypes[share.config.datetype] == "jalali":
            if dateTo:
                year, month, day = str(dateTo).split(":")
                e=jalali_to_gregorian(int(year),int(month),int(day))
                dateTo = datetime(e[0], e[1], e[2])
            if dateFrom:
                year, month, day = dateFrom.split(":")
                e=jalali_to_gregorian(int(year),int(month),int(day))
                dateFrom = datetime(e[0], e[1], e[2])
        else:
            if dateTo:
                year, month, day = str(dateTo).split(":")
                dateTo = datetime(int(day),int(month),int(year))
            if dateFrom:
                year, month, day = dateFrom.split(":")
                dateFrom = datetime(int(day),int(month),int(year))

        if dateTo:
            result = result.filter(Cheque.chqDueDate <= dateTo)
        if dateFrom:
            DD = timedelta(days=1)
            dateFrom -= DD
            result = result.filter(Cheque.chqDueDate >= dateFrom)

        # Show
        for cheque,customer in result:
            if share.config.datetypes[share.config.datetype] == "jalali": 
                year, month, day = str(cheque.chqWrtDate).split("-")
                chqWrtDate = gregorian_to_jalali(int(year),int(month),int(day))
                chqWrtDate = str(chqWrtDate[0]) + '-' + str(chqWrtDate[1]) + '-' + str(chqWrtDate[2])

                year, month, day = str(cheque.chqWrtDate).split("-")
                chqDueDate = gregorian_to_jalali(int(year),int(month),int(day))
                chqDueDate = str(chqDueDate[0]) + '-' + str(chqDueDate[1]) + '-' + str(chqDueDate[2])

            else:
                year, month, day = str(cheque.chqWrtDate).split("-")
                chqWrtDate = str(day) + '-' + str(month) + '-' + str(year)

                year, month, day = str(cheque.chqDueDate).split("-")
                chqDueDate = str(day) + '-' + str(month) + '-' + str(year)

            if (cheque.chqStatus == 2) or (cheque.chqStatus == 3):
                clear = 'Cleared'
            else:
                clear = 'Not Cleared'

            if cheque.chqDelete == False:
                if (cheque.chqStatus == 3) or (cheque.chqStatus == 4) or (cheque.chqStatus == 7):
                    self.treestoreIncoming.append(None, (str(cheque.chqId), str(cheque.chqAmount), str(chqWrtDate), str(chqDueDate), str(cheque.chqSerial), str(clear), str(customer.custName), str(cheque.chqAccount), str(cheque.chqTransId), str(cheque.chqNoteBookId), str(cheque.chqDesc), str(cheque.chqBillId), str(cheque.chqOrder)))
                else:
                    self.treestoreOutgoing.append(None, (str(cheque.chqId), str(cheque.chqAmount), str(chqWrtDate), str(chqDueDate), str(cheque.chqSerial), str(clear), str(customer.custName), str(cheque.chqAccount), str(cheque.chqTransId), str(cheque.chqNoteBookId), str(cheque.chqDesc), str(cheque.chqBillId), str(cheque.chqOrder)))
            else:
                self.treestoreDeleted.append(None, (str(cheque.chqId), str(cheque.chqAmount), str(chqWrtDate), str(chqDueDate), str(cheque.chqSerial), str(clear), str(customer.custName), str(cheque.chqAccount), str(cheque.chqTransId), str(cheque.chqNoteBookId), str(cheque.chqDesc), str(cheque.chqBillId), str(cheque.chqOrder)))

    def getSelection(self):
        selection = self.treeviewOutgoing.get_selection()
        iter = selection.get_selected()[1]
        if iter != None :
            self.code = convertToLatin(self.treestoreOutgoing.get(iter, 0)[0])
        else:
            selection = self.treeviewIncoming.get_selection()
            iter = selection.get_selected()[1]
            if iter != None :
                self.code = convertToLatin(self.treestoreIncoming.get(iter, 0)[0])
            else:
                selection = self.treeviewDeleted.get_selection()
                iter = selection.get_selected()[1]
                if iter != None :
                    self.code = convertToLatin(self.treestoreDeleted.get(iter, 0)[0])

    def odatAzMoshtari(self, sender):
        self.getSelection()
        result = config.db.session.query(Cheque)
        result = result.filter(Cheque.chqId == self.code).first()
        result.chqStatus = 6
        ch_history = ChequeHistory(result.chqId, result.chqAmount, result.chqWrtDate, result.chqDueDate, result.chqSerial, result.chqStatus, result.chqCust, result.chqAccount, result.chqTransId, result.chqDesc, self.current_time)
        config.db.session.add(ch_history)
        config.db.session.commit()
        share.mainwin.silent_daialog(_("The operation was completed successfully."))
        self.searchFilter()

    def odatBeMoshtari(self, sender):
        self.getSelection()
        result = config.db.session.query(Cheque, Customers)
        result = result.filter(Customers.custId == Cheque.chqCust)
        result = result.filter(Cheque.chqId == self.code).first()
        result.Cheque.chqStatus = 7
        ch_history = ChequeHistory(result.Cheque.chqId, result.Cheque.chqAmount, result.Cheque.chqWrtDate, result.Cheque.chqDueDate, result.Cheque.chqSerial, result.Cheque.chqStatus, result.Cheque.chqCust, result.Cheque.chqAccount, result.Cheque.chqTransId, result.Cheque.chqDesc, self.current_time)
        config.db.session.add(ch_history)
        config.db.session.commit()

        document = class_document.Document()
        document.add_notebook(result.Customers.custSubj  , result.Cheque.chqAmount, _('Odat cheque'))
        document.add_notebook(dbconf.get_int('other_cheque'), -result.Cheque.chqAmount, _('Odat cheque'))
        document.save()

        config.db.session.commit()
        share.mainwin.silent_daialog(_("The operation was completed successfully."))
        self.searchFilter()

    def bargasht(self, sender):
        self.getSelection()
        result = config.db.session.query(Cheque, Customers)
        result = result.filter(Customers.custId == Cheque.chqCust)
        result = result.filter(Cheque.chqId == self.code).first()
        result.Cheque.chqStatus = 8
        ch_history = ChequeHistory(result.Cheque.chqId, result.Cheque.chqAmount, result.Cheque.chqWrtDate, result.Cheque.chqDueDate, result.Cheque.chqSerial, result.Cheque.chqStatus, result.Cheque.chqCust, result.Cheque.chqAccount, result.Cheque.chqTransId, result.Cheque.chqDesc, self.current_time)
        config.db.session.add(ch_history)
        config.db.session.commit()

        document = class_document.Document()
        document.add_notebook(result.Customers.custSubj  , result.Cheque.chqAmount, _('Bargasht cheque'))
        document.add_notebook(58, -result.Cheque.chqAmount, _('Bargasht cheque'))
        document.save()

        config.db.session.commit()
        share.mainwin.silent_daialog(_("The operation was completed successfully."))
        self.searchFilter()

    def passShode(self, sender):
        self.getSelection()
        result = config.db.session.query(Cheque, Customers)
        result = result.filter(Customers.custId == Cheque.chqCust)
        result = result.filter(Cheque.chqId == self.code).first()
        if result.Cheque.chqStatus == 4:
            sub = subjects.Subjects(parent_id=[1,14])
            sub.connect('subject-selected', self.on_subject_selected)
        if result.Cheque.chqStatus == 1:
            result.Cheque.chqStatus = 2
            ch_history = ChequeHistory(result.Cheque.chqId, result.Cheque.chqAmount, result.Cheque.chqWrtDate, result.Cheque.chqDueDate, result.Cheque.chqSerial, result.Cheque.chqStatus, result.Cheque.chqCust, result.Cheque.chqAccount, result.Cheque.chqTransId, result.Cheque.chqDesc, self.current_time)
            config.db.session.add(ch_history)
            config.db.session.commit()
            document = class_document.Document()
            document.add_notebook(result.Customers.custSubj, -result.Cheque.chqAmount, _('Pass shode'))
            document.add_notebook(dbconf.get_int('our_cheque'), -result.Cheque.chqAmount, _('Pass shode'))
            document.save()
            share.mainwin.silent_daialog(_("The operation was completed successfully."))
            self.searchFilter()

    def on_subject_selected(self, subject, id, code, name):
        result = config.db.session.query(Cheque, Customers)
        result = result.filter(Customers.custId == Cheque.chqCust)
        result = result.filter(Cheque.chqId == self.code).first()
        result.Cheque.chqStatus = 3
        ch_history = ChequeHistory(result.Cheque.chqId, result.Cheque.chqAmount, result.Cheque.chqWrtDate, result.Cheque.chqDueDate, result.Cheque.chqSerial, result.Cheque.chqStatus, result.Cheque.chqCust, result.Cheque.chqAccount, result.Cheque.chqTransId, result.Cheque.chqDesc, self.current_time)
        config.db.session.add(ch_history)
        config.db.session.commit()

        document = class_document.Document()
        document.add_notebook(result.Customers.custSubj  , result.Cheque.chqAmount, _('Pass shode'))
        document.add_notebook(id, result.Cheque.chqAmount, _('Pass shode'))
        document.add_notebook(dbconf.get_int('other_cheque'), -result.Cheque.chqAmount, _('Pass shode'))
        document.save()
        subject.window.destroy()
        share.mainwin.silent_daialog(_("The operation was completed successfully."))

    def on_dialog_destroy(self, sender):
        self.dialog.hide()

    def selectChequeFromListIncoming(self, treeview, path, view_column):
        selection = self.treeviewIncoming.get_selection()
        iter = selection.get_selected()[1]
        
        if iter != None :
            self.code = convertToLatin(self.treestoreIncoming.get(iter, 0)[0])
            self.showHistory(self.code)

    def selectChequeFromListOutgoing(self, treeview, path, view_column):
        selection = self.treeviewOutgoing.get_selection()
        iter = selection.get_selected()[1]
        
        if iter != None :
            self.code = convertToLatin(self.treestoreOutgoing.get(iter, 0)[0])
            self.showHistory(self.code)

    def selectChequeFromListDeleted(self, treeview, path, view_column):
        selection = self.treeviewOutgoing.get_selection()
        iter = selection.get_selected()[1]
        
        if iter != None :
            self.code = convertToLatin(self.treestoreOutgoing.get(iter, 0)[0])
            self.showHistory(self.code)

    def showHistory(self, code):
        self.window = self.builder.get_object("window1")
        
        self.treeviewHistory = self.builder.get_object("treeviewHistory")
        self.treestoreHistory = Gtk.TreeStore(str, str, str, str, str, str, str, str, str, str, str)
        self.treeviewHistory.set_model(self.treestoreHistory)

        column = Gtk.TreeViewColumn(_("ID"), Gtk.CellRendererText(), text = 0)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(0)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Amount"), Gtk.CellRendererText(), text = 1)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(4)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Write Date"), Gtk.CellRendererText(), text = 2)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(5)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Due Date"), Gtk.CellRendererText(), text = 3)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(5)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Serial"), Gtk.CellRendererText(), text = 4)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Clear"), Gtk.CellRendererText(), text = 5)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)
        
        column = Gtk.TreeViewColumn(_("Customer Name"), Gtk.CellRendererText(), text = 6)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Account"), Gtk.CellRendererText(), text = 7)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Transaction ID"), Gtk.CellRendererText(), text = 8)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Note Book ID"), Gtk.CellRendererText(), text = 9)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(2)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Description"), Gtk.CellRendererText(), text = 10)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("History ID"), Gtk.CellRendererText(), text = 11)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)

        column = Gtk.TreeViewColumn(_("Bill ID"), Gtk.CellRendererText(), text = 12)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)
        
        column = Gtk.TreeViewColumn(_("Order"), Gtk.CellRendererText(), text = 13)
        column.set_spacing(5)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        column.set_sort_indicator(True)
        self.treeviewHistory.append_column(column)
        
        # self.treeviewHistory.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        #self.treestore.set_sort_func(0, self.sortGroupIds)
        # self.treestore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.window.show_all()
        self.builder.connect_signals(self)

        self.treestoreHistory.clear()
        result = config.db.session.query(ChequeHistory, Customers)
        result = result.filter(ChequeHistory.ChequeId == code)
        result = result.filter(Customers.custId == ChequeHistory.Cust)

        # Show
        for cheque,customer in result:
            if share.config.datetypes[share.config.datetype] == "jalali": 
                year, month, day = str(cheque.WrtDate).split("-")
                chqWrtDate = gregorian_to_jalali(int(year),int(month),int(day))
                chqWrtDate = str(chqWrtDate[0]) + '-' + str(chqWrtDate[1]) + '-' + str(chqWrtDate[2])

                year, month, day = str(cheque.DueDate).split("-")
                DueDate = gregorian_to_jalali(int(year),int(month),int(day))
                chqDueDate = str(DueDate[0]) + '-' + str(DueDate[1]) + '-' + str(DueDate[2])

            else:
                year, month, day = str(cheque.WrtDate).split("-")
                chqWrtDate = str(day) + '-' + str(month) + '-' + str(year)

                year, month, day = str(cheque.DueDate).split("-")
                chqDueDate = str(day) + '-' + str(month) + '-' + str(year)

            if (cheque.Status == 2) or (cheque.Status == 3):
                clear = 'Cleared'
            else:
                clear = 'Not Cleared'

            self.treestoreHistory.append(None, (str(cheque.ChequeId), str(cheque.Amount), str(chqWrtDate), str(chqDueDate), str(cheque.Serial), str(clear), str(customer.custName), str(cheque.Account), str(cheque.TransId), str(cheque.TransId), str(cheque.Desc)))
    def on_select_cell(self, sender):
        my_button = self.builder.get_object("odatAsMoshtariButton")
        my_button.set_sensitive(True)
        my_button = self.builder.get_object("odatBeMoshtariButton")
        my_button.set_sensitive(True)
        my_button = self.builder.get_object("bargashtButton")
        my_button.set_sensitive(True)
        my_button = self.builder.get_object("passButton")
        my_button.set_sensitive(True)
        self.getSelection()
        result = config.db.session.query(Cheque)
        result = result.filter(Cheque.chqId == self.code).first()
        if result.chqStatus in [2,3,4,5,6,7,8]:
            my_button = self.builder.get_object("odatAsMoshtariButton")
            my_button.set_sensitive(False)
        if result.chqStatus in [1,2,3,5,6,7,8]:
            my_button = self.builder.get_object("odatBeMoshtariButton")
            my_button.set_sensitive(False)
        if result.chqStatus in [1,2,3,5,6,7,8]:
            my_button = self.builder.get_object("bargashtButton")
            my_button.set_sensitive(False)
        if result.chqStatus in [2,3,6,7,8]:
            my_button = self.builder.get_object("passButton")
            my_button.set_sensitive(False)
        if result.chqDelete == True:
            my_button = self.builder.get_object("deleteButton")
            my_button.set_sensitive(False)
    def on_delete(self, sender):
        self.getSelection()
        result = config.db.session.query(Cheque)
        result = result.filter(Cheque.chqId == self.code).first()
        result.chqDelete = True
        ch_history = ChequeHistory(result.chqId, result.chqAmount, result.chqWrtDate, result.chqDueDate, result.chqSerial, result.chqStatus, result.chqCust, result.chqAccount, result.chqTransId, result.chqDesc, self.current_time, result.chqDelete)
        config.db.session.add(ch_history)
        config.db.session.commit()

        share.mainwin.silent_daialog(_("The operation was completed successfully."))
        self.searchFilter()