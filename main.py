import argparse
import os
from shift_cipher import ShiftCipher

def main():
    parser = argparse.ArgumentParser(description="Công cụ mã hóa và giải mã Shift Cipher nâng cao")
    
    # Tạo các nhóm lệnh
    subparsers = parser.add_subparsers(dest="command", help="Lệnh")
    
    # Tham số chung
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-l", "--language", choices=["en", "vi"], default="en",
                             help="Ngôn ngữ để phân tích tần suất (en=Tiếng Anh, vi=Tiếng Việt)")
    
    # Lệnh mã hóa văn bản
    encrypt_parser = subparsers.add_parser("encrypt", help="Mã hóa văn bản", parents=[parent_parser])
    encrypt_parser.add_argument("text", help="Văn bản cần mã hóa")
    encrypt_parser.add_argument("shift", type=int, help="Số vị trí dịch chuyển (1-25)")
    
    # Lệnh giải mã văn bản
    decrypt_parser = subparsers.add_parser("decrypt", help="Giải mã văn bản", parents=[parent_parser])
    decrypt_parser.add_argument("text", help="Văn bản cần giải mã")
    decrypt_parser.add_argument("shift", type=int, help="Số vị trí dịch chuyển (1-25)")
    
    # Lệnh brute force
    brute_parser = subparsers.add_parser("brute", help="Thử tất cả các khóa có thể", parents=[parent_parser])
    brute_parser.add_argument("text", help="Văn bản cần giải mã")
    brute_parser.add_argument("-t", "--top", type=int, default=5, help="Số lượng kết quả hàng đầu cần hiển thị")
    
    # Lệnh phân tích văn bản
    analyze_parser = subparsers.add_parser("analyze", help="Phân tích văn bản mã hóa và đề xuất khóa", parents=[parent_parser])
    analyze_parser.add_argument("text", help="Văn bản cần phân tích")
    
    # Lệnh mã hóa file
    encrypt_file_parser = subparsers.add_parser("encrypt-file", help="Mã hóa nội dung file", parents=[parent_parser])
    encrypt_file_parser.add_argument("input_file", help="Đường dẫn đến file đầu vào")
    encrypt_file_parser.add_argument("output_file", help="Đường dẫn đến file đầu ra")
    encrypt_file_parser.add_argument("shift", type=int, help="Số vị trí dịch chuyển (1-25)")
    
    # Lệnh giải mã file
    decrypt_file_parser = subparsers.add_parser("decrypt-file", help="Giải mã nội dung file", parents=[parent_parser])
    decrypt_file_parser.add_argument("input_file", help="Đường dẫn đến file đầu vào")
    decrypt_file_parser.add_argument("output_file", help="Đường dẫn đến file đầu ra")
    decrypt_file_parser.add_argument("shift", type=int, help="Số vị trí dịch chuyển (1-25)")
    
    # Lệnh phân tích file
    analyze_file_parser = subparsers.add_parser("analyze-file", help="Phân tích file mã hóa và đề xuất khóa", parents=[parent_parser])
    analyze_file_parser.add_argument("input_file", help="Đường dẫn đến file đầu vào")
    
    args = parser.parse_args()
    
    # Tạo đối tượng ShiftCipher với ngôn ngữ tương ứng
    if hasattr(args, 'language'):
        cipher = ShiftCipher(language=args.language)
    else:
        cipher = ShiftCipher()
    
    # Xử lý các lệnh
    if args.command == "encrypt":
        validate_shift(args.shift)
        result = cipher.encrypt(args.text, args.shift)
        print(f"Văn bản gốc: {args.text}")
        print(f"Văn bản mã hóa: {result}")
        
    elif args.command == "decrypt":
        validate_shift(args.shift)
        result = cipher.decrypt(args.text, args.shift)
        print(f"Văn bản mã hóa: {args.text}")
        print(f"Văn bản giải mã: {result}")
        
    elif args.command == "brute":
        results = cipher.brute_force(args.text)
        print(f"Văn bản mã hóa: {args.text}")
        print(f"Ngôn ngữ phân tích: {'Tiếng Anh' if args.language == 'en' else 'Tiếng Việt'}")
        print("Các kết quả giải mã tốt nhất:")
        
        # Hiển thị các kết quả hàng đầu
        top_results = results[:min(args.top, len(results))]
        for i, (shift, text, score) in enumerate(top_results, 1):
            print(f"{i}. Khóa {shift:2d} (Điểm: {score:.4f}): {text}")
            
    elif args.command == "analyze":
        shift, decrypted, score = cipher.analyze_text(args.text)
        print(f"Văn bản mã hóa: {args.text}")
        print(f"Ngôn ngữ phân tích: {'Tiếng Anh' if args.language == 'en' else 'Tiếng Việt'}")
        print(f"Khóa đề xuất: {shift} (Điểm: {score:.4f})")
        print(f"Văn bản giải mã: {decrypted}")
        
    elif args.command == "encrypt-file":
        validate_shift(args.shift)
        check_file_exists(args.input_file)
        
        if cipher.encrypt_file(args.input_file, args.output_file, args.shift):
            print(f"Đã mã hóa thành công file {args.input_file} -> {args.output_file}")
        else:
            print("Mã hóa file thất bại!")
        
    elif args.command == "decrypt-file":
        validate_shift(args.shift)
        check_file_exists(args.input_file)
        
        if cipher.decrypt_file(args.input_file, args.output_file, args.shift):
            print(f"Đã giải mã thành công file {args.input_file} -> {args.output_file}")
        else:
            print("Giải mã file thất bại!")
        
    elif args.command == "analyze-file":
        check_file_exists(args.input_file)
        
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            shift, decrypted, score = cipher.analyze_text(content)
            print(f"File mã hóa: {args.input_file}")
            print(f"Ngôn ngữ phân tích: {'Tiếng Anh' if args.language == 'en' else 'Tiếng Việt'}")
            print(f"Khóa đề xuất: {shift} (Điểm: {score:.4f})")
            print(f"Các dòng đầu tiên giải mã:")
            
            # Hiển thị 5 dòng đầu tiên của văn bản giải mã
            preview_lines = decrypted.splitlines()[:5]
            for line in preview_lines:
                print(f"  {line}")
                
            # Hỏi người dùng có muốn lưu kết quả giải mã không
            save = input("\nBạn có muốn lưu kết quả giải mã không? (y/n): ").lower()
            if save == 'y':
                output_file = input("Nhập tên file đầu ra: ")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(decrypted)
                print(f"Đã lưu kết quả giải mã vào {output_file}")
                
        except Exception as e:
            print(f"Lỗi khi phân tích file: {e}")
    else:
        parser.print_help()

def validate_shift(shift):
    """Kiểm tra giá trị shift có hợp lệ không"""
    if not 1 <= shift <= 25:
        print("Lỗi: Vị trí dịch chuyển phải từ 1 đến 25.")
        exit(1)

def check_file_exists(file_path):
    """Kiểm tra file có tồn tại không"""
    if not os.path.isfile(file_path):
        print(f"Lỗi: File '{file_path}' không tồn tại.")
        exit(1)

if __name__ == "__main__":
    main() 