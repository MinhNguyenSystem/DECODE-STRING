
```markdown
# 🛡️ AST Deobfuscator

<p align="center">
  <b>Advanced Deobfuscation Tool based on AST</b><br>
  <i>Unpacker • Constant Folding • Dynamic Evaluation • Dead Code Removal</i>
</p>

<p align="center">
  <b>Copyright © 2026 MinhNguyen2412</b>
</p>

<p align="center">
  <a href="#-english">
    <img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge" alt="English">
  </a>
  &nbsp;&nbsp;
  <a href="#-vietnamese">
    <img src="https://img.shields.io/badge/Ngôn_Ngữ-Tiếng_Việt-red?style=for-the-badge" alt="Vietnamese">
  </a>
</p>
```
---

<a name="-english"></a>
## 🇬🇧 English

### 📖 Introduction
**AST Deobfuscator** is a powerful Python reverse-engineering tool designed to analyze and clean obfuscated code using Abstract Syntax Trees (AST). It packs robust features to handle complex protection schemes like **String Encryption**, **Zlib Packing**, and **Junk Code Injection**.

### 🚀 Key Features

*   **Unpacker**: Automatically detects classes using Zlib + XOR + Hex Strings and decrypts them.
*   **Constant Folding**: Pre-calculates math operations (`10 + 20`), bitwise logic, and comparisons directly within the AST.
*   **Dynamic Decoder Evaluation**: Identifies local decoder functions and safely executes them in a sandbox to retrieve plaintext strings.
*   **String Manipulation**: Handles complex string slicing (`[::-1]`), concatenation, and formatting.
*   **Dead Code Removal**: Cleans up standalone strings (docstrings/junk) inserted to confuse readers.

### 📦 Installation

This tool requires **Python 3.8+**

```bash
# Install the library for enhanced UI
pip install rich

# Install unparse support (Only if using Python < 3.9)
pip install astor
```

🛠️ Usage

Save the script as deobf_string.py.

Run the tool via terminal:
```bash
python deobf_string.py
```

The tool will list files in the current directory.

Enter the path to your obfuscated file.

Outputs:

filename_deobf.py: The cleaned, readable source code.

filename_records.json: A log of every string decrypted.

🧩 Demo Cases (Input vs Output)
1. Obfuscation (Zlib + XOR)

Input:
```python
class Protection:
    key = b'secret'
    enc = "789c0b05..." # Hex of Zlib compressed data
    def resolve(self, n): return getattr(builtins, n)
```

Output:
```python
class Protection:
    key = b'secret'
    enc = 'print' # Decrypted
    def resolve(self, n): return getattr(__builtins__, n)
```

2. String Slicing & Math

Input:
```python
pw = "k" + "c" + "a" + "H"[::-1]
val = (100 * 5) + 50
```

Output:
```python
pw = 'kcaH'
val = 550
```

<div align="right">
<a href="#-ast-deobfuscator">⬆️ Back to Top</a>
</div>


<a name="-vietnamese"></a>

🇻🇳 Vietnamese
📖 Giới thiệu

AST Deobfuscator là một công cụ dịch ngược mã nguồn Python mạnh mẽ dựa trên AST (Cây cú pháp trừu tượng), chuyên trị các loại mã hóa phức tạp như Mã hóa chuỗi, Pack lớp bảo vệ, và Chèn code rác.

🚀 Tính năng nổi bật

Unpacker: Tự động phát hiện và giải mã lớp bảo vệ kiểu (Zlib + XOR + Hex Strings) và vá lại các hàm gọi getattr.

Gập hằng số (Constant Folding): Tính toán trước các phép cộng, trừ, nhân, chia, bitwise và so sánh ngay trong code (10 * 5 -> 50).

Thực thi giải mã động: Tự động nhận diện các hàm giải mã cục bộ và chạy chúng trong môi trường an toàn để lấy chuỗi gốc.

Xử lý chuỗi: Tự động nối chuỗi, cắt chuỗi (s[::-1], s[0:4]) và giải mã bytes.

Xóa code rác: Loại bỏ các chuỗi vô nghĩa (junk strings) được chèn vào để gây rối mắt.

📦 Cài đặt

Yêu cầu Python 3.8+

```bash
# Cài đặt thư viện giao diện
pip install rich

# Cài đặt hỗ trợ unparse (Chỉ cần nếu dùng Python < 3.9)
pip install astor
```

🛠️ Hướng dẫn sử dụng

Lưu đoạn code tool thành file deobf_string.py.

Chạy tool bằng CMD/Terminal:

```bash
python deobf_string.py
```

Tool sẽ hiện danh sách file trong thư mục.

Nhập đường dẫn file bị mã hóa (Input file).

Kết quả:

filename_deobf.py: File code sạch đã giải mã.

filename_records.json: Log chi tiết các chuỗi đã giải mã.

🧩 Các dạng Demo (Input vs Output)

Dưới đây là các khả năng xử lý thực tế của tool:

1. Obfuscation (Zlib + XOR + Hex)

Tool tự động quét class, brute-force key và giải mã.

Input Code:
```python
import zlib
class AntiCrack:
    key = b'my_secret_key'
    # Chuỗi hex nén zlib
    data = "789c4bcecf494502000690022d" 
    
    def _void(self, n): pass
```

Output Code:
```python
import zlib
class AntiCrack:
    key = b'my_secret_key'
    data = 'CODE_SECURE' # Đã giải mã
    
    def _void(self, n): pass
```

2. Cắt chuỗi & Nối chuỗi (String Slicing)

Input Code:
```python
a = "n" + "o" + "h" + "t" + "y" + "P"
secret = a[::-1]
token = "HiddenTokenHere"[0:6]
```

Output Code:
```python
a = 'nohtyP'
secret = 'Python'
token = 'Hidden'
```

3. Toán học cơ bản & Logic (Constant Folding)

Input Code:
```python
x = (50 * 2) + (100 // 4)
check = True and False or True
if 100 > 10:
    print("Yes")
```

Output Code:
```python
x = 125
check = True
print('Yes') # Lệnh if đã được tối ưu hóa
```

4. Hàm giải mã tùy chỉnh (Custom Decoder)
Tool phát hiện hàm và chạy thử để lấy giá trị.

Input Code:
```python
def decrypt(s):
    return s[::-1]

user = decrypt("nimda")
pw = decrypt("123456")
```

Output Code:
```python
def decrypt(s):
    return s[::-1]

user = 'admin'
pw = '654321'
```

5. Giải mã Bytes & Eval

Input Code:
```python
x = eval("10 + 20")
msg = b'\x48\x65\x6c\x6c\x6f'.decode('utf-8')
```

Output Code:
```python
x = 30
msg = 'Hello'
```
<div align="center">
<b>Copyright © 2026 MinhNguyen2412</b>
</div>
