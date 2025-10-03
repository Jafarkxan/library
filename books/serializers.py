from rest_framework import serializers
from .models import Book
import re


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        # TITLE validatsiya

    def validate_title(self, value):
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Title bo'sh bo'lmasligi kerak.")
        if len(v) < 2:
            raise serializers.ValidationError("Title kamida 2 ta belgidan iborat bo'lishi kerak.")
        # Bu qatorda kamida bittadan harf (unicode) bo'lishi kerak:
        if not any(ch.isalpha() for ch in v):
            raise serializers.ValidationError(
                "Title kamida bitta harf o'z ichiga olishi kerak — faqat raqam yozib bo'lmaydi.")
        return v

        # AUTHOR validatsiya

    def validate_author(self, value):
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Muallif nomi bo'sh bo'lmaydi.")
        if len(v) > 100:
            raise serializers.ValidationError("Muallif nomi 100 belgidan oshmasin.")
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ'’\-\s\.]+", v):
            raise serializers.ValidationError(
                "Muallif nomi faqat harflar, bo'shliq va .-' belgilaridan iborat bo'lishi kerak."
            )
        return v

        # PRICE validatsiya

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price manfiy bo'lishi mumkin emas.")
        if value > 1_000_000:
            raise serializers.ValidationError("Price juda katta (1 mln dan oshmasin).")
        return value

        # ISBN validatsiya

    def validate_isbn(self, value):
        s = re.sub(r"[\s\-]", "", value)  # bo'shliq va tirelarni olib tashlash

        # ISBN-10
        if len(s) == 10:
            total = 0
            for i, ch in enumerate(s, start=1):
                if i < 10:
                    if not ch.isdigit():
                        raise serializers.ValidationError("ISBN-10: birinchi 9 belgi raqam bo'lishi kerak.")
                    d = int(ch)
                else:
                    if ch in ('X', 'x'):
                        d = 10
                    elif ch.isdigit():
                        d = int(ch)
                    else:
                        raise serializers.ValidationError("ISBN-10 oxirgi belgi raqam yoki 'X' bo'lishi kerak.")
                total += i * d
            if total % 11 != 0:
                raise serializers.ValidationError("ISBN-10 noto'g'ri chek-summa.")

        # ISBN-13
        elif len(s) == 13:
            if not s.isdigit():
                raise serializers.ValidationError("ISBN-13 faqat raqamlardan iborat bo'lishi kerak.")
            total = 0
            for i, ch in enumerate(s[:-1]):
                d = int(ch)
                w = 1 if (i % 2 == 0) else 3
                total += d * w
            checksum = (10 - (total % 10)) % 10
            if checksum != int(s[-1]):
                raise serializers.ValidationError("ISBN-13 noto'g'ri chek-summa.")
        else:
            raise serializers.ValidationError("ISBN uzunligi 10 yoki 13 bo'lishi kerak.")

        return value