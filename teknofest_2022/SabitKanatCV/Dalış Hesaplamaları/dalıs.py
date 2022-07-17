import math
import pandas as pd
class Dalis:
    def __init__(self):
        self.sabit_ucus_hizi = 15 # +x m/s
        self.sabit_ucus_irtifasi = 20 # m
        self.dalinacak_irtifa = 13 # m
        self.dalis_süresi = 1 # s
        self.max_ruzgar_hizi = 10.2 # ? m/s
        self.yercekimi_ivmesi = 9.8 # m/s^2 -z
    def dusme_suresi_hesapla(self):
        self.dikey_hiz = self.dalinacak_irtifa / self.dalis_süresi # m/s -z
        delta = self.dikey_hiz**2 + 2*self.yercekimi_ivmesi*self.dalinacak_irtifa
        self.dusme_suresi = ((-1*self.dikey_hiz) + delta**(1/2)) / self.yercekimi_ivmesi
        self.dalissiz_dusme_suresi = (2*self.sabit_ucus_irtifasi/self.yercekimi_ivmesi)**(1/2)
        self.dalissiz_alcakirtifa_dusme_suresi = (2*self.dalinacak_irtifa/self.yercekimi_ivmesi)**(1/2)
    def yatay_sapma_hesapla(self):
        max_hiz = self.sabit_ucus_hizi + self.max_ruzgar_hizi
        min_hiz = self.sabit_ucus_hizi - self.max_ruzgar_hizi
        self.max_sapma = max_hiz * self.dusme_suresi
        self.min_sapma = min_hiz * self.dusme_suresi
        self.dalissiz_sapma = self.max_ruzgar_hizi * self.dalissiz_dusme_suresi
        self.dalissiz_alcakirtifa_sapma = self.max_ruzgar_hizi * self.dalissiz_alcakirtifa_dusme_suresi
    def output(self):
        data_list = [[self.dusme_suresi, self.max_sapma, self.min_sapma,
                    self.dalissiz_dusme_suresi, self.dalissiz_sapma,
                    self.dalissiz_alcakirtifa_dusme_suresi, self.dalissiz_alcakirtifa_sapma,
                    self.max_ruzgar_hizi, self.dalis_süresi]]
        data_names = ["Dalışlı Düşme Süresi","Dalışlı Max Sapma","Dalışlı Min Sapma",
                    "Dalışsız Düşme Süresi", "Dalışsız Sapma",
                    "Dalışsız Alçalarak Düşme Süresi","Dalışsız Alçalarak Sapma",
                    "Öngörülen Max Rüzgar Hızı","Dalış Süresi"]
        return data_list, data_names
    def main(self):
        self.dusme_suresi_hesapla()
        self.yatay_sapma_hesapla()
        data, names = self.output()
        df = pd.DataFrame(data =data, columns=names)
        return df

if __name__ == "__main__":
    calc = Dalis()
    print(calc.main())        