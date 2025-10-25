import os
import struct
from pathlib import Path

# ------------------------------------------------------------
# إعدادات الصفحة
# ------------------------------------------------------------
PAGE_SIZE = 4096           # حجم الصفحة بالبايت
FOOTER_SIZE = 4            # آخر 4 بايت (2 free_offset + 2 slot_count)
SLOT_SIZE = 4              # كل فتحة (slot) = 2 offset + 2 length


# ------------------------------------------------------------
# دوال مساعدة للصفحة
# ------------------------------------------------------------

def new_empty_page():
    """إنشاء صفحة جديدة فارغة (كلها أصفار) مع تهيئة الـ footer."""
    page = bytearray(PAGE_SIZE)
    struct.pack_into('<H', page, PAGE_SIZE - FOOTER_SIZE, 0)         # free_offset = 0
    struct.pack_into('<H', page, PAGE_SIZE - FOOTER_SIZE + 2, 0)     # slot_count = 0
    return bytes(page)


def read_footer(page_data):
    """قراءة footer الصفحة وإرجاع (free_offset, slot_count)."""
    if len(page_data) != PAGE_SIZE:
        raise ValueError("page_data must be PAGE_SIZE bytes")
    free_offset = struct.unpack_from('<H', page_data, PAGE_SIZE - FOOTER_SIZE)[0]
    slot_count = struct.unpack_from('<H', page_data, PAGE_SIZE - FOOTER_SIZE + 2)[0]
    return free_offset, slot_count


def write_footer(page, free_offset, slot_count):
    """كتابة قيم footer الجديدة داخل الصفحة."""
    struct.pack_into('<H', page, PAGE_SIZE - FOOTER_SIZE, free_offset)
    struct.pack_into('<H', page, PAGE_SIZE - FOOTER_SIZE + 2, slot_count)


def slot_position(slot_index):
    """حساب موضع فتحة معينة (index يبدأ من 0)."""
    return PAGE_SIZE - FOOTER_SIZE - (slot_index + 1) * SLOT_SIZE


def read_slot(page_data, slot_index):
    """قراءة فتحة معينة من الصفحة (offset, length)."""
    pos = slot_position(slot_index)
    off = struct.unpack_from('<H', page_data, pos)[0]
    length = struct.unpack_from('<H', page_data, pos + 2)[0]
    return off, length


def write_slot(page, slot_index, off, length):
    """كتابة بيانات فتحة (offset, length) داخل الصفحة."""
    pos = slot_position(slot_index)
    struct.pack_into('<H', page, pos, off)
    struct.pack_into('<H', page, pos + 2, length)


# ------------------------------------------------------------
# الوظائف المطلوبة في المشروع
# ------------------------------------------------------------

def Calculate_free_space(page_data):
    """حساب المساحة الخالية داخل الصفحة (بايت)."""
    free_offset, slot_count = read_footer(page_data)
    slot_table_start = PAGE_SIZE - FOOTER_SIZE - slot_count * SLOT_SIZE
    free_bytes_for_data = slot_table_start - free_offset
    return free_bytes_for_data


def insert_record_data_to_page_data(page_data, record_data):
    """
    إدراج سجل جديد داخل الصفحة.
    تُرجع (page_bytes_after_insert, record_id)
    وترفع ValueError إذا لم توجد مساحة كافية.
    """
    if not isinstance(record_data, (bytes, bytearray)):
        raise TypeError("record_data must be bytes-like")

    free_offset, slot_count = read_footer(page_data)
    slot_table_start = PAGE_SIZE - FOOTER_SIZE - slot_count * SLOT_SIZE
    required_for_data = len(record_data)
    required_total = required_for_data + SLOT_SIZE
    free_bytes = slot_table_start - free_offset

    if free_bytes < required_total:
        raise ValueError("Not enough free space in page")

    # نسخ الصفحة لكتابة البيانات
    page = bytearray(page_data)

    # كتابة السجل في مكانه الجديد
    page[free_offset:free_offset + required_for_data] = record_data

    # إنشاء فتحة جديدة
    write_slot(page, slot_count, free_offset, required_for_data)

    # تحديث footer
    new_free_offset = free_offset + required_for_data
    new_slot_count = slot_count + 1
    write_footer(page, new_free_offset, new_slot_count)

    return bytes(page), slot_count  # record_id = رقم الفتحة الجديدة


def get_record_from_page(page_data, record_id):
    """قراءة سجل واحد من الصفحة بناءً على record_id."""
    free_offset, slot_count = read_footer(page_data)
    if record_id < 0 or record_id >= slot_count:
        raise IndexError("record_id out of range")
    off, length = read_slot(page_data, record_id)
    return bytes(page_data[off: off + length])


def get_all_record_from_page(page_data):
    """إرجاع كل السجلات داخل الصفحة كقائمة."""
    free_offset, slot_count = read_footer(page_data)
    return [get_record_from_page(page_data, i) for i in range(slot_count)]


def insert_record_to_file(file_name, record_data):
    """
    إدراج سجل داخل أول صفحة بها مساحة كافية.
    إذا لم توجد، تُنشأ صفحة جديدة.
    تُرجع (page_number, record_id).
    """
    Path(file_name).parent.mkdir(parents=True, exist_ok=True)
    required_total = len(record_data) + SLOT_SIZE

    # إذا الملف غير موجود أو فارغ
    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        page = new_empty_page()
        page, rec_id = insert_record_data_to_page_data(page, record_data)
        with open(file_name, 'wb') as f:
            f.write(page)
        return 0, rec_id

    # الملف موجود
    with open(file_name, 'r+b') as f:
        f.seek(0, os.SEEK_END)
        total_size = f.tell()
        page_count = total_size // PAGE_SIZE

        # البحث عن صفحة فيها مساحة كافية
        for p in range(page_count):
            f.seek(p * PAGE_SIZE)
            page = f.read(PAGE_SIZE)
            free_bytes = Calculate_free_space(page)
            if free_bytes >= required_total:
                new_page, rec_id = insert_record_data_to_page_data(page, record_data)
                f.seek(p * PAGE_SIZE)
                f.write(new_page)
                return p, rec_id

        # لا توجد صفحة مناسبة → إضافة صفحة جديدة
        page = new_empty_page()
        page, rec_id = insert_record_data_to_page_data(page, record_data)
        f.seek(0, os.SEEK_END)
        f.write(page)
        return page_count, rec_id


def get_record_from_file(file_name, page_number, record_id):
    """قراءة سجل من ملف استنادًا إلى رقم الصفحة ورقم السجل."""
    with open(file_name, 'rb') as f:
        f.seek(page_number * PAGE_SIZE)
        page = f.read(PAGE_SIZE)
        if len(page) != PAGE_SIZE:
            raise ValueError("Page not found or truncated")
        return get_record_from_page(page, record_id)


def get_all_record_from_file(file_name):
    """قراءة جميع السجلات من كل الصفحات في الملف."""
    records = []
    if not os.path.exists(file_name):
        return records

    with open(file_name, 'rb') as f:
        f.seek(0, os.SEEK_END)
        total_size = f.tell()
        page_count = total_size // PAGE_SIZE
        f.seek(0)
        for p in range(page_count):
            page = f.read(PAGE_SIZE)
            for idx, rec in enumerate(get_all_record_from_page(page)):
                records.append((p, idx, rec))
    return records


# ------------------------------------------------------------
# اختبار سريع
# ------------------------------------------------------------
if __name__ == "__main__":
    test_file = "test_heapfile.bin"
    if os.path.exists(test_file):
        os.remove(test_file)

    records = [
        b"hello",
        b"world",
        b"this is a longer record to test insertion",
        b"12345" * 200  # سجل كبير ~1000 بايت
    ]

    for r in records:
        print("Inserted:", insert_record_to_file(test_file, r))

    all_records = get_all_record_from_file(test_file)
    print("\nAll records found:")
    for page_num, rec_id, rec in all_records:
        print(f"Page {page_num} - Record {rec_id} - len={len(rec)} - preview={rec[:40]!r}")

    page0 = open(test_file, "rb").read(PAGE_SIZE)
    free_offset, slot_count = read_footer(page0)
    print("\nFooter Page0:", free_offset, slot_count)
    print("Free space:", Calculate_free_space(page0))
