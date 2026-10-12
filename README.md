# SDF Assignment 10 — Unit Testing & Mutation Testing

**Kelompok 8**

| Nama | NIM | Peran |
|------|-----|-------|
| Roby Cahya Insani | 25120300006 | Ketua |
| Muhammad Hasbi Nurkhalis |  24110300014 | Anggota |
| Daniel Satria | 24120310014 | Anggota |
| Fajar Muhammad Ramadhan | 25120300023 | Anggota |

**Mata Kuliah:** Software Development Fundamentals


## Deskripsi

Tugas ini berisi:
- Penulisan unit test untuk modul `pricing.py` menggunakan **PyTest**.
- Pengujian mutasi sederhana untuk membuktikan daya deteksi test.
- Jawaban 6 pertanyaan analisis.

---

## Struktur Proyek

```
sdf-assignment-10/
├── README.md                      ← laporan ini
├── .gitignore
├── pytest_output.txt              ← output pytest -v (kode benar)
├── src/
│   └── pricing.py                 ← modul yang diuji (TIDAK DIUBAH)
├── tests/
│   └── test_pricing.py            ← 12+ fungsi test
└── mutation/
    ├── mutation_1_no_discount.py  ← mutasi 1
    ├── mutation_2_wrong_tax.py    ← mutasi 2
    └── mutation_3_no_validation.py ← mutasi 3
```

---

## Cara Menjalankan Test

```bash
py -m pytest tests/ -v
```

---

## Ringkasan Test

Total: **21 test** (12+ fungsi, dengan beberapa parametrize).

Cakupan aturan bisnis:

| Aturan | Test |
|--------|------|
| 1. Subtotal = harga × kuantitas | `test_calculate_subtotal_basic`, `test_calculate_subtotal_parametrized` |
| 2. Harga negatif → ValueError | `test_calculate_subtotal_negative_price_raises`, `test_calculate_subtotal_negative_price_message` |
| 3. Kuantitas ≤ 0 → ValueError | `test_calculate_subtotal_zero_quantity_raises`, `test_calculate_subtotal_negative_quantity_raises` |
| 4. Diskon member 10% | `test_apply_member_discount_member`, `test_apply_member_discount_non_member`, `test_member_discount_rate_value` |
| 5. Pajak 11% | `test_add_tax_basic`, `test_tax_rate_value` |
| 6. write_receipt | `test_write_receipt_creates_file`, `test_write_receipt_content`, `test_write_receipt_ends_with_newline`, `test_write_receipt_empty_lines` |
| Integrasi | `test_calculate_total_non_member`, `test_calculate_total_member`, `test_calculate_total_default_is_non_member`, `test_calculate_total_member_less_than_non_member` |

---

## Fitur PyTest yang Digunakan

| Fitur | Lokasi | Jumlah |
|-------|--------|--------|
| `pytest.mark.parametrize` | `test_calculate_subtotal_parametrized` | 1 test, 3 kombinasi |
| `pytest.raises` | 5 test | ✅ min 2 |
| `pytest.approx` | 6 test | ✅ min 1 |
| Fixture `tmp_path` | 4 test | ✅ |

---

## Mutation Testing

Tiga kerusakan buatan dibuat pada salinan `pricing.py`. Untuk setiap mutasi, `src/pricing.py` sementara diganti dengan file mutasi, test dijalankan, lalu file asli dikembalikan.

| No | Mutasi (Kerusakan Buatan) | Test yang Gagal | Kesimpulan Daya Deteksi |
|----|---------------------------|-----------------|-------------------------|
| 1 | Menghapus penerapan diskon member (fungsi `apply_member_discount` selalu mengembalikan subtotal) | `test_apply_member_discount_member`, `test_calculate_total_member`, `test_calculate_total_member_less_than_non_member` | **Terdeteksi (3 test gagal).** Test berhasil mendeteksi hilangnya logika diskon. |
| 2 | Mengubah tarif pajak `TAX_RATE` dari 0.11 menjadi 0.20 | `test_add_tax_basic`, `test_tax_rate_value`, `test_calculate_total_non_member`, `test_calculate_total_member`, `test_calculate_total_default_is_non_member` | **Terdeteksi (5 test gagal).** Test berhasil mendeteksi kesalahan tarif pajak. |
| 3 | Menghapus validasi `unit_price < 0` di `calculate_subtotal` | `test_calculate_subtotal_negative_price_raises`, `test_calculate_subtotal_negative_price_message` | **Terdeteksi (2 test gagal).** Test berhasil mendeteksi hilangnya validasi masukan. |

**Kesimpulan:** Semua mutasi berhasil dideteksi oleh test. Test kita memiliki daya deteksi yang baik terhadap perubahan logika bisnis.

---

## Output `pytest -v` (Kode Benar)

```
===================================== test session starts ======================================
platform win32 -- Python 3.11.2, pytest-9.1.1, pluggy-1.6.0
collected 21 items

tests/test_pricing.py::test_calculate_subtotal_basic PASSED
tests/test_pricing.py::test_calculate_subtotal_parametrized[1000-1-1000] PASSED
tests/test_pricing.py::test_calculate_subtotal_parametrized[500-4-2000] PASSED
tests/test_pricing.py::test_calculate_subtotal_parametrized[2500-2-5000] PASSED
tests/test_pricing.py::test_calculate_subtotal_negative_price_raises PASSED
tests/test_pricing.py::test_calculate_subtotal_negative_price_message PASSED
tests/test_pricing.py::test_calculate_subtotal_zero_quantity_raises PASSED
tests/test_pricing.py::test_calculate_subtotal_negative_quantity_raises PASSED
tests/test_pricing.py::test_apply_member_discount_member PASSED
tests/test_pricing.py::test_apply_member_discount_non_member PASSED
tests/test_pricing.py::test_member_discount_rate_value PASSED
tests/test_pricing.py::test_add_tax_basic PASSED
tests/test_pricing.py::test_tax_rate_value PASSED
tests/test_pricing.py::test_calculate_total_non_member PASSED
tests/test_pricing.py::test_calculate_total_member PASSED
tests/test_pricing.py::test_calculate_total_default_is_non_member PASSED
tests/test_pricing.py::test_calculate_total_member_less_than_non_member PASSED
tests/test_pricing.py::test_write_receipt_creates_file PASSED
tests/test_pricing.py::test_write_receipt_content PASSED
tests/test_pricing.py::test_write_receipt_ends_with_newline PASSED
tests/test_pricing.py::test_write_receipt_empty_lines PASSED

====================================== 21 passed in 0.19s ======================================
```

---

## Pertanyaan Analisis

### 1. Mengapa perbandingan bilangan floating point sebaiknya memakai `pytest.approx`?

Bilangan floating point disimpan dalam format IEEE 754 dengan presisi terbatas. Operasi aritmatika seperti perkalian dan pembagian dapat menghasilkan galat pembulatan kecil. Contoh:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

Akibatnya, perbandingan langsung (`==`) bisa gagal meskipun secara matematis hasilnya sama. `pytest.approx` membandingkan dengan toleransi relatif/absolut (default `1e-6`), sehingga perbandingan stabil dan tidak rapuh terhadap galat pembulatan.

```python
assert calculate_total(100, 3, is_member=True) == pytest.approx(299.7)   # aman
assert calculate_total(100, 3, is_member=True) == 299.7                  # bisa gagal
```

### 2. Mengapa test yang memakai berkas nyata di direktori proyek lebih berisiko?

Test yang memakai berkas nyata di direktori proyek berisiko karena:

1. Mengotori repository (file hasil test tertinggal).
2. Konflik antar test (dua test menulis file yang sama).
3. Tidak bersih antar run (file lama mempengaruhi test berikutnya).
4. Sulit dijalankan paralel.
5. Bergantung pada izin file system.
6. Tidak portabel antar OS.

`tmp_path` menyediakan direktori sementara unik per test yang otomatis dibuat dan dibersihkan PyTest, terisolasi, aman untuk paralel, dan tidak mengotori repository.

### 3. Test paling lemah dan usulan perbaikan

Test paling lemah:

```python
def test_member_discount_rate_value():
    assert MEMBER_DISCOUNT_RATE == 0.10
```

**Alasan:** Hanya memeriksa nilai konstanta, bukan perilaku fungsi. Kalau `apply_member_discount` diubah untuk mengabaikan konstanta, test ini tetap lulus.

**Usulan perbaikan:**

```python
def test_apply_member_discount_uses_rate_constant():
    subtotal = 1000
    expected = subtotal * (1 - MEMBER_DISCOUNT_RATE)
    assert apply_member_discount(subtotal, True) == pytest.approx(expected)
```

### 4. Bagaimana mutation testing mengubah cara menilai kualitas test?

Sebelum mutation testing, saya menilai test dari coverage (berapa persen baris dieksekusi). Tapi coverage tidak menjamin test mendeteksi bug — test bisa mengeksekusi baris tanpa assertion yang berarti.

Setelah mutation testing:

1. Coverage ≠ kualitas.
2. Test harus punya assertion konkret.
3. Test harus menguji perilaku, bukan implementasi.
4. Mutation score adalah metrik lebih baik daripada coverage.

Kualitas test diukur dari kemampuannya mendeteksi bug, bukan dari berapa banyak kode yang dieksekusi.

### 5. Padanan PyTest dengan JUnit 5

| PyTest | JUnit 5 |
|--------|---------|
| `pytest.raises(ValueError)` | `assertThrows(ValueError.class, () -> ...)` |
| `pytest.mark.parametrize` | `@ParameterizedTest` + `@ValueSource` / `@CsvSource` |
| `tmp_path` fixture | `@TempDir` |
| `@pytest.fixture` | `@BeforeEach` / `@BeforeAll` |
| `assert x == y` | `assertEquals(x, y)` |
| `pytest.approx` | `assertEquals(expected, actual, delta)` |

### 6. Mengapa "total anggota selalu lebih besar daripada subtotal" keliru?

Pernyataan ini salah karena:

1. Anggota mendapat diskon 10%, sehingga subtotal dikurangi sebelum pajak.
2. Pajak 11% ditambahkan setelah diskon.
3. Efek netto: `(1 - 0.10) × (1 + 0.11) = 0.9 × 1.11 = 0.999`, yang lebih kecil dari 1.

Contoh: `unit_price = 100`, `quantity = 3`, `is_member = True`:

- Subtotal: `100 × 3 = 300`
- Diskon 10%: `300 × 0.9 = 270`
- Pajak 11%: `270 × 1.11 = 299.7`
- **Total = 299.7**

Bandingkan: subtotal = 300, total anggota = 299.7. Karena **299.7 < 300**, total anggota lebih kecil dari subtotal. Asumsi "total selalu lebih besar dari subtotal" keliru.

---

## Kesimpulan

- **21 test** lulus pada kode yang benar.
- **3 mutasi** berhasil dideteksi oleh test (3, 5, dan 2 test gagal).
- Test memiliki daya deteksi yang baik terhadap perubahan logika bisnis.