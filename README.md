# Mật Mã Dịch Chuyển (Shift Cipher)

Một ứng dụng toàn diện để mã hóa và giải mã văn bản sử dụng thuật toán mật mã dịch chuyển (Shift Cipher), còn được gọi là mật mã Caesar.

## Giới thiệu

Mật mã dịch chuyển là một trong những kỹ thuật mã hóa đơn giản nhất và lâu đời nhất. Nguyên tắc hoạt động như sau:
- Mỗi ký tự trong văn bản gốc được thay thế bằng một ký tự khác
- Ký tự thay thế được xác định bằng cách dịch chuyển cố định một số vị trí trong bảng chữ cái
- Ví dụ: với độ dịch k = 3, 'A' sẽ được mã hóa thành 'D', 'B' thành 'E', và cứ thế

## Tính năng

- **Mã hóa và giải mã văn bản** sử dụng khóa dịch chuyển từ 1-25
- **Mã hóa và giải mã file** văn bản
- **Phân tích tần suất ký tự** để tự động đề xuất khóa có khả năng cao nhất
- **Hỗ trợ đa ngôn ngữ** (Tiếng Anh và Tiếng Việt) cho việc phân tích tần suất
- **Giao diện đồ họa (GUI)** trực quan, dễ sử dụng
- **Giao diện dòng lệnh (CLI)** linh hoạt cho các tác vụ tự động hóa

## Cài đặt

Ứng dụng yêu cầu Python 3.6 trở lên.

```
# Tải mã nguồn
git clone https://github.com/username/shift-cipher.git
cd shift-cipher

# Cài đặt các thư viện phụ thuộc (nếu có)
# pip install -r requirements.txt
```

## Sử dụng

### Giao diện đồ họa

Để sử dụng giao diện đồ họa, chạy:

```
python gui.py
```

### Giao diện dòng lệnh

#### Mã hóa văn bản

```
python main.py encrypt "van ban can ma hoa" 3 --language vi
```

#### Giải mã văn bản

```
python main.py decrypt "ydq edq fdq pd krd" 3 --language vi
```

#### Thử tất cả các khóa có thể (Brute Force)

```
python main.py brute "ydq edq fdq pd krd" --language vi --top 5
```

#### Phân tích văn bản và đề xuất khóa tốt nhất

```
python main.py analyze "ydq edq fdq pd krd" --language vi
```

#### Mã hóa file

```
python main.py encrypt-file input.txt output.txt 3 --language vi
```

#### Giải mã file

```
python main.py decrypt-file input.txt output.txt 3 --language vi
```

#### Phân tích file mã hóa

```
python main.py analyze-file encrypted.txt --language vi
```

## Ví dụ

**Mã hóa:**
```
python main.py encrypt "HELLO" 3
```
Kết quả: `KHOOR`

**Giải mã:**
```
python main.py decrypt "KHOOR" 3
```
Kết quả: `HELLO`

**Thử tất cả các khóa:**
```
python main.py brute "KHOOR"
```
Kết quả sẽ hiển thị các khả năng giải mã với các độ dịch khác nhau, được sắp xếp theo khả năng hợp lý cao nhất (dựa trên phân tích tần suất).

## Cấu trúc mã nguồn

- `shift_cipher.py` - Thư viện lõi chứa các thuật toán và lớp ShiftCipher
- `main.py` - Giao diện dòng lệnh
- `gui.py` - Giao diện đồ họa người dùng
- `test_shift_cipher.py` - Các bài kiểm thử tự động

## Lưu ý kỹ thuật

- Chỉ các ký tự chữ cái (A-Z, a-z) được mã hóa
- Các ký tự khác như dấu cách, dấu câu, số sẽ được giữ nguyên
- Chương trình bảo tồn kiểu chữ (hoa/thường)
- Phân tích tần suất dựa trên tần suất xuất hiện các chữ cái trong tiếng Anh và tiếng Việt 