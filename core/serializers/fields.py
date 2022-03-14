import re

from rest_framework import serializers


class CPFField(serializers.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.cpf_validator)

    def cpf_validator(self, cpf):
        if not cpf:
            raise serializers.ValidationError('CPF inválido.')

        # if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        if not re.fullmatch(r'\d{11}', cpf):
            raise serializers.ValidationError('CPF deve conter 11 dígitos.')

        numbers = [int(digit) for digit in cpf]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            raise serializers.ValidationError('CPF deve conter 11 dígitos.')

        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise serializers.ValidationError('CPF inválido.')

        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise serializers.ValidationError('CPF inválido.')


class DAPField(serializers.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.dap_validator)

    def dap_validator(self, dap):
        if not dap:
            raise serializers.ValidationError('DAP inválido.')

        if not re.fullmatch(r'[A-Z]{3}\d{22}', dap):
            raise serializers.ValidationError('DAP deve estar no formato: [A-Z]{3}[0-9]{22}.')


class CREAField(serializers.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.crea_validator)

    def crea_validator(self, crea):
        if not crea:
            raise serializers.ValidationError('Crea inválido.')

        if not re.fullmatch(r'\d{10}', crea):
            raise serializers.ValidationError('Crea deve possuir 10 digitos.')
