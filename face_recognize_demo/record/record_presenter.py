import time

class RecordPresenter:
    def __init__(self, view=None):
        self.view = view
        self.records = []

    def update_records(self, records=None):
        """

        :param records:单条打卡记录
        :return:
        """
        if records.smaple is None:
            return
        self.records.insert(0, records)
        self.view.list_widget.clear()

        temp_records = []

        # 如果不足五条数据，需要占位补全
        if len(self.records) > 5:
            temp_records = self.records[0:5]
        else:
            temp_records = self.records

        for record in temp_records:
            timestruct = time.localtime(record.record_time)
            timetext = time.strftime('%H:%M:%S', timestruct)

            self.view.add_record_item(record.smaple, record.reccordImg, record.name, timetext, record.confirence)
        if len(temp_records) < 5:
            for i in range(5-len(temp_records)):
                self.view.add_default_item()
