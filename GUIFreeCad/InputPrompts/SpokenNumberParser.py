# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""Parse spoken numeric phrases into integer and float values."""

from __future__ import annotations

import re
import unicodedata


class SpokenNumberParser:
    """Converts voice-recognized numeric phrases into Python numbers."""

    DigitWords: dict[str, str] = {
        "cero": "0",
        "zero": "0",
        "uno": "1",
        "un": "1",
        "una": "1",
        "one": "1",
        "um": "1",
        "uma": "1",
        "dos": "2",
        "two": "2",
        "dois": "2",
        "duas": "2",
        "tres": "3",
        "three": "3",
        "cuatro": "4",
        "four": "4",
        "quatro": "4",
        "cinco": "5",
        "five": "5",
        "seis": "6",
        "six": "6",
        "meia": "6",
        "siete": "7",
        "seven": "7",
        "sete": "7",
        "ocho": "8",
        "eight": "8",
        "oito": "8",
        "nueve": "9",
        "nine": "9",
        "nove": "9",
        # 10-19: numeros de una sola palabra, no se arman por concatenacion.
        "diez": "10",
        "ten": "10",
        "dez": "10",
        "once": "11",
        "eleven": "11",
        "onze": "11",
        "doce": "12",
        "twelve": "12",
        "doze": "12",
        "trece": "13",
        "thirteen": "13",
        "treze": "13",
        "catorce": "14",
        "fourteen": "14",
        "catorze": "14",
        "quatorze": "14",
        "quince": "15",
        "fifteen": "15",
        "quinze": "15",
        "dieciseis": "16",
        "sixteen": "16",
        "dezesseis": "16",
        "diecisiete": "17",
        "seventeen": "17",
        "dezessete": "17",
        "dieciocho": "18",
        "eighteen": "18",
        "dezoito": "18",
        "diecinueve": "19",
        "nineteen": "19",
        "dezenove": "19",
        # Decenas (20-90) dichas solas, sin unidad detras ("treinta" -> 30).
        "veinte": "20",
        "twenty": "20",
        "vinte": "20",
        "treinta": "30",
        "thirty": "30",
        "trinta": "30",
        "cuarenta": "40",
        "forty": "40",
        "quarenta": "40",
        "cincuenta": "50",
        "fifty": "50",
        "cinquenta": "50",
        "sesenta": "60",
        "sixty": "60",
        "sessenta": "60",
        "setenta": "70",
        "seventy": "70",
        "ochenta": "80",
        "eighty": "80",
        "oitenta": "80",
        "noventa": "90",
        "ninety": "90",
        # 21-29 contraidos en español ("veintidos"), unica lengua de las tres
        # que los dice como una sola palabra en vez de "veinte y dos".
        "veintiuno": "21",
        "veintidos": "22",
        "veintitres": "23",
        "veinticuatro": "24",
        "veinticinco": "25",
        "veintiseis": "26",
        "veintisiete": "27",
        "veintiocho": "28",
        "veintinueve": "29",
        # Centenas y miles (100-900, 1000) comunes en medidas CAD
        "cien": "100",
        "ciento": "100",
        "doscientos": "200",
        "doscientas": "200",
        "trescientos": "300",
        "trescientas": "300",
        "cuatrocientos": "400",
        "cuatrocientas": "400",
        "quinientos": "500",
        "quinientas": "500",
        "seiscientos": "600",
        "seiscientas": "600",
        "setecientos": "700",
        "setecientas": "700",
        "ochocientos": "800",
        "ochocientas": "800",
        "novecientos": "900",
        "novecientas": "900",
        "mil": "1000",
        "hundred": "100",
        "thousand": "1000",
        "cem": "100",
        "cento": "100",
        "duzentos": "200",
        "duzentas": "200",
        "trezentos": "300",
        "trezentas": "300",
        "quatrocentos": "400",
        "quatrocentas": "400",
        "quinhentos": "500",
        "quinhentas": "500",
        "seiscentos": "600",
        "seiscentas": "600",
        "setecentos": "700",
        "setecentas": "700",
        "oitocentos": "800",
        "oitocentas": "800",
        "novecentos": "900",
        "novecentas": "900",
    }

    # Palabras de decena (20-90) que se combinan con una unidad siguiente
    # ("treinta y dos" -> 32, "twenty two" -> 22, "vinte e um" -> 21). Se
    # necesitan como valores enteros aparte de DigitWords porque hay que
    # sumarlas con la unidad, no solo reconocerlas como palabra suelta.
    TensWords: dict[str, int] = {
        "veinte": 20,
        "twenty": 20,
        "vinte": 20,
        "treinta": 30,
        "thirty": 30,
        "trinta": 30,
        "cuarenta": 40,
        "forty": 40,
        "quarenta": 40,
        "cincuenta": 50,
        "fifty": 50,
        "cinquenta": 50,
        "sesenta": 60,
        "sixty": 60,
        "sessenta": 60,
        "setenta": 70,
        "seventy": 70,
        "ochenta": 80,
        "eighty": 80,
        "oitenta": 80,
        "noventa": 90,
        "ninety": 90,
    }

    # Palabras de centena (100-900) que se combinan con decenas/unidades
    HundredsWords: dict[str, int] = {
        "cien": 100,
        "ciento": 100,
        "hundred": 100,
        "cem": 100,
        "cento": 100,
        "doscientos": 200,
        "doscientas": 200,
        "duzentos": 200,
        "duzentas": 200,
        "trescientos": 300,
        "trescientas": 300,
        "trezentos": 300,
        "trezentas": 300,
        "cuatrocientos": 400,
        "cuatrocientas": 400,
        "quatrocentos": 400,
        "quatrocentas": 400,
        "quinientos": 500,
        "quinientas": 500,
        "quinhentos": 500,
        "quinhentas": 500,
        "seiscientos": 600,
        "seiscientas": 600,
        "seiscentos": 600,
        "seiscentas": 600,
        "setecientos": 700,
        "setecientas": 700,
        "setecentos": 700,
        "setecentas": 700,
        "ochocientos": 800,
        "ochocientas": 800,
        "oitocentos": 800,
        "oitocentas": 800,
        "novecientos": 900,
        "novecientas": 900,
        "novecentos": 900,
        "novecentas": 900,
    }

    ThousandsWords: dict[str, int] = {
        "mil": 1000,
        "thousand": 1000,
    }

    # Conector opcional entre decena y unidad. El ingles no usa uno en este
    # rango ("twenty two"), por eso no aparece aca.
    ConnectorWords: set[str] = {"y", "e"}

    # "diez y seis" / "dez e seis" -> 16. Solo se suman con conector explicito: sin el,
    # "diez seis" sigue siendo 10 y 6 dictados por separado.
    TenWords: set[str] = {"diez", "dez"}

    # Unidades 1-9 con valor entero, derivadas de DigitWords para no repetir
    # la lista: se usan solo para sumarlas a una decena en _MergeTensAndUnits.
    UnitWords: dict[str, int] = {
        word: int(value)
        for word, value in DigitWords.items()
        if value.isdigit() and 1 <= int(value) <= 9
    }

    DecimalWords: set[str] = {
        "coma",
        "punto",
        "decimal",
        "comma",
        "point",
        "virgula",
        "ponto",
    }
    NegativeWords: set[str] = {"menos", "minus", "negative", "negativo"}

    # Estas dos se completan al final del modulo con lo que haya en
    # Atria/dictionary/NavCommands/TraduceTo*.py, para que sumar un sinonimo sea editar
    # el diccionario y no tres archivos de codigo. Lo que queda escrito aca es
    # el respaldo por si el diccionario no se puede cargar.
    #
    # A diferencia del Browser, que trabaja en un idioma por vez, los prompts
    # aceptan los tres a la vez: el usuario puede decir "ok" con la interfaz en
    # espanol y tiene que andar igual.
    ConfirmationWords: set[str] = {
        "enter",
        "entrar",
        "enviar",
        "send",
        "ok",
        "okey",
        "okay",
        "aceptar",
        "aceitar",
        "confirmar",
        "accept",
        "confirm",
        "listo",
        "vale",
        "hecho",
        "dale",
        "si",
        "bueno",
        "done",
        "yes",
        "yep",
        "pronto",
        "feito",
        "sim",
    }
    CancellationWords: set[str] = {
        "cancelar",
        "cancel",
        "cancela",
        "cancelamento",
        "descartar",
        "discard",
        "anular",
        "abortar",
        "abort",
        "no",
        "nao",
        "olvidalo",
        "never mind",
    }

    @classmethod
    def ParseInteger(cls, Phrase: str) -> int:
        """Parse a spoken phrase into an integer."""
        number_text = cls.ParseNumberText(Phrase, AllowDecimal=False)
        return int(number_text)

    @classmethod
    def ParseFloat(cls, Phrase: str) -> float:
        """Parse a spoken phrase into a float."""
        number_text = cls.ParseNumberText(Phrase, AllowDecimal=True)
        return float(number_text)

    @classmethod
    def TryParseInteger(cls, Phrase: str) -> int | None:
        """Return an integer when parsing succeeds, otherwise None."""
        try:
            return cls.ParseInteger(Phrase)
        except ValueError:
            return None

    @classmethod
    def TryParseFloat(cls, Phrase: str) -> float | None:
        """Return a float when parsing succeeds, otherwise None."""
        try:
            return cls.ParseFloat(Phrase)
        except ValueError:
            return None

    @classmethod
    def ParseNumberText(cls, Phrase: str, *, AllowDecimal: bool) -> str:
        """Convert a spoken phrase into a numeric string."""
        tokens = cls.Tokenize(Phrase)
        if not tokens:
            raise ValueError("No numeric phrase was provided.")
        tokens = cls._MergeTensAndUnits(tokens)

        sign = ""
        digits: list[str] = []
        decimal_seen = False
        digit_seen = False

        for token in tokens:
            if token in cls.ConfirmationWords:
                break
            if token in cls.CancellationWords:
                raise ValueError("Numeric input was cancelled.")
            if token in cls.NegativeWords and not digit_seen and not sign:
                sign = "-"
                continue
            if token in cls.DecimalWords:
                if not AllowDecimal:
                    raise ValueError("Decimal separator is not valid for integer input.")
                if decimal_seen:
                    raise ValueError("Multiple decimal separators were provided.")
                digits.append(".")
                decimal_seen = True
                continue

            numeric_token = cls._TokenToNumericText(token)
            if numeric_token is None:
                continue

            if "." in numeric_token:
                if not AllowDecimal:
                    raise ValueError("Decimal number is not valid for integer input.")
                if decimal_seen:
                    raise ValueError("Multiple decimal separators were provided.")
                whole, decimal = numeric_token.split(".", 1)
                if whole:
                    digits.append(whole)
                    digit_seen = True
                digits.append(".")
                decimal_seen = True
                if decimal:
                    digits.append(decimal)
                    digit_seen = True
                continue

            digits.append(numeric_token)
            digit_seen = True

        if not digit_seen:
            raise ValueError(f"No numeric value could be parsed from: {Phrase!r}")

        number_text = sign + "".join(digits)
        if number_text.endswith("."):
            number_text += "0"
        if number_text in {"", "-", ".", "-."}:
            raise ValueError(f"Invalid numeric value parsed from: {Phrase!r}")
        return number_text

    @classmethod
    def _MergeTensAndUnits(cls, Tokens: list[str]) -> list[str]:
        """Merge compound spoken numbers (thousands, hundreds, tens, units).

        Lets users say natural compound numbers ("ciento cincuenta", "treinta y dos",
        "dos mil quinientos", "twenty two") instead of dictating each digit separately.
        Lone digit words are left untouched so digit-by-digit dictation still works.
        """
        merged: list[str] = []
        index, total = 0, len(Tokens)
        while index < total:
            accum_val = 0
            consumed = False

            # Millares: "dos mil" -> 2000, o "mil" -> 1000
            if (
                Tokens[index] in cls.UnitWords
                and index + 1 < total
                and Tokens[index + 1] in cls.ThousandsWords
            ):
                accum_val += cls.UnitWords[Tokens[index]] * 1000
                index += 2
                consumed = True
            elif Tokens[index] in cls.ThousandsWords:
                accum_val += 1000
                index += 1
                consumed = True

            # Centenas: "quinientos" / "doscientos" / "ciento"
            if index < total and Tokens[index] in cls.HundredsWords:
                accum_val += cls.HundredsWords[Tokens[index]]
                index += 1
                consumed = True

            # Decenas y unidades
            if index < total and Tokens[index] in cls.TensWords:
                tens_val = cls.TensWords[Tokens[index]]
                index += 1
                consumed = True
                if index < total and Tokens[index] in cls.ConnectorWords:
                    index += 1
                if index < total and Tokens[index] in cls.UnitWords:
                    tens_val += cls.UnitWords[Tokens[index]]
                    index += 1
                accum_val += tens_val
            elif (
                index + 2 < total
                and Tokens[index] in cls.TenWords
                and Tokens[index + 1] in cls.ConnectorWords
                and Tokens[index + 2] in cls.UnitWords
            ):
                accum_val += 10 + cls.UnitWords[Tokens[index + 2]]
                index += 3
                consumed = True
            elif index < total and Tokens[index] in cls.UnitWords and consumed:
                accum_val += cls.UnitWords[Tokens[index]]
                index += 1

            if consumed:
                merged.append(str(accum_val))
            else:
                merged.append(Tokens[index])
                index += 1
        return merged

    @classmethod
    def Tokenize(cls, Phrase: str) -> list[str]:
        """Normalize and split a phrase into parseable tokens."""
        normalized = cls.NormalizeText(Phrase)
        return re.findall(r"-?\d+(?:[.,]\d+)?|[a-z0-9]+", normalized)

    @staticmethod
    def NormalizeText(Text: str) -> str:
        """Remove accents and normalize common decimal punctuation."""
        if not Text:
            return ""
        normalized = (
            unicodedata.normalize("NFKD", Text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        return normalized.replace(",", ".")

    @classmethod
    def _TokenToNumericText(cls, Token: str) -> str | None:
        if Token in cls.DigitWords:
            return cls.DigitWords[Token]
        if re.fullmatch(r"-?\d+(?:\.\d+)?", Token):
            return Token
        return None


def _LoadNavWordsFromDictionaries() -> None:
    """Widen the confirm/cancel sets with NavCommands/TraduceTo*.py.

    Los prompts aceptan los tres idiomas a la vez, asi que se juntan los tres
    TraduceTo. Si el diccionario no esta o falla la importacion, quedan los
    conjuntos escritos en la clase: los prompts siguen andando con las palabras
    basicas en vez de romper el arranque.
    """
    try:
        import importlib
        import sys

        from GUIFreeCad.integration.voice_bootstrap import _resolve_dictionary_root

        root = _resolve_dictionary_root()
        if not (root / "NavCommands").is_dir():
            return

        parent = str(root.parent)
        if parent not in sys.path:
            sys.path.insert(0, parent)

        package = root.name
        actions = importlib.import_module(f"{package}.NavCommands.NavActions").NavActions
        send, cancel = actions.get("send"), actions.get("cancel")

        for lang in ("TraduceToEs", "TraduceToEn", "TraduceToPt"):
            module = importlib.import_module(f"{package}.NavCommands.{lang}")
            mapping = getattr(module, lang, {})
            for spoken, target in mapping.items():
                raw = spoken.strip().lower()
                normalized = SpokenNumberParser.NormalizeText(raw).strip()
                if target is send:
                    SpokenNumberParser.ConfirmationWords.add(raw)
                    if normalized != raw:
                        SpokenNumberParser.ConfirmationWords.add(normalized)
                elif target is cancel:
                    SpokenNumberParser.CancellationWords.add(raw)
                    if normalized != raw:
                        SpokenNumberParser.CancellationWords.add(normalized)
    except Exception:
        # Un diccionario roto no puede dejar los prompts sin confirmar.
        pass


_LoadNavWordsFromDictionaries()
