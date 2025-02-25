from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Sequence, Tuple, Type, Union

import numpy as np

from dataclasses import field
from .autodiff import Context, Variable, backpropagate, central_difference
from .scalar_functions import (
    Inv,
    Mul,
    ScalarFunction,
    EQ,
    LT,
    Add,
    Exp,
    Log,
    Neg,
    ReLU,
    Sigmoid,
)

ScalarLike = Union[float, int, "Scalar"]


@dataclass
class ScalarHistory:
    """`ScalarHistory` stores the history of `Function` operations that was
    used to construct the current Variable.

    Attributes
    ----------
        last_fn : The last Function that was called.
        ctx : The context for that Function.
        inputs : The inputs that were given when `last_fn.forward` was called.

    """

    last_fn: Optional[Type[ScalarFunction]] = None
    ctx: Optional[Context] = None
    inputs: Sequence[Scalar] = ()


# ## Task 1.2 and 1.4
# Scalar Forward and Backward

_var_count = 0


@dataclass
class Scalar:
    """A reimplementation of scalar values for autodifferentiation
    tracking. Scalar Variables behave as close as possible to standard
    Python numbers while also tracking the operations that led to the
    number's creation. They can only be manipulated by
    `ScalarFunction`.
    """

    data: float
    history: Optional[ScalarHistory] = field(default_factory=ScalarHistory)
    derivative: Optional[float] = None
    name: str = field(default="")
    unique_id: int = field(default=0)

    def __post_init__(self):
        """Post-initialization to assign unique ID and convert data to float."""
        global _var_count
        _var_count += 1
        object.__setattr__(self, "unique_id", _var_count)
        object.__setattr__(self, "name", str(self.unique_id))
        object.__setattr__(self, "data", float(self.data))

    def __repr__(self) -> str:
        """Return a string representation of the Scalar object."""
        return f"Scalar({self.data})"

    def __mul__(self, b: ScalarLike) -> Scalar:
        """Multiply two Scalar values."""
        return Mul.apply(self, b)

    def __truediv__(self, b: ScalarLike) -> Scalar:
        """Divide two Scalar values."""
        return Mul.apply(self, Inv.apply(b))

    def __rtruediv__(self, b: ScalarLike) -> Scalar:
        """Right division of two Scalar values."""
        return Mul.apply(b, Inv.apply(self))

    def __bool__(self) -> bool:
        """Return the boolean value of the Scalar."""
        return bool(self.data)

    def __radd__(self, b: ScalarLike) -> Scalar:
        """Right addition of two Scalar values."""
        return self + b

    def __rmul__(self, b: ScalarLike) -> Scalar:
        """Right multiplication of two Scalar values."""
        return self * b

    # Variable elements for backprop

    def accumulate_derivative(self, x: Any) -> None:
        """Add `val` to the the derivative accumulated on this variable.
        Should only be called during autodifferentiation on leaf variables.

        Args:
        ----
            x: value to be accumulated

        """
        assert self.is_leaf(), "Only leaf variables can have derivatives."
        if self.derivative is None:
            self.__setattr__("derivative", 0.0)
        self.__setattr__("derivative", self.derivative + x)

    def is_leaf(self) -> bool:
        """Return True if this variable was created by the user (no `last_fn`)."""
        return self.history is not None and self.history.last_fn is None

    def is_constant(self) -> bool:
        """Return True if this variable has no history."""
        return self.history is None

    @property
    def parents(self) -> Iterable[Variable]:
        """Return the parent variables of this Scalar."""
        assert self.history is not None
        return self.history.inputs

    def chain_rule(self, d_output: Any) -> Iterable[Tuple[Variable, Any]]:
        """Perform the chain rule to compute gradients for this Scalar.

        Args:
        ----
            d_output: The output gradient to propagate backward.

        Returns:
        -------
            An iterable of (Variable, gradient) pairs.

        """
        # h = self.history
        # assert h is not None
        # assert h.last_fn is not None
        # assert h.ctx is not None

        # # Initialize an empty list to store the chain rule results
        # chain_rule_results = []

        # # Get the gradients of the inputs with respect to the output by calling the stored function
        # d_inputs = h.last_fn.backward(h.ctx, d_output)

        # # Ensure that d_inputs is a tuple or list (to handle multiple gradients)
        # if not isinstance(d_inputs, (tuple, list)):
        #     d_inputs = [d_inputs]

        # # Iterate through all inputs and their corresponding gradients
        # for input_var, d_input in zip(h.inputs, d_inputs):
        #     # Append the input variable and its corresponding gradient to the results
        #     chain_rule_results.append((input_var, d_input))

        # # Return the chain rule results as an iterable
        # return chain_rule_results

        h = self.history
        assert h is not None
        assert h.last_fn is not None
        assert h.ctx is not None

        # Get the gradients of the inputs with respect to the output by calling the stored function
        d_inputs = h.last_fn.backward(h.ctx, d_output)  # type: ignore

        # Ensure that d_inputs is a tuple or list (to handle multiple gradients)
        if not isinstance(d_inputs, (tuple, list)):
            d_inputs = [d_inputs]

        # Iterate through all inputs and their corresponding gradients
        chain_rule_results = []
        for input_var, d_input in zip(h.inputs, d_inputs):
            chain_rule_results.append((input_var, d_input))

        # Return the chain rule results as an iterable
        return chain_rule_results

    def backward(self, d_output: Optional[float] = None) -> None:
        """Calls autodiff to fill in the derivatives for the history of this object.

        Args:
        ----
            d_output (number, opt): starting derivative to backpropagate through the model
                                   (typically left out, and assumed to be 1.0).

        """
        if d_output is None:
            d_output = 1.0
        backpropagate(self, d_output)

    # TODO: Implement for Task 1.2.
    def __add__(self, b: ScalarLike) -> Scalar:
        """Add two Scalar values."""
        return Add.apply(self, b)

    def __lt__(self, b: ScalarLike) -> Scalar:
        """Check if Scalar is less than another Scalar."""
        return LT.apply(self, b)

    def __gt__(self, b: ScalarLike) -> Scalar:
        """Check if Scalar is greater than another Scalar."""
        return LT.apply(b, self)

    def __eq__(self, b: ScalarLike) -> Scalar:  # type: ignore[override]
        """Check if Scalar is equal to another Scalar."""
        return EQ.apply(self, b)

    def __sub__(self, b: ScalarLike) -> Scalar:
        """Subtract two Scalar values."""
        return Add.apply(self, Neg.apply(b))

    def __neg__(self) -> Scalar:
        """Negate the Scalar value."""
        return Neg.apply(self)

    def log(self) -> Scalar:
        """Return the logarithm of the Scalar."""
        return Log.apply(self)

    def exp(self) -> Scalar:
        """Return the exponential of the Scalar."""
        return Exp.apply(self)

    def sigmoid(self) -> Scalar:
        """Apply the sigmoid function to the Scalar."""
        return Sigmoid.apply(self)

    def relu(self) -> Scalar:
        """Apply the ReLU function to the Scalar."""
        return ReLU.apply(self)


def derivative_check(f: Any, *scalars: Scalar) -> None:
    """Checks that autodiff works on a Python function.

    Asserts False if the derivative is incorrect.

    Parameters
    ----------
    f : callable
        A function that takes n `Scalar` inputs and returns a scalar value.
    *scalars : Scalar
        A variable number of Scalar inputs to be used for the derivative check.

    """
    out = f(*scalars)
    out.backward()

    err_msg = """
Derivative check at arguments f(%s) and received derivative f'=%f for argument %d,
but was expecting derivative f'=%f from central difference."""
    for i, x in enumerate(scalars):
        check = central_difference(f, *scalars, arg=i)
        print(str([x.data for x in scalars]), x.derivative, i, check)
        assert x.derivative is not None
        np.testing.assert_allclose(
            x.derivative,
            check.data,
            1e-2,
            1e-2,
            err_msg=err_msg
            % (str([x.data for x in scalars]), x.derivative, i, check.data),
        )
