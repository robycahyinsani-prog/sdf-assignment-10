"""Unit test untuk modul pricing.py.

Mencakup seluruh aturan bisnis:
1. Subtotal = harga satuan x kuantitas.
2. Harga satuan negatif -> ValueError.
3. Kuantitas nol atau negatif -> ValueError.
4. Member diskon 10%, non-member bayar penuh.
5. Pajak 11% ditambahkan setelah diskon.
6. Struk ditulis ke berkas dengan setiap baris diakhiri newline.
"""

import sys
from pathlib import Path

import pytest

# Tambahkan folder src ke sys.path agar pricing bisa di-import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pricing import (
    MEMBER_DISCOUNT_RATE,
    TAX_RATE,
    add_tax,
    apply_member_discount,
    calculate_subtotal,
    calculate_total,
    write_receipt,
)


# ============================================================
# Aturan 1: Subtotal = harga satuan x kuantitas
# ============================================================

def test_calculate_subtotal_basic():
    """Subtotal = harga x kuantitas untuk nilai normal."""
    assert calculate_subtotal(100, 3) == 300


@pytest.mark.parametrize(
    "unit_price, quantity, expected",
    [
        (1000, 1, 1000),
        (500, 4, 2000),
        (2500, 2, 5000),
    ],
)
def test_calculate_subtotal_parametrized(unit_price, quantity, expected):
    """Subtotal untuk berbagai kombinasi harga dan kuantitas."""
    assert calculate_subtotal(unit_price, quantity) == expected


# ============================================================
# Aturan 2: Harga satuan negatif -> ValueError
# ============================================================

def test_calculate_subtotal_negative_price_raises():
    """Harga satuan negatif harus memunculkan ValueError."""
    with pytest.raises(ValueError):
        calculate_subtotal(-100, 2)


def test_calculate_subtotal_negative_price_message():
    """Pesan error harus menyebut 'unit_price'."""
    with pytest.raises(ValueError, match="unit_price"):
        calculate_subtotal(-1, 1)


# ============================================================
# Aturan 3: Kuantitas nol atau negatif -> ValueError
# ============================================================

def test_calculate_subtotal_zero_quantity_raises():
    """Kuantitas nol harus memunculkan ValueError."""
    with pytest.raises(ValueError):
        calculate_subtotal(100, 0)


def test_calculate_subtotal_negative_quantity_raises():
    """Kuantitas negatif harus memunculkan ValueError."""
    with pytest.raises(ValueError, match="quantity"):
        calculate_subtotal(100, -3)


# ============================================================
# Aturan 4: Member diskon 10%, non-member bayar penuh
# ============================================================

def test_apply_member_discount_member():
    """Member mendapat diskon 10%."""
    assert apply_member_discount(1000, True) == pytest.approx(900)


def test_apply_member_discount_non_member():
    """Non-member membayar penuh."""
    assert apply_member_discount(1000, False) == 1000


def test_member_discount_rate_value():
    """Konstanta diskon harus 0.10."""
    assert MEMBER_DISCOUNT_RATE == 0.10


# ============================================================
# Aturan 5: Pajak 11% setelah diskon
# ============================================================

def test_add_tax_basic():
    """Pajak 11% ditambahkan pada amount."""
    assert add_tax(1000) == pytest.approx(1110)


def test_tax_rate_value():
    """Konstanta pajak harus 0.11."""
    assert TAX_RATE == 0.11


# ============================================================
# Integrasi: calculate_total
# ============================================================

def test_calculate_total_non_member():
    """Non-member: subtotal + pajak, tanpa diskon."""
    # 100 * 3 = 300; pajak 11% -> 333
    assert calculate_total(100, 3, is_member=False) == pytest.approx(333.0)


def test_calculate_total_member():
    """Member: subtotal - diskon 10% + pajak 11%."""
    # 100 * 3 = 300; diskon -> 270; pajak -> 299.7
    assert calculate_total(100, 3, is_member=True) == pytest.approx(299.7)


def test_calculate_total_default_is_non_member():
    """Default is_member=False -> tanpa diskon."""
    assert calculate_total(100, 3) == pytest.approx(333.0)


def test_calculate_total_member_less_than_non_member():
    """Total member harus lebih kecil dari non-member (karena diskon)."""
    member = calculate_total(100, 3, is_member=True)
    non_member = calculate_total(100, 3, is_member=False)
    assert member < non_member


# ============================================================
# Aturan 6: write_receipt dengan tmp_path
# ============================================================

def test_write_receipt_creates_file(tmp_path):
    """write_receipt membuat file di path yang diberikan."""
    receipt = tmp_path / "receipt.txt"
    write_receipt(receipt, ["Item A: 100", "Item B: 200"])
    assert receipt.exists()


def test_write_receipt_content(tmp_path):
    """Isi file harus sesuai dengan baris yang diberikan."""
    receipt = tmp_path / "receipt.txt"
    lines = ["Item A: 100", "Item B: 200", "Total: 300"]
    write_receipt(receipt, lines)
    content = receipt.read_text(encoding="utf-8")
    assert content == "Item A: 100\nItem B: 200\nTotal: 300\n"


def test_write_receipt_ends_with_newline(tmp_path):
    """Baris terakhir harus diakhiri newline."""
    receipt = tmp_path / "receipt.txt"
    write_receipt(receipt, ["Only line"])
    content = receipt.read_text(encoding="utf-8")
    assert content.endswith("\n")


def test_write_receipt_empty_lines(tmp_path):
    """write_receipt dengan list kosong tetap menulis newline."""
    receipt = tmp_path / "receipt.txt"
    write_receipt(receipt, [])
    content = receipt.read_text(encoding="utf-8")
    assert content == "\n"