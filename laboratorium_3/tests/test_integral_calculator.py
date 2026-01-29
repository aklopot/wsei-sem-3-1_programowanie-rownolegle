import pytest
from src.modules.integral_calculator import IntegralCalculator


class TestIntegralCalculator:

    @pytest.fixture
    def calculator(self):
        return IntegralCalculator()

    def test_initialization(self, calculator):
        assert calculator is not None
        assert isinstance(calculator, IntegralCalculator)

    def test_function_task1_1(self, calculator):
        # y = 2x + 2x² dla x=0 powinno być 0
        assert calculator.function_task1_1(0) == 0
        # y = 2x + 2x² dla x=1 powinno być 2 + 2 = 4
        assert calculator.function_task1_1(1) == 4
        # y = 2x + 2x² dla x=2 powinno być 4 + 8 = 12
        assert calculator.function_task1_1(2) == 12

    def test_function_task1_2(self, calculator):
        # y = 2x² dla x=0 powinno być 0
        assert calculator.function_task1_2(0) == 0
        # y = 2x² dla x=1 powinno być 2
        assert calculator.function_task1_2(1) == 2
        # y = 2x² dla x=3 powinno być 18
        assert calculator.function_task1_2(3) == 18

    def test_function_task1_3(self, calculator):
        # y = 2x - 3 dla x=0 powinno być -3
        assert calculator.function_task1_3(0) == -3
        # y = 2x - 3 dla x=2 powinno być 1
        assert calculator.function_task1_3(2) == 1
        # y = 2x - 3 dla x=5 powinno być 7
        assert calculator.function_task1_3(5) == 7

    def test_calculate_integral_trapezoids_simple(self, calculator):
        # Całka z f(x) = 2x od 0 do 2 powinna wynosić x² = 4
        result = calculator._calculate_integral_trapezoids_simple(
            0, 2, 1000, lambda x: 2 * x
        )
        assert abs(result - 4.0) < 0.01

    def test_calculate_integral_trapezoids_simple_quadratic(self, calculator):
        # Całka z f(x) = x² od 0 do 3 powinna wynosić x³/3 = 9
        result = calculator._calculate_integral_trapezoids_simple(
            0, 3, 1000, lambda x: x ** 2
        )
        assert abs(result - 9.0) < 0.01

    def test_calculate_integral_trapezoids_negative_interval(self, calculator):
        # Całka z f(x) = 2x od -2 do 2 powinna wynosić 0 (symetryczna)
        result = calculator._calculate_integral_trapezoids_simple(
            -2, 2, 1000, lambda x: 2 * x
        )
        assert abs(result - 0.0) < 0.01

