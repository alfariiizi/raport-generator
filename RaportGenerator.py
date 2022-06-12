import pandas as pd
import numpy as np
import random as rd

# This piece of code is taken from Raport-Generator2.ipynb

class RaportGenerator:
    def __init__(self, path_to_file: str, n_cols: int, generate_oneliner=True):
        self.path_to_file = path_to_file
        self.n_cols = n_cols
        self.df = pd.read_csv(path_to_file, names=['Nama', 'Nilai'])
        self.generator()
        self.update_df()
        self.generate_oneliner = generate_oneliner
        if generate_oneliner:
            self.one_liner_value()

    def generator(self):
        output = []
        rata = []
        for i in self.df.loc[:, 'Nilai']:
            notGood = True  # flag, to make sure that the value of averange value is close to the value that I want
            buff = []		# store value for each row
            averange = 0.0  # store averange value

            while(notGood):
                buff.clear()
                for j in range(self.n_cols): # 10 adalah panjang ke kanan nya
                    value = 0		# buffer for to make sure that the value that want to append is greater than the KKM
                    while True:
                        rand_number = 0
                        if i > 76:
                            rand_number = rd.randint(-2, 2)
                        elif i == 76:  # 75 adalah KKM nya, sehingga jika siswa nilainya 75, maka tidak akan diproses
                            rand_number = rd.randint(-1, 1)
                        else:  # siswa yang nilai rata - rata nya sama dengan KKM atau kurang dari KKM
                            rand_number = 0

                        value = int(i) + rand_number
                        if (i >= 75 and value >= 75) or i < 75:
                            break

                    buff.append(value)
                averange = sum(buff) / len(buff)
                if averange == i:
                    notGood = False

            output.append(buff)
            rata.append(averange)
            
        self.value = np.array(output)
        self.rata = rata

    def _name_generator_(self, const_name):
        name = []
        counter = 1
        for i in range(self.n_cols):
            name.append( const_name + "-" + str(counter) )
            counter += 1
        return name
    
    def update_df(self):
        nama = self._name_generator_('KD')
        for i in range(self.n_cols):
            self.df[nama[i]] = self.value[:,i]
    
    def one_liner_value(self):
        self.value_in_one_column = []
        for i in range(self.n_cols):
            for j in self.value[:,i]:
                self.value_in_one_column.append(j)
        
    def save_as_csv(self, save_name):
        self.df.to_csv(f'Generate - {save_name}.csv')
        if self.generate_oneliner:
            pd.DataFrame(self.value_in_one_column).to_csv(f"One_liner - {save_name}.csv")