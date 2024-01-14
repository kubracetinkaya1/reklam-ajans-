
from PyQt6.QtWidgets import QWidget, QPushButton, QMessageBox, QTableWidgetItem
from system_design import Ui_Form
from connet_db import ConnectDatabase



class SystemWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db = ConnectDatabase()
        self.oyuncu= self.ui.lineEdit_OyuncuAd
        self.yas=self.ui.lineEdit_Yas
        self.deneyim=self.ui.lineEdit_Deneyim
        self.boy=self.ui.lineEdit_Boy


        self.add_btn = self.ui.pushButton_Ekle
        self.update_btn = self.ui.pushButton_Guncelle
        self.select_btn = self.ui.pushButton_Sec
        self.search_btn = self.ui.pushButton_Ara
        self.clear_btn = self.ui.pushButton_Temizle
        self.delete_btn = self.ui.pushButton_Sil

        self.result_table = self.ui.tableWidget
        self.button_list = self.ui.tableWidget.findChildren(QPushButton)
        self.init_signal_slot()
        self.search_info()

    def init_signal_slot(self):
        self.add_btn.clicked.connect(self.add_info)
        self.update_btn.clicked.connect(self.update_info)
        self.delete_btn.clicked.connect(self.delete_info)
        self.select_btn.clicked.connect(self.select_info)
        self.clear_btn.clicked.connect(self.clear_info)
        self.search_btn.clicked.connect(self.search_info)

    def add_info(self):
        # Function to add actor information
        self.disable_buttons()

        oyuncu_info= self.get_oyuncu_info()

        if oyuncu_info ['oyuncu']:
            check_result = self.check_oyuncu(oyuncu=(oyuncu_info['oyuncu']))

            if check_result:
                QMessageBox.information(self, "Warning", "Please input a new oyuncu ID",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return
            add_result = None
            try:
                add_result = self.db.add_info(oyuncu_info)
                print("Kayıt başarıyla eklendi.")
            except Exception as e:
                QMessageBox.information(self, "Warning", f"Add fail: {add_result}, Please try again.",
                                        QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Warning", "Please input oyuncu ID and yas.",
                                    QMessageBox.StandardButton.Ok)

        self.search_info()
        self.enable_buttons()

    def update_info(self):
        new_oyuncu_info = self.get_oyuncu_info()

        if new_oyuncu_info['oyuncu']:
            update_result = self.db.update_info(new_oyuncu_info)

            print(update_result)
            if not update_result:
                QMessageBox.information(self,"Uyarı","Tekrar deneyin",QMessageBox.StandardButton.Ok)
            else:
                self.search_info()
        else:
            QMessageBox.information((self, "Uyari", "oyuncu seçiniz", QMessageBox.StandardButton.Ok))

    def delete_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Dikkat!", "Silmek istediğinize emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            print(selected_option)
            if selected_option == QMessageBox.StandardButton.Yes:
                oyuncu_info = self.result_table.item(select_row,0).text().strip()
                delete_result = self.db.delete_info(oyuncu_info)
                if delete_result:
                    self.search_info()
                else:
                    QMessageBox.information(self, "Uyarı", "Lütfen tekrar deneyin", QMessageBox.StandardButton.Ok)
        else:
            pass

    def  select_info(self):
         # Function to select and populate actor information in the form
         select_row = self.result_table.currentRow()
         self.oyuncu.setEnabled(False)
         if select_row != -1:
            self.oyuncu_info = self.result_table.item(select_row,0).text().strip()
            self.oyuncu.setText(self.oyuncu_info)
            self.yas_info = self.result_table.item(select_row,1).text().strip()
            self.yas.setText(self.yas_info)
            self.deneyim_info = self.result_table.item(select_row,3).text().strip()
            self.deneyim.setText(self.deneyim_info)
            self.boy_info = self.result_table.item(select_row,2).text().strip()
            self.boy.setText(self.boy_info)
            
             

    def  clear_info(self):
          # Function to clear the form
          self.oyuncu.setEnabled(True)
          self.oyuncu.clear()
          self.deneyim.clear()
          self.yas.clear()
          self.boy.clear()
        

    def search_info(self):
         oyuncu_info = self.get_oyuncu_info()
         search_result = self.db.search_info(oyuncu_info)
         self.show_data(search_result)

    def disable_buttons(self):

        for button in self.button_list:
            button.setDisabled(True)

    def enable_buttons(self):

        for button in self.button_list:
            button.setDisabled(False)

    def get_oyuncu_info(self):
        oyuncu = self.oyuncu.text().strip()
        yas = self.yas.text().strip()
        boy = self.boy.text().strip()
        deneyim = self.deneyim.text().strip()
        

        oyuncu_info = {
            'oyuncu': oyuncu,
            'yas': yas,
            'boy': boy,
            'deneyim': deneyim,
        }

        return oyuncu_info

    def check_oyuncu(self, oyuncu):
        result = self.db.get_single_data(oyuncu)
        return result

    def show_data(self, result):
        # Function to populate the table with actor information
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info["oyuncu"],
                    info["yas"],
                    info["boy"],
                    info["deneyim"],
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)

        else:
            self.result_table.setRowCount(0)
            return
