"""
Zestaw testów dla modułu FibonacciCalculator.
Testy obejmują podstawową funkcjonalność obliczania ciągu Fibonacciego.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.modules.fibonacci_calculator import FibonacciCalculator


class TestFibonacciCalculator:
    """Klasa testowa dla FibonacciCalculator."""

    @pytest.fixture
    def calculator(self):
        """Fixture do utworzenia instancji FibonacciCalculator."""
        return FibonacciCalculator()

    def test_initialization(self, calculator):
        """Test, że kalkulator inicjalizuje się bez błędów."""
        assert calculator is not None
        assert isinstance(calculator, FibonacciCalculator)

    def test_display_fibonacci_range_first_five(self, calculator, capsys):
        """Test wyświetlania pierwszych 5 liczb Fibonacciego."""
        calculator.display_fibonacci_range(0, 5)
        captured = capsys.readouterr()
        
        assert "Ciąg Fibonacciego:" in captured.out
        assert "F[0] = 0" in captured.out
        assert "F[1] = 1" in captured.out
        assert "F[2] = 1" in captured.out
        assert "F[3] = 2" in captured.out
        assert "F[4] = 3" in captured.out

    def test_display_fibonacci_range_from_index_3(self, calculator, capsys):
        """Test wyświetlania liczb Fibonacciego od indeksu 3."""
        calculator.display_fibonacci_range(3, 3)
        captured = capsys.readouterr()
        
        assert "Ciąg Fibonacciego:" in captured.out
        assert "F[3] = 3" in captured.out
        assert "F[4] = 5" in captured.out
        assert "F[5] = 8" in captured.out

    def test_display_fibonacci_single_element(self, calculator, capsys):
        """Test wyświetlania pojedynczej liczby Fibonacciego."""
        calculator.display_fibonacci_range(0, 1)
        captured = capsys.readouterr()
        
        assert "F[0] = 0" in captured.out

    def test_display_fibonacci_large_index(self, calculator, capsys):
        """Test wyświetlania liczb Fibonacciego dla dużych indeksów."""
        calculator.display_fibonacci_range(10, 2)
        captured = capsys.readouterr()
        
        assert "F[10] = 89" in captured.out
        assert "F[11] = 144" in captured.out

    @patch('src.validators.input_validator.InputValidator.get_positive_integer')
    def test_run_task1_valid_input(self, mock_input, calculator, capsys):
        """Test run_task1 ze ważnymi danymi."""
        mock_input.return_value = 5
        
        calculator.run_task1()
        captured = capsys.readouterr()
        
        assert "Ciąg Fibonacciego:" in captured.out
        assert "F[0] = 0" in captured.out
        assert "F[4] = 3" in captured.out

    @patch('src.validators.input_validator.InputValidator.get_positive_integer')
    def test_run_task1_single_element(self, mock_input, calculator, capsys):
        """Test run_task1 z pojedynczym elementem."""
        mock_input.return_value = 1
        
        calculator.run_task1()
        captured = capsys.readouterr()
        
        assert "F[0] = 0" in captured.out

    @patch('src.validators.input_validator.InputValidator.get_non_negative_integer')
    @patch('src.validators.input_validator.InputValidator.get_positive_integer')
    def test_run_task2_valid_input(self, mock_count, mock_start, calculator, capsys):
        """Test run_task2 ze ważnymi danymi."""
        mock_start.return_value = 2
        mock_count.return_value = 4
        
        calculator.run_task2()
        captured = capsys.readouterr()
        
        assert "Ciąg Fibonacciego:" in captured.out
        assert "F[2] = 2" in captured.out
        assert "F[3] = 3" in captured.out
        assert "F[4] = 5" in captured.out
        assert "F[5] = 8" in captured.out

    @patch('src.validators.input_validator.InputValidator.get_non_negative_integer')
    @patch('src.validators.input_validator.InputValidator.get_positive_integer')
    def test_run_task2_from_index_zero(self, mock_count, mock_start, calculator, capsys):
        """Test run_task2 od indeksu 0."""
        mock_start.return_value = 0
        mock_count.return_value = 3
        
        calculator.run_task2()
        captured = capsys.readouterr()
        
        assert "F[0] = 0" in captured.out
        assert "F[1] = 1" in captured.out
        assert "F[2] = 1" in captured.out
