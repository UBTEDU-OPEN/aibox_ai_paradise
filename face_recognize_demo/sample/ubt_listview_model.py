from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, QVariant, Qt


class MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.listdata = datain


    def rowCount(self, parent=QModelIndex()):
        '''

        :param parent:
        :return:
        '''
        return len(self.listdata)

    def data(self, index, role):
        '''

        :param index:
        :param role:
        :return:
        '''
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()

    def addItem(self, itemData):
        '''

        :param itemData:
        :return:
        '''
        if itemData:
            self.beginInsertRows(QModelIndex(),len(self.listdata),len(self.listdata) + 1)
            self.listdata.append(itemData)
            self.endInsertRows()

    def deleteItem(self, index):
        '''

        :param index:
        :return:
        '''
        self.beginRemoveRows(QModelIndex(),index,index)
        del self.listdata[index]
        self.endRemoveRows()

    def clearItems(self):
        '''

        :return:
        '''
        self.beginRemoveRows(QModelIndex(), 1, len(self.listdata))
        self.listdata = self.listdata[0:1]
        self.endRemoveRows()

    def index_data(self,index):
        '''

        :param index:
        :return:
        '''
        return self.listdata[index]