import json
import csv
from datetime import datetime
from typing import List, Optional

class ConNguoi:
    def __init__(self, ho_ten: str, ngay_sinh: str, gioi_tinh: str, que_quan: str, email: str, sdt: str):
        self._ho_ten = ho_ten
        self._ngay_sinh = ngay_sinh
        self._gioi_tinh = gioi_tinh
        self._que_quan = que_quan
        self._email = email
        self._sdt = sdt

    @property
    def ho_ten(self) -> str:
        return self._ho_ten
    @ho_ten.setter
    def ho_ten(self, ho_ten: str):
        self._ho_ten = ho_ten
    @property
    def ngay_sinh(self) -> str:
        return self._ngay_sinh
    @ngay_sinh.setter
    def ngay_sinh(self, ngay_sinh: str):
        self._ngay_sinh = ngay_sinh
    @property
    def gioi_tinh(self) -> str:
        return self._gioi_tinh
    @gioi_tinh.setter
    def gioi_tinh(self, gioi_tinh: str):
        self._gioi_tinh = gioi_tinh
    @property
    def que_quan(self) -> str:
        return self._que_quan
    @que_quan.setter
    def que_quan(self, que_quan: str):
        self._que_quan = que_quan
    @property
    def email(self) -> str:
        return self._email
    @email.setter
    def email(self, email: str):
        self._email = email
    @property
    def sdt(self) -> str:
        return self._sdt
    @sdt.setter
    def sdt(self, sdt: str):
        self._sdt = sdt

class NhanVien(ConNguoi):
    def __init__(self, ma_nv: str, ho_ten: str, ngay_sinh: str, gioi_tinh: str, 
                 que_quan: str, email: str, sdt: str, phong_ban: str, nam_vao_lam: int):
        super().__init__(ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt)
        self._ma_nv = ma_nv
        self._phong_ban = phong_ban
        self._nam_vao_lam = nam_vao_lam

    def to_dict(self) -> dict:
        return {
            "ma_nv": self._ma_nv,
            "ho_ten": self._ho_ten,
            "ngay_sinh": self._ngay_sinh,
            "gioi_tinh": self._gioi_tinh,
            "que_quan": self._que_quan,
            "email": self._email,
            "sdt": self._sdt,
            "phong_ban": self._phong_ban,
            "nam_vao_lam": self._nam_vao_lam
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'NhanVien':
        return cls(
            ma_nv=data["ma_nv"],
            ho_ten=data["ho_ten"],
            ngay_sinh=data["ngay_sinh"],
            gioi_tinh=data["gioi_tinh"],
            que_quan=data["que_quan"],
            email=data["email"],
            sdt=data["sdt"],
            phong_ban=data["phong_ban"],
            nam_vao_lam=data["nam_vao_lam"]
        )

    def __str__(self) -> str:
        return (f"Mã NV: {self._ma_nv}, Họ tên: {self._ho_ten}, "
                f"Ngày sinh: {self._ngay_sinh}, Giới tính: {self._gioi_tinh}, "
                f"Quê quán: {self._que_quan}, Email: {self._email}, "
                f"SĐT: {self._sdt}, Phòng ban: {self._phong_ban}, "
                f"Năm vào làm: {self._nam_vao_lam}")

    @property
    def ma_nv(self) -> str:
        return self._ma_nv
    @ma_nv.setter
    def ma_nv(self, ma_nv: str):
        self._ma_nv = ma_nv
    @property
    def phong_ban(self) -> str:
        return self._phong_ban
    @phong_ban.setter
    def phong_ban(self, phong_ban: str):
        self._phong_ban = phong_ban
    @property
    def nam_vao_lam(self) -> int:
        return self._nam_vao_lam
    @nam_vao_lam.setter
    def nam_vao_lam(self, nam_vao_lam: int):
        self._nam_vao_lam = nam_vao_lam

class DanhSachNhanVien:
    def __init__(self):
        self._ds: List[NhanVien] = []

    def themVao(self, nv: NhanVien) -> None:
        if any(s._ma_nv == nv._ma_nv for s in self._ds):
            raise ValueError("Mã nhân viên đã tồn tại")
        self._ds.append(nv)

    def chinhSua(self, nv: NhanVien) -> None:
        for i, s in enumerate(self._ds):
            if s._ma_nv == nv._ma_nv:
                if nv._ma_nv != s._ma_nv and any(x._ma_nv == nv._ma_nv for x in self._ds):
                    raise ValueError("Mã nhân viên mới đã tồn tại")
                self._ds[i] = nv
                return
        raise ValueError("Không tìm thấy nhân viên")

    def xoaDi(self, ma_nv: str) -> None:
        self._ds = [s for s in self._ds if s._ma_nv != ma_nv]

    def timKiem(self, tu_khoa: str) -> List[NhanVien]:
        tu_khoa = tu_khoa.lower()
        return [s for s in self._ds if tu_khoa in s._ho_ten.lower() or tu_khoa in s._ma_nv]

    def sapXep(self) -> None:
        self._ds.sort(key=lambda x: x._ho_ten)

    def luuVaoTapTin(self, ten_tap_tin: str) -> None:
        with open(ten_tap_tin, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self._ds], f, ensure_ascii=False)
        print(f"Đã lưu danh sách ra {ten_tap_tin}")

    def docTuTapTin(self, ten_tap_tin: str) -> None:
        try:
            with open(ten_tap_tin, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._ds = [NhanVien.from_dict(d) for d in data]
            print(f"Đã tải danh sách từ {ten_tap_tin}")
        except FileNotFoundError:
            print("Không tìm thấy tệp dữ liệu")

    def xuatRaCSV(self, ten_tap_tin: str) -> None:
        with open(ten_tap_tin, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Mã NV", "Họ tên", "Ngày sinh", "Giới tính", "Quê quán", 
                            "Email", "Số điện thoại", "Phòng ban", "Năm vào làm"])
            for nv in self._ds:
                writer.writerow([
                    nv._ma_nv, nv._ho_ten, nv._ngay_sinh, nv._gioi_tinh, nv._que_quan,
                    nv._email, nv._sdt, nv._phong_ban, nv._nam_vao_lam
                ])
        print(f"Đã xuất danh sách ra {ten_tap_tin}")

class DieuKhien:
    def __init__(self):
        self._ds = DanhSachNhanVien()
        self._vai_tro = ""
        self._du_lieu = {}
        self._nguoi_dung = self.docTaiKhoan()

    def docTaiKhoan(self) -> List[dict]:
        try:
            with open("taikhoan.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Không tìm thấy tệp taikhoan.json. Vui lòng tạo tệp với danh sách tài khoản.")
            return []

    def luuTaiKhoan(self) -> None:
        with open("taikhoan.json", "w", encoding="utf-8") as f:
            json.dump(self._nguoi_dung, f, ensure_ascii=False)
        print("Đã lưu danh sách tài khoản vào taikhoan.json")

    def khoi_tao(self, goc, vai_tro="nhanvien") -> None:
        self._vai_tro = vai_tro
        self.taoGiaoDien()

    def taoGiaoDien(self) -> None:
        print("Khởi tạo giao diện dòng lệnh...")

    def layDuLieuNhap(self) -> NhanVien:
        try:
            ma_nv = input("Nhập mã nhân viên: ")
            ho_ten = input("Nhập họ tên: ")
            ngay_sinh = input("Nhập ngày sinh (DD-MM-YYYY): ")
            ngay_sinh = datetime.strptime(ngay_sinh, "%d-%m-%Y").strftime("%d-%m-%Y")
            gioi_tinh = input("Nhập giới tính (Nam/Nu): ")
            if gioi_tinh not in ["Nam", "Nu"]:
                raise ValueError("Giới tính không hợp lệ")
            que_quan = input("Nhập quê quán: ")
            email = input("Nhập email: ")
            sdt = input("Nhập số điện thoại: ")
            phong_ban = input("Nhập phòng ban: ")
            nam_vao_lam = int(input("Nhập năm vào làm: "))
            return NhanVien(ma_nv, ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt, phong_ban, nam_vao_lam)
        except ValueError as e:
            print(f"Lỗi: {str(e)}")
            return None

    def hienThiDanhSach(self) -> None:
        if not self._ds._ds:
            print("Không có nhân viên nào")
        for nv in self._ds._ds:
            print(nv)

    def themNV(self) -> None:
        nv = self.layDuLieuNhap()
        if nv:
            self._ds.themVao(nv)
            print("Thêm nhân viên thành công")

    def chinhSuaNV(self) -> None:
        ma_nv = input("Nhập mã nhân viên cần sửa: ")
        nv = self.layDuLieuNhap()
        if nv:
            nv._ma_nv = ma_nv
            try:
                self._ds.chinhSua(nv)
                print("Sửa nhân viên thành công")
            except ValueError as e:
                print(f"Lỗi: {str(e)}")

    def xoaDiNV(self) -> None:
        ma_nv = input("Nhập mã nhân viên cần xóa: ")
        self._ds.xoaDi(ma_nv)
        print("Xóa nhân viên thành công")

    def timKiemNV(self) -> None:
        tu_khoa = input("Nhập tên hoặc mã nhân viên cần tìm: ")
        ket_qua = self._ds.timKiem(tu_khoa)
        if not ket_qua:
            print("Không tìm thấy nhân viên")
        for nv in ket_qua:
            print(nv)

def chinh():
    dk = DieuKhien()
    
    if not dk._nguoi_dung:
        print("Chương trình không thể chạy vì thiếu tệp tài khoản.")
        return

    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ NHÂN VIÊN ===")
        print("1. Đăng nhập")
        print("2. Thoát")
        try:
            lua_chon = input("Chọn (1-2): ")
        except KeyboardInterrupt:
            print("\nĐã thoát chương trình")
            break

        if lua_chon == "2":
            print("Tạm biệt!")
            break

        if lua_chon != "1":
            print("Lựa chọn không hợp lệ")
            continue

        email = input("Nhập email: ")
        mat_khau = input("Nhập mật khẩu: ")
        for nd in dk._nguoi_dung:
            if nd["email"] == email and nd["mat_khau"] == mat_khau:
                dk.khoi_tao(None, vai_tro=nd["vai_tro"])
                print(f"Đăng nhập thành công: {email} ({nd['vai_tro']})")
                break
        else:
            print("Email hoặc mật khẩu không đúng")
            continue

        while True:
            print("\n=== MENU ===")
            print("1. Xem danh sách nhân viên")
            if dk._vai_tro in ["QuanLy", "Admin"]:
                print("2. Thêm nhân viên")
                print("3. Sửa thông tin nhân viên")
                print("4. Xóa nhân viên")
                print("5. Tìm kiếm nhân viên")
                print("6. Xuất danh sách ra CSV")
                print("7. Lưu dữ liệu")
                print("8. Tải dữ liệu")
            if dk._vai_tro == "Admin":
                print("9. Phân quyền người dùng")
            print("10. Đăng xuất")
            try:
                lua_chon = input("Chọn: ")
            except KeyboardInterrupt:
                print("\nĐã đăng xuất")
                break

            if lua_chon == "10":
                print("Đã đăng xuất")
                break

            if lua_chon == "1":
                dk.hienThiDanhSach()

            elif lua_chon == "2" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk.themNV()

            elif lua_chon == "3" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk.chinhSuaNV()

            elif lua_chon == "4" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk.xoaDiNV()

            elif lua_chon == "5" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk.timKiemNV()

            elif lua_chon == "6" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk._ds.xuatRaCSV("nhanvien.csv")

            elif lua_chon == "7" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk._ds.luuVaoTapTin("nhanvien.json")

            elif lua_chon == "8" and dk._vai_tro in ["QuanLy", "Admin"]:
                dk._ds.docTuTapTin("nhanvien.json")

            elif lua_chon == "9" and dk._vai_tro == "Admin":
                email_moi = input("Nhập email người dùng: ")
                vai_tro_moi = input("Nhập vai trò mới (NhanVien/QuanLy/Admin): ")
                for nd in dk._nguoi_dung:
                    if nd["email"] == email_moi:
                        nd["vai_tro"] = vai_tro_moi
                        dk.luuTaiKhoan()
                        print("Phân quyền thành công")
                        break
                else:
                    print("Không tìm thấy người dùng")

            else:
                print("Lựa chọn không hợp lệ hoặc không có quyền")

if __name__ == "__main__":
    chinh()