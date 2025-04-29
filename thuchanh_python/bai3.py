import json
import os

class Student:
    def __init__(self, full_name, mssv, class_name, phone, birth_date, current_address):
        self.full_name = full_name
        self.mssv = mssv
        self.class_name = class_name
        self.phone = phone
        self.birth_date = birth_date
        self.current_address = current_address

    def to_dict(self):
        return {
            "Họ tên": self.full_name,
            "MSSV": self.mssv,
            "Lớp": self.class_name,
            "SĐT": self.phone,
            "Ngày sinh": self.birth_date,
            "Địa chỉ hiện tại": self.current_address
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class Family(Student):
    def __init__(self, full_name, mssv, class_name, phone, birth_date, current_address,
                 family_address, father_name, mother_name):
        super().__init__(full_name, mssv, class_name, phone, birth_date, current_address)
        self.family_address = family_address
        self.father_name = father_name
        self.mother_name = mother_name

    def to_dict(self):
        return {
            "Thông tin sinh viên": super().to_dict(),
            "Thông tin gia đình": {
                "Địa chỉ gia đình": self.family_address,
                "Họ tên bố": self.father_name,
                "Họ tên mẹ": self.mother_name
            }
        }

    def update(self, **kwargs):
        super().update(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.students = []
                for item in data:
                    sv = item["Thông tin sinh viên"]
                    gd = item["Thông tin gia đình"]
                    family = Family(
                        sv["Họ tên"], sv["MSSV"], sv["Lớp"], sv["SĐT"], sv["Ngày sinh"], sv["Địa chỉ hiện tại"],
                        gd["Địa chỉ gia đình"], gd["Họ tên bố"], gd["Họ tên mẹ"]
                    )
                    self.students.append((item["id"], family))

    def save(self):
        data = [{"id": id, **student.to_dict()} for id, student in self.students]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_student(self, family: Family):
        new_id = 1 if not self.students else max(s[0] for s in self.students) + 1
        self.students.append((new_id, family))
        self.save()

    def delete_student(self, student_id):
        self.students = [s for s in self.students if s[0] != student_id]
        self.save()

    def update_student(self, student_id, **kwargs):
        for i, (id, student) in enumerate(self.students):
            if id == student_id:
                student.update(**kwargs)
                self.students[i] = (id, student)
                self.save()
                break

    def list_students(self):
        for id, student in self.students:
            print(f"ID: {id}")
            print(json.dumps(student.to_dict(), indent=4, ensure_ascii=False))
            print("—" * 40)

# === Ví dụ sử dụng chương trình ===
if __name__ == "__main__":
    manager = StudentManager()

    # Thêm một sinh viên mới
    sv1 = Family(
        "Nguyễn Văn A", "123456", "CNTT1", "0123456789", "01/01/2000", "TPHCM",
        "Long An", "Nguyễn Văn B", "Trần Thị C"
    )
    manager.add_student(sv1)

    # Hiển thị danh sách
    manager.list_students()

    # Cập nhật sinh viên ID = 1
    manager.update_student(1, phone="0999888777")

    # Xóa sinh viên ID = 1
    # manager.delete_student(1)
