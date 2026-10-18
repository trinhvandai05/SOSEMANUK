
import unittest  # Import thư viện unittest để viết và chạy các bài kiểm thử tự động

from sosemanuk.core.fsm import trans, mux, fsm_step  # Import 3 hàm: trans (biến đổi trạng thái), mux (hàm chọn/ghép dữ liệu) và fsm_step (thực hiện một bước FSM)

class TestFSM(unittest.TestCase):  # Khai báo lớp TestFSM để chứa các bài kiểm thử FSM

    def test_mux(self):  # Kiểm thử hoạt động của hàm mux
        self.assertEqual(mux(0, 3, 4), 3)  # Kiểm tra mux với tham số đầu là 0 thì kết quả phải bằng 3
        self.assertEqual(mux(1, 3, 4), 7)  # Kiểm tra mux với tham số đầu là 1 thì kết quả phải bằng 7

    def test_old_register_and_f(self):  # Kiểm thử các thanh ghi cũ và giá trị đầu ra f của FSM
        s = [0, 3, 0, 0, 0, 0, 0, 0, 4, 5]  # Khởi tạo danh sách trạng thái s gồm 10 phần tử
        r1, r2, f = fsm_step(1, 2, s)  # Gọi fsm_step với đầu vào 1, 2 và trạng thái s; nhận 3 giá trị trả về r1, r2, f
        self.assertEqual(r1, 9)  # Kiểm tra giá trị thanh ghi r1 trả về phải bằng 9
        self.assertEqual(r2, trans(1))  # Kiểm tra r2 phải bằng kết quả của hàm trans(1)
        self.assertEqual(f, (14 ^ trans(1)))  # Kiểm tra f phải bằng phép XOR giữa 14 và trans(1)
        self.assertNotEqual(r2, trans(r1))  # Kiểm tra r2 khác trans(r1), tức r2 không bằng kết quả trans áp dụng lên r1

    def test_even_branch(self):  # Kiểm thử nhánh xử lý chẵn của FSM
        s = [0, 3, 0, 0, 0, 0, 0, 0, 4, 5]  # Khởi tạo trạng thái s với 10 phần tử
        self.assertEqual(fsm_step(0, 2, s)[0], 5)  # Gọi fsm_step với đầu vào 0, 2 và kiểm tra phần tử trả về đầu tiên bằng 5
