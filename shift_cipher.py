class ShiftCipher:
    """
    Lớp thực hiện các thuật toán mã hóa dịch chuyển (Shift Cipher)
    """
    
    # Tần suất xuất hiện của các chữ cái trong tiếng Anh
    ENGLISH_FREQ = {
        'a': 0.0817, 'b': 0.0149, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270,
        'f': 0.0223, 'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015,
        'k': 0.0077, 'l': 0.0402, 'm': 0.0241, 'n': 0.0675, 'o': 0.0751,
        'p': 0.0193, 'q': 0.0009, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
        'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015, 'y': 0.0197, 'z': 0.0007
    }
    
    # Tần suất xuất hiện của các chữ cái trong tiếng Việt
    VIETNAMESE_FREQ = {
        'a': 0.0851, 'b': 0.0128, 'c': 0.0324, 'd': 0.0284, 'e': 0.0119,
        'f': 0.0001, 'g': 0.0134, 'h': 0.0241, 'i': 0.0824, 'j': 0.0001,
        'k': 0.0074, 'l': 0.0264, 'm': 0.0297, 'n': 0.1003, 'o': 0.0739,
        'p': 0.0189, 'q': 0.0011, 'r': 0.0031, 's': 0.0162, 't': 0.0689,
        'u': 0.0524, 'v': 0.0223, 'w': 0.0002, 'x': 0.0009, 'y': 0.0168, 'z': 0.0001
    }
    
    def __init__(self, language='en'):
        """
        Khởi tạo đối tượng ShiftCipher.
        
        Args:
            language (str): Ngôn ngữ được sử dụng ('en' cho tiếng Anh, 'vi' cho tiếng Việt)
        """
        self.language = language
        self.freq_map = self.ENGLISH_FREQ if language == 'en' else self.VIETNAMESE_FREQ
        
    def encrypt(self, text, shift):
        """
        Mã hóa văn bản sử dụng Shift Cipher.
        
        Args:
            text (str): Văn bản cần mã hóa
            shift (int): Số vị trí dịch chuyển
            
        Returns:
            str: Văn bản đã mã hóa
        """
        result = []
        
        for char in text:
            if char.isalpha():
                # Xác định mã ASCII cơ sở (65 cho 'A', 97 cho 'a')
                ascii_base = 65 if char.isupper() else 97
                
                # Công thức mã hóa: (x + shift) % 26
                shifted = (ord(char) - ascii_base + shift) % 26
                
                # Chuyển về ký tự
                result.append(chr(shifted + ascii_base))
            else:
                # Giữ nguyên các ký tự không phải chữ cái
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, text, shift):
        """
        Giải mã văn bản đã mã hóa bằng Shift Cipher.
        
        Args:
            text (str): Văn bản đã mã hóa
            shift (int): Số vị trí dịch chuyển
            
        Returns:
            str: Văn bản gốc
        """
        # Giải mã chính là mã hóa với shift âm
        return self.encrypt(text, -shift)
    
    def brute_force(self, text):
        """
        Thử tất cả các khả năng dịch chuyển có thể (1-25).
        
        Args:
            text (str): Văn bản đã mã hóa
            
        Returns:
            list: Danh sách các giải mã có thể
        """
        results = []
        
        for shift in range(1, 26):
            decrypted = self.decrypt(text, shift)
            score = self.calculate_language_score(decrypted)
            results.append((shift, decrypted, score))
        
        # Sắp xếp kết quả theo điểm so khớp ngôn ngữ (cao đến thấp)
        return sorted(results, key=lambda x: x[2], reverse=True)
    
    def calculate_letter_frequency(self, text):
        """
        Tính tần suất xuất hiện của các chữ cái trong văn bản.
        
        Args:
            text (str): Văn bản cần phân tích
            
        Returns:
            dict: Từ điển chứa tần suất xuất hiện của các chữ cái
        """
        # Chuyển văn bản về chữ thường và loại bỏ các ký tự không phải chữ cái
        text = ''.join(c.lower() for c in text if c.isalpha())
        
        if not text:
            return {}
            
        frequency = {}
        total_chars = len(text)
        
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        
        # Chuyển đếm thành tần suất (tỷ lệ)
        for char in frequency:
            frequency[char] /= total_chars
            
        return frequency
    
    def calculate_language_score(self, text):
        """
        Tính điểm so khớp của văn bản với ngôn ngữ đã chọn.
        
        Args:
            text (str): Văn bản cần đánh giá
            
        Returns:
            float: Điểm so khớp (0-1, càng cao càng giống ngôn ngữ)
        """
        text_freq = self.calculate_letter_frequency(text)
        score = 0
        
        for char, freq in text_freq.items():
            if char in self.freq_map:
                # Tính độ chênh lệch giữa tần suất chuẩn và tần suất trong văn bản
                score += 1 - abs(freq - self.freq_map.get(char, 0))
        
        # Chuẩn hóa điểm
        return score / len(text_freq) if text_freq else 0
    
    def analyze_text(self, text):
        """
        Phân tích văn bản đã mã hóa và đề xuất khóa giải mã tốt nhất.
        
        Args:
            text (str): Văn bản đã mã hóa
            
        Returns:
            tuple: (shift, decrypted_text, score) - khóa, văn bản giải mã, và điểm số
        """
        results = self.brute_force(text)
        return results[0] if results else (0, text, 0)
    
    def encrypt_file(self, input_file, output_file, shift):
        """
        Mã hóa nội dung của file.
        
        Args:
            input_file (str): Đường dẫn đến file đầu vào
            output_file (str): Đường dẫn đến file đầu ra
            shift (int): Số vị trí dịch chuyển
            
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
                
            encrypted = self.encrypt(content, shift)
            
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(encrypted)
                
            return True
        except Exception as e:
            print(f"Lỗi khi mã hóa file: {e}")
            return False
    
    def decrypt_file(self, input_file, output_file, shift):
        """
        Giải mã nội dung của file.
        
        Args:
            input_file (str): Đường dẫn đến file đầu vào
            output_file (str): Đường dẫn đến file đầu ra
            shift (int): Số vị trí dịch chuyển
            
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
                
            decrypted = self.decrypt(content, shift)
            
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(decrypted)
                
            return True
        except Exception as e:
            print(f"Lỗi khi giải mã file: {e}")
            return False

# Các hàm tiện ích để tương thích ngược với mã cũ
def encrypt(text, shift):
    cipher = ShiftCipher()
    return cipher.encrypt(text, shift)

def decrypt(text, shift):
    cipher = ShiftCipher()
    return cipher.decrypt(text, shift)

def brute_force(text):
    cipher = ShiftCipher()
    results = cipher.brute_force(text)
    # Chuyển đổi định dạng kết quả để tương thích với mã cũ
    return [(shift, decrypted) for shift, decrypted, _ in results] 