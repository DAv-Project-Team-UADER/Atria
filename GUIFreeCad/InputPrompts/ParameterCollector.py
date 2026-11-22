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

"""Collect function parameters with ATRIA input prompts and Validator."""

from __future__ import annotations

import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import (
    KindLabel,
    ParamFriendlyMessage,
    ParamFriendlyName,
    ResolveLanguage,
    T,
)


@dataclass(frozen=True)
class _FallbackRequirementSpec:
    """Internal fallback when validation.RequirementSpec is unavailable."""

    index: int
    name: str
    kind: str
    required: bool


class ParameterCollector:
    """Collects and validates all parameters required by a callable."""

    def __init__(
        self,
        Language: str | None = None,
        Parent=None,
        DelayMs: int = 30,
        ValidatorInstance: Any | None = None,
    ) -> None:
        self._StoredLanguage = Language
        self.Parent = Parent
        self.DelayMs = DelayMs
        self._Validator = ValidatorInstance or self._CreateValidator()

    @property
    def Language(self) -> str:
        """Language of the prompt texts: explicit if configured, or live from options."""
        if self._StoredLanguage is not None:
            return self._StoredLanguage
        try:
            return ResolveLanguage()
        except Exception:
            return "es"

    @Language.setter
    def Language(self, value: str) -> None:
        self._StoredLanguage = value

    def CollectForFunction(
        self,
        Function: Callable[..., Any],
        SimulatedFinalTexts: Iterable[str] | None = None,
    ) -> PromptResult:
        """Collect all parameters for Function and return validated kwargs."""
        if not callable(Function):
            return PromptResult.Fail("Function is not callable.")

        specs = self._GetRequiredRequirementSpecs(Function)
        if not specs:
            return PromptResult.Ok({})

        simulated_inputs = list(SimulatedFinalTexts) if SimulatedFinalTexts is not None else None
        collected: dict[str, Any] = {}

        for index, spec in enumerate(specs):
            result = self._CollectValueForSpec(spec, simulated_inputs, index)

            if result.Cancelled:
                return result
            if not result.Success:
                return PromptResult.Fail(
                    result.Error or f"Could not collect parameter '{spec.name}'."
                )

            collected[spec.name] = result.Value
            self._RunDelay()

        return self.ValidateCollectedParameters(Function, collected)

    def GetRequirementsText(self, Function: Callable[..., Any]) -> str:
        """Return localized requirements using Validator."""
        return self._Validator.GetRequirements(self.Language, Function)

    def ValidateCollectedParameters(
        self,
        Function: Callable[..., Any],
        CollectedParameters: dict[str, Any],
    ) -> PromptResult:
        """Validate collected kwargs using Validator."""
        ok, validated = self._Validator.ValidateRequirements(
            self.Language,
            Function,
            CollectedParameters,
        )
        if not ok or validated is None:
            return PromptResult.Fail("Collected parameters failed validation.")

        return PromptResult.Ok(validated)

    def _CollectValueForSpec(
        self,
        Spec: Any,
        SimulatedInputs: list[str] | None,
        Index: int,
    ) -> PromptResult:
        if SimulatedInputs is not None:
            if Index >= len(SimulatedInputs):
                return PromptResult.Fail(f"Missing simulated input for '{Spec.name}'.")
            return self._ParseSimulatedValue(Spec, SimulatedInputs[Index])

        prompt = self._CreatePromptForSpec(Spec)
        return self._RequestPromptValue(prompt, None, Index)

    def _RequestPromptValue(
        self,
        Prompt: Any,
        SimulatedInputs: list[str] | None,
        Index: int,
    ) -> PromptResult:
        if SimulatedInputs is not None:
            if Index >= len(SimulatedInputs):
                return PromptResult.Fail("Missing simulated input for parameter.")
            return Prompt.ProcessFinalText(SimulatedInputs[Index])

        from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

        PromptVoiceRouter.SetActivePrompt(Prompt)
        try:
            return Prompt.RequestValue()
        finally:
            PromptVoiceRouter.ClearActivePrompt(Prompt)

    def _ParseSimulatedValue(self, Spec: Any, Text: str) -> PromptResult:
        tokens = SpokenNumberParser.Tokenize(Text)
        if any(token in SpokenNumberParser.CancellationWords for token in tokens):
            return PromptResult.Cancel()

        kind = getattr(Spec, "kind", "object")
        has_confirmation = any(token in SpokenNumberParser.ConfirmationWords for token in tokens)

        if not has_confirmation:
            cleaned = Text.strip().replace(",", ".")
            if kind in ("float", "int"):
                try:
                    f_val = float(cleaned)
                    if kind == "int":
                        return PromptResult.Ok(int(f_val))
                    return PromptResult.Ok(f_val)
                except ValueError:
                    pass
                try:
                    if kind == "int":
                        return PromptResult.Ok(SpokenNumberParser.ParseInteger(Text))
                    return PromptResult.Ok(SpokenNumberParser.ParseFloat(Text))
                except Exception:
                    pass
            elif kind in ("coord", "point", "vector"):
                from InputPrompts.CoordinateInputPrompt import CoordinateInputPrompt

                prompt = CoordinateInputPrompt()
                coords = prompt._ExtractCoordinates(Text)
                if coords:
                    return PromptResult.Ok(coords)
            return PromptResult.Fail(f"Missing confirmation for '{Spec.name}'.")

        try:
            if kind in ("coord", "point", "vector"):
                from InputPrompts.CoordinateInputPrompt import CoordinateInputPrompt

                prompt = CoordinateInputPrompt()
                return prompt.ProcessFinalText(Text)
            if kind == "int":
                cleaned = Text.strip().replace(",", ".")
                try:
                    f_val = float(cleaned)
                    if f_val.is_integer():
                        return PromptResult.Ok(int(f_val))
                except ValueError:
                    pass
                return PromptResult.Ok(SpokenNumberParser.ParseInteger(Text))
            if kind == "float":
                cleaned = Text.strip().replace(",", ".")
                try:
                    return PromptResult.Ok(float(cleaned))
                except ValueError:
                    pass
                return PromptResult.Ok(SpokenNumberParser.ParseFloat(Text))
            if kind == "str":
                value = self._StripConfirmation(Text)
                if not value:
                    return PromptResult.Fail(f"Text value for '{Spec.name}' cannot be empty.")
                return PromptResult.Ok(value)

            value = self._StripConfirmation(Text)
            if not value:
                return PromptResult.Fail(f"Object value for '{Spec.name}' cannot be empty.")
            return PromptResult.Ok(value)
        except ValueError as error:
            return PromptResult.Fail(str(error))

    def _CreatePromptForSpec(self, Spec: Any):
        kind = getattr(Spec, "kind", "object")
        title = self._BuildPromptTitle(Spec)
        message = self._BuildPromptMessage(Spec)

        if kind in ("coord", "point", "vector"):
            from InputPrompts.CoordinateInputPrompt import CoordinateInputPrompt

            return CoordinateInputPrompt(title, message, self.Parent)

        if kind == "int":
            from InputPrompts.IntegerInputPrompt import IntegerInputPrompt

            return IntegerInputPrompt(title, message, self.Parent)
        if kind == "float":
            from InputPrompts.FloatInputPrompt import FloatInputPrompt

            return FloatInputPrompt(title, message, self.Parent)
        if kind == "str":
            from InputPrompts.StringInputPrompt import StringInputPrompt

            return StringInputPrompt(title, message, self.Parent)

        from InputPrompts.ObjectSelectionInputPrompt import ObjectSelectionInputPrompt

        return ObjectSelectionInputPrompt(title, message, self.Parent)

    def _BuildPromptTitle(self, Spec: Any) -> str:
        name = getattr(Spec, "name", "value")
        friendly = ParamFriendlyName(self.Language, name)
        if friendly:
            return f"ATRIA — {friendly}"
        return T(self.Language, "param_title", index=getattr(Spec, "index", ""))

    def _BuildPromptMessage(self, Spec: Any) -> str:
        name = getattr(Spec, "name", "value")
        kind = getattr(Spec, "kind", "object")
        friendly = ParamFriendlyMessage(self.Language, name, kind)
        if friendly:
            return friendly
        return T(
            self.Language,
            "param_message",
            kind=KindLabel(self.Language, kind),
            name=name,
        )

    @staticmethod
    def _StripConfirmation(Text: str) -> str:
        words = Text.strip().split()
        while words:
            normalized = SpokenNumberParser.NormalizeText(words[-1])
            if normalized not in SpokenNumberParser.ConfirmationWords:
                break
            words.pop()
        return " ".join(words).strip()

    def _GetRequirementSpecs(self, Function: Callable[..., Any]) -> list[Any]:
        build_specs = getattr(self._Validator, "_BuildSpecs", None)
        if callable(build_specs):
            return list(build_specs(Function))
        return self._BuildFallbackSpecs(Function)

    def _GetRequiredRequirementSpecs(self, Function: Callable[..., Any]) -> list[Any]:
        return [
            spec
            for spec in self._GetRequirementSpecs(Function)
            if getattr(spec, "required", True)
        ]

    def _BuildFallbackSpecs(self, Function: Callable[..., Any]) -> list[_FallbackRequirementSpec]:
        try:
            signature = inspect.signature(Function)
        except (TypeError, ValueError):
            return []

        specs: list[_FallbackRequirementSpec] = []
        index = 1
        for name, parameter in signature.parameters.items():
            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            specs.append(
                _FallbackRequirementSpec(
                    index=index,
                    name=name,
                    kind=self._KindFromAnnotation(parameter.annotation),
                    required=parameter.default is inspect.Parameter.empty,
                )
            )
            index += 1
        return specs

    @staticmethod
    def _KindFromAnnotation(Annotation: Any) -> str:
        if Annotation is int:
            return "int"
        if Annotation is float:
            return "float"
        if Annotation is str:
            return "str"
        return "object"

    def _CreateValidator(self):
        self._EnsureValidationPath()
        from validator import Validator

        return Validator()

    @staticmethod
    def _EnsureValidationPath() -> Path:
        validation_root = Path(__file__).resolve()
        for parent in validation_root.parents:
            candidate = parent / "validation"
            if candidate.is_dir():
                validation_root = candidate
                break
        else:
            validation_root = Path(__file__).resolve().parents[3] / "validation"

        validation_text = str(validation_root)
        if validation_root.is_dir() and validation_text not in sys.path:
            sys.path.insert(0, validation_text)
        return validation_root

    def _RunDelay(self) -> None:
        if self.DelayMs <= 0:
            return
        try:
            try:
                from PySide6.QtCore import QEventLoop, QTimer
            except ImportError:
                from PySide2.QtCore import QEventLoop, QTimer  # type: ignore[assignment]

            loop = QEventLoop()
            QTimer.singleShot(self.DelayMs, loop.quit)
            if hasattr(loop, "exec"):
                loop.exec()
            else:
                loop.exec_()
        except Exception:
            return
