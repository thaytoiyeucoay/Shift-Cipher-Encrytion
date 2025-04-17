import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from shift_cipher import ShiftCipher

class ShiftCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shift Cipher - Mã hóa dịch chuyển")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Tạo đối tượng cipher
        self.cipher = ShiftCipher()
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_widgets(self):
        # Tạo Notebook (tab control)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tab mã hóa/giải mã văn bản
        self.text_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.text_tab, text="Mã hóa Văn bản")
        
        # Tab mã hóa/giải mã file
        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="Mã hóa File")
        
        # Tab phân tích văn bản
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Phân tích")
        
        # Thêm nội dung cho từng tab
        self.setup_text_tab()
        self.setup_file_tab()
        self.setup_analysis_tab()
        
    def setup_text_tab(self):
        # Frame chọn chức năng và ngôn ngữ
        option_frame = ttk.LabelFrame(self.text_tab, text="Tùy chọn")
        option_frame.pack(fill="x", padx=10, pady=10)
        
        # Hàng 1: Chọn chức năng, khóa, ngôn ngữ
        ttk.Label(option_frame, text="Chức năng:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.operation_var = tk.StringVar(value="encrypt")
        ttk.Radiobutton(option_frame, text="Mã hóa", variable=self.operation_var, value="encrypt").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(option_frame, text="Giải mã", variable=self.operation_var, value="decrypt").grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(option_frame, text="Khóa (1-25):").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.shift_var = tk.IntVar(value=3)
        shift_spinbox = ttk.Spinbox(option_frame, from_=1, to=25, textvariable=self.shift_var, width=5)
        shift_spinbox.grid(row=0, column=4, padx=5, pady=5)
        
        ttk.Label(option_frame, text="Ngôn ngữ:").grid(row=0, column=5, padx=5, pady=5, sticky="w")
        self.language_var = tk.StringVar(value="en")
        ttk.Radiobutton(option_frame, text="Tiếng Anh", variable=self.language_var, value="en", 
                      command=self.update_language).grid(row=0, column=6, padx=5, pady=5)
        ttk.Radiobutton(option_frame, text="Tiếng Việt", variable=self.language_var, value="vi", 
                      command=self.update_language).grid(row=0, column=7, padx=5, pady=5)
        
        # Frame văn bản đầu vào
        input_frame = ttk.LabelFrame(self.text_tab, text="Văn bản đầu vào")
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10)
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame nút thao tác
        button_frame = ttk.Frame(self.text_tab)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Thực hiện", command=self.process_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        
        # Frame văn bản đầu ra
        output_frame = ttk.LabelFrame(self.text_tab, text="Kết quả")
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def setup_file_tab(self):
        # Frame tùy chọn
        option_frame = ttk.LabelFrame(self.file_tab, text="Tùy chọn")
        option_frame.pack(fill="x", padx=10, pady=10)
        
        # Hàng 1: Chọn chức năng, khóa, ngôn ngữ
        ttk.Label(option_frame, text="Chức năng:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_operation_var = tk.StringVar(value="encrypt")
        ttk.Radiobutton(option_frame, text="Mã hóa", variable=self.file_operation_var, value="encrypt").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(option_frame, text="Giải mã", variable=self.file_operation_var, value="decrypt").grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(option_frame, text="Khóa (1-25):").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.file_shift_var = tk.IntVar(value=3)
        shift_spinbox = ttk.Spinbox(option_frame, from_=1, to=25, textvariable=self.file_shift_var, width=5)
        shift_spinbox.grid(row=0, column=4, padx=5, pady=5)
        
        # Frame chọn file
        file_frame = ttk.LabelFrame(self.file_tab, text="Chọn File")
        file_frame.pack(fill="x", padx=10, pady=10)
        
        # Hàng 1: File đầu vào
        ttk.Label(file_frame, text="File đầu vào:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.input_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Chọn", command=self.browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Hàng 2: File đầu ra
        ttk.Label(file_frame, text="File đầu ra:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.output_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.output_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Chọn", command=self.browse_output_file).grid(row=1, column=2, padx=5, pady=5)
        
        # Frame xử lý
        process_frame = ttk.Frame(self.file_tab)
        process_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(process_frame, text="Thực hiện", command=self.process_file).pack(side=tk.LEFT, padx=5)
        
        # Thanh trạng thái
        self.file_status_var = tk.StringVar(value="Sẵn sàng")
        ttk.Label(self.file_tab, textvariable=self.file_status_var).pack(anchor="w", padx=10, pady=5)
        
        # Thanh tiến trình
        self.progress = ttk.Progressbar(self.file_tab, orient=tk.HORIZONTAL, length=780, mode='indeterminate')
        self.progress.pack(fill="x", padx=10, pady=5)
        
    def setup_analysis_tab(self):
        # Frame tùy chọn
        option_frame = ttk.LabelFrame(self.analysis_tab, text="Tùy chọn")
        option_frame.pack(fill="x", padx=10, pady=10)
        
        # Hàng 1: Chọn ngôn ngữ
        ttk.Label(option_frame, text="Ngôn ngữ:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.analysis_language_var = tk.StringVar(value="en")
        ttk.Radiobutton(option_frame, text="Tiếng Anh", variable=self.analysis_language_var, value="en", 
                       command=self.update_analysis_language).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(option_frame, text="Tiếng Việt", variable=self.analysis_language_var, value="vi", 
                       command=self.update_analysis_language).grid(row=0, column=2, padx=5, pady=5)
        
        # Frame văn bản mã hóa
        input_frame = ttk.LabelFrame(self.analysis_tab, text="Văn bản mã hóa")
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.analysis_input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10)
        self.analysis_input_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame nút thao tác
        button_frame = ttk.Frame(self.analysis_tab)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Phân tích", command=self.analyze_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Phân tích từ file", command=self.analyze_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.clear_analysis).pack(side=tk.LEFT, padx=5)
        
        # Frame kết quả phân tích
        output_frame = ttk.LabelFrame(self.analysis_tab, text="Kết quả phân tích")
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # TreeView để hiển thị kết quả
        self.result_tree = ttk.Treeview(output_frame, columns=("key", "score", "text"), show="headings")
        self.result_tree.heading("key", text="Khóa")
        self.result_tree.heading("score", text="Điểm")
        self.result_tree.heading("text", text="Văn bản giải mã")
        
        self.result_tree.column("key", width=50)
        self.result_tree.column("score", width=100)
        self.result_tree.column("text", width=630)
        
        self.result_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
    def update_language(self):
        self.cipher = ShiftCipher(language=self.language_var.get())
        
    def update_analysis_language(self):
        self.cipher = ShiftCipher(language=self.analysis_language_var.get())
        
    def process_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần xử lý.")
            return
            
        try:
            shift = self.shift_var.get()
            if not 1 <= shift <= 25:
                messagebox.showerror("Lỗi", "Khóa phải từ 1 đến 25.")
                return
                
            operation = self.operation_var.get()
            if operation == "encrypt":
                result = self.cipher.encrypt(input_text, shift)
            else:
                result = self.cipher.decrypt(input_text, shift)
                
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xảy ra lỗi: {str(e)}")
            
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file đầu vào", 
                                             filetypes=[("Text files", "*.txt"), 
                                                      ("All files", "*.*")])
        if file_path:
            self.input_file_var.set(file_path)
            
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(title="Chọn file đầu ra", 
                                               filetypes=[("Text files", "*.txt"), 
                                                        ("All files", "*.*")])
        if file_path:
            self.output_file_var.set(file_path)
            
    def process_file(self):
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()
        
        if not input_file or not output_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cả file đầu vào và đầu ra.")
            return
            
        try:
            shift = self.file_shift_var.get()
            if not 1 <= shift <= 25:
                messagebox.showerror("Lỗi", "Khóa phải từ 1 đến 25.")
                return
                
            operation = self.file_operation_var.get()
            
            # Bắt đầu xử lý
            self.file_status_var.set("Đang xử lý...")
            self.progress.start()
            
            # Sử dụng luồng riêng để tránh giao diện bị đóng băng
            threading.Thread(target=self.process_file_thread, 
                           args=(input_file, output_file, operation, shift)).start()
                
        except Exception as e:
            self.progress.stop()
            self.file_status_var.set("Xảy ra lỗi")
            messagebox.showerror("Lỗi", f"Xảy ra lỗi: {str(e)}")
            
    def process_file_thread(self, input_file, output_file, operation, shift):
        try:
            if operation == "encrypt":
                success = self.cipher.encrypt_file(input_file, output_file, shift)
            else:
                success = self.cipher.decrypt_file(input_file, output_file, shift)
                
            # Cập nhật giao diện từ luồng chính
            self.root.after(0, self.update_file_status, success, output_file)
                
        except Exception as e:
            self.root.after(0, self.handle_file_error, str(e))
            
    def update_file_status(self, success, output_file):
        self.progress.stop()
        if success:
            self.file_status_var.set(f"Xử lý thành công, lưu tại: {output_file}")
            messagebox.showinfo("Thành công", f"File đã được xử lý thành công và lưu tại:\n{output_file}")
        else:
            self.file_status_var.set("Xử lý thất bại")
            messagebox.showerror("Lỗi", "Không thể xử lý file.")
            
    def handle_file_error(self, error_msg):
        self.progress.stop()
        self.file_status_var.set("Xảy ra lỗi")
        messagebox.showerror("Lỗi", f"Xảy ra lỗi: {error_msg}")
        
    def analyze_text(self):
        input_text = self.analysis_input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần phân tích.")
            return
            
        try:
            # Cập nhật cipher với ngôn ngữ đã chọn
            self.cipher = ShiftCipher(language=self.analysis_language_var.get())
            
            # Phân tích
            results = self.cipher.brute_force(input_text)
            
            # Xóa kết quả cũ
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)
                
            # Hiển thị kết quả
            for i, (shift, text, score) in enumerate(results[:10]):  # Chỉ hiển thị 10 kết quả đầu
                # Cắt bớt văn bản nếu quá dài
                display_text = text[:100] + "..." if len(text) > 100 else text
                self.result_tree.insert("", i, values=(shift, f"{score:.4f}", display_text))
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xảy ra lỗi khi phân tích: {str(e)}")
            
    def analyze_from_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file cần phân tích", 
                                             filetypes=[("Text files", "*.txt"), 
                                                      ("All files", "*.*")])
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Hiển thị nội dung file
            self.analysis_input_text.delete("1.0", tk.END)
            
            # Hiển thị tối đa 5000 ký tự để tránh quá tải
            if len(content) > 5000:
                self.analysis_input_text.insert("1.0", content[:5000] + "...(nội dung bị cắt bớt)")
            else:
                self.analysis_input_text.insert("1.0", content)
                
            # Phân tích
            self.analyze_text()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            
    def clear_analysis(self):
        self.analysis_input_text.delete("1.0", tk.END)
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftCipherGUI(root)
    root.mainloop() 