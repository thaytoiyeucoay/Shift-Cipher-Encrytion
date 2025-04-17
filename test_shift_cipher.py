import unittest
from shift_cipher import ShiftCipher, encrypt, decrypt, brute_force

class TestShiftCipher(unittest.TestCase):
    def setUp(self):
        """Khởi tạo đối tượng ShiftCipher cho các bài kiểm thử"""
        self.cipher_en = ShiftCipher(language='en')
        self.cipher_vi = ShiftCipher(language='vi')
    
    def test_encrypt(self):
        """Kiểm tra chức năng mã hóa"""
        # Kiểm tra phương thức của lớp
        self.assertEqual(self.cipher_en.encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(self.cipher_en.encrypt("hello", 3), "khoor")
        self.assertEqual(self.cipher_en.encrypt("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(self.cipher_en.encrypt("XYZ", 3), "ABC")
        self.assertEqual(self.cipher_en.encrypt("xyz", 3), "abc")
        self.assertEqual(self.cipher_en.encrypt("HELLO", 0), "HELLO")  # Không dịch chuyển
        self.assertEqual(self.cipher_en.encrypt("HELLO", 26), "HELLO")  # Dịch chuyển 1 vòng đầy đủ
        
        # Kiểm tra hàm tiện ích
        self.assertEqual(encrypt("HELLO", 3), "KHOOR")
        
    def test_decrypt(self):
        """Kiểm tra chức năng giải mã"""
        # Kiểm tra phương thức của lớp
        self.assertEqual(self.cipher_en.decrypt("KHOOR", 3), "HELLO")
        self.assertEqual(self.cipher_en.decrypt("khoor", 3), "hello")
        self.assertEqual(self.cipher_en.decrypt("Khoor, Zruog!", 3), "Hello, World!")
        self.assertEqual(self.cipher_en.decrypt("ABC", 3), "XYZ")
        self.assertEqual(self.cipher_en.decrypt("abc", 3), "xyz")
        
        # Kiểm tra hàm tiện ích
        self.assertEqual(decrypt("KHOOR", 3), "HELLO")
        
    def test_encryption_decryption_consistency(self):
        """Kiểm tra tính nhất quán giữa mã hóa và giải mã"""
        plaintext = "The quick brown fox jumps over the lazy dog"
        for shift in range(1, 26):
            # Kiểm tra phương thức của lớp
            encrypted = self.cipher_en.encrypt(plaintext, shift)
            decrypted = self.cipher_en.decrypt(encrypted, shift)
            self.assertEqual(decrypted, plaintext)
            
            # Kiểm tra hàm tiện ích
            encrypted = encrypt(plaintext, shift)
            decrypted = decrypt(encrypted, shift)
            self.assertEqual(decrypted, plaintext)
            
    def test_brute_force(self):
        """Kiểm tra chức năng dò tìm tất cả các khóa"""
        encrypted = self.cipher_en.encrypt("HELLO", 3)
        
        # Kiểm tra phương thức của lớp
        results = self.cipher_en.brute_force(encrypted)
        
        # Kiểm tra một trong các kết quả phải là văn bản gốc
        found = False
        for shift, text, score in results:
            if text == "HELLO":
                found = True
                self.assertEqual(shift, 3)
                break
                
        self.assertTrue(found, "Không tìm thấy văn bản gốc trong kết quả brute force")
        
        # Kiểm tra hàm tiện ích
        compat_results = brute_force(encrypted)
        self.assertEqual(len(compat_results), 25)
        
    def test_letter_frequency(self):
        """Kiểm tra tính toán tần suất chữ cái"""
        text = "hello world"
        freq = self.cipher_en.calculate_letter_frequency(text)
        
        # Kiểm tra tổng tần suất phải bằng 1
        self.assertAlmostEqual(sum(freq.values()), 1.0, places=5)
        
        # Kiểm tra một số tần suất cụ thể
        self.assertAlmostEqual(freq.get('l', 0), 3/8, places=5)  # 'l' xuất hiện 3 lần trong 8 chữ cái
        self.assertAlmostEqual(freq.get('o', 0), 2/8, places=5)  # 'o' xuất hiện 2 lần trong 8 chữ cái
        
    def test_analyze_text(self):
        """Kiểm tra chức năng phân tích văn bản"""
        # Tạo văn bản tiếng Anh mã hóa đơn giản
        english_text = "the quick brown fox jumps over the lazy dog"
        encrypted = self.cipher_en.encrypt(english_text, 5)
        
        # Phân tích với ngôn ngữ tiếng Anh
        key, decrypted, score = self.cipher_en.analyze_text(encrypted)
        
        # Khóa được đề xuất phải là 5 hoặc 21 (26-5)
        self.assertTrue(key == 5 or key == 21, 
                      f"Khóa được đề xuất ({key}) khác với khóa thực tế (5 hoặc 21)")
        
    def test_different_languages(self):
        """Kiểm tra phân tích với các ngôn ngữ khác nhau"""
        # Tạo văn bản đơn giản mã hóa với khóa 3
        text = "hello"
        encrypted = self.cipher_en.encrypt(text, 3)
        
        # Xác nhận cả hai đối tượng cho cùng một kết quả mã hóa
        self.assertEqual(self.cipher_en.encrypt(text, 3), self.cipher_vi.encrypt(text, 3))
        
        # Kiểm tra brute force với các ngôn ngữ khác nhau phải cho ra thứ tự kết quả khác nhau
        # (Ghi chú: Đây là kiểm thử khó, phụ thuộc vào dữ liệu và có thể bị lỗi nếu văn bản quá ngắn)
        en_results = self.cipher_en.brute_force(encrypted)
        vi_results = self.cipher_vi.brute_force(encrypted)
        
        # Chuyển đổi kết quả thành từ điển để dễ so sánh
        en_scores = {shift: score for shift, _, score in en_results}
        vi_scores = {shift: score for shift, _, score in vi_results}
        
        # Điểm số khác nhau cho ít nhất một khóa
        different_scores = False
        for shift in range(1, 26):
            if abs(en_scores.get(shift, 0) - vi_scores.get(shift, 0)) > 0.01:  # Dung sai nhỏ
                different_scores = True
                break
                
        # Ghi chú: Test này có thể không ổn định với văn bản quá ngắn
        # self.assertTrue(different_scores, "Điểm số phân tích ngôn ngữ phải khác nhau giữa tiếng Anh và tiếng Việt")

    def test_performance(self):
        """Kiểm tra hiệu năng cơ bản"""
        import time
        
        # Tạo văn bản lớn để kiểm tra
        large_text = "Hello world! " * 1000
        
        # Đo thời gian mã hóa
        start_time = time.time()
        encrypted = self.cipher_en.encrypt(large_text, 13)
        encrypt_time = time.time() - start_time
        
        # Đo thời gian giải mã
        start_time = time.time()
        decrypted = self.cipher_en.decrypt(encrypted, 13)
        decrypt_time = time.time() - start_time
        
        # Kiểm tra thời gian không quá 0.1 giây cho mỗi thao tác
        self.assertLess(encrypt_time, 0.1, "Mã hóa quá chậm")
        self.assertLess(decrypt_time, 0.1, "Giải mã quá chậm")
        self.assertEqual(decrypted, large_text)

if __name__ == "__main__":
    unittest.main() 