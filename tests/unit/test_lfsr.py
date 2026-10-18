import unittest,random
from sosemanuk.core.lfsr import lfsr_step
from sosemanuk.core.alpha import div_alpha,mul_alpha
class TestLFSR(unittest.TestCase): # Khai báo lớp kiểm thử TestLFSR, kế thừa từ unittest.TestCase
    def test_shift(self):# Hàm kiểm thử phép dịch chuyển của LFSR
        s=list(range(10)); expected=9^div_alpha(3)^mul_alpha(0) # Tính giá trị mong đợi bằng các phép toán trên alpha
        self.assertEqual(lfsr_step(s),0)# Kiểm tra kết quả lfsr_step(s) có bằng 0 hay không
        self.assertEqual(s,list(range(1,10))+[expected]) # Kiểm tra s sau khi dịch: bỏ phần tử đầu và thêm expected vào cuối
    def test_linearity(self): # Hàm kiểm thử tính tuyến tính của phép biến đổi LFSR
        rnd=random.Random(89)# Tạo bộ sinh số ngẫu nhiên với seed 89 để kết quả có thể tái lập
        for _ in range(100): # Lặp lại phép kiểm thử 100 lần

            x=[rnd.getrandbits(32) for i in range(10)] # Tạo danh sách x gồm 10 số nguyên ngẫu nhiên, mỗi số 32 bit
            y=[rnd.getrandbits(32) for i in range(10)] # Tạo danh sách y gồm 10 số nguyên ngẫu nhiên, mỗi số 32 bit
            z=[a^b for a,b in zip(x,y)]# Tạo z bằng phép XOR từng cặp phần tử tương ứng của x và y
            lfsr_step(x);lfsr_step(y);lfsr_step(z) # Thực hiện một bước LFSR trên cả ba danh sách x, y và z
            self.assertEqual(z,[a^b for a,b in zip(x,y)])# Kiểm tra kết quả LFSR có bảo toàn tính tuyến tính hay không

