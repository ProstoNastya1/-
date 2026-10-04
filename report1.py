from fractions import Fraction

def minor(matrix, row, col):
    return [
        [value for j, value in enumerate(line) if j != col]
        for i, line in enumerate(matrix)
        if i != row
    ]

def determinant(matrix):
    n = len(matrix)

    if n == 0:
        return Fraction(1)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return (
            matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]
        )

    return sum(
        (-1) ** j * matrix[0][j]
        * determinant(minor(matrix, 0, j))
        for j in range(n)
    )

def inverse_determinant(matrix):
    n = len(matrix)
    det = determinant(matrix)

    if det == 0:
        raise ValueError("행렬식이 0이므로 역행렬이 존재하지 않습니다.")

    return [
        [
            (-1) ** (i + j)
            * determinant(minor(matrix, j, i)) / det
            for j in range(n)
        ]
        for i in range(n)
    ]

def inverse_gauss_jordan(matrix):
    n = len(matrix)
    augmented = [
        matrix[i][:] + [Fraction(i == j) for j in range(n)]
        for i in range(n)
    ]

    for col in range(n):
        pivot = max(
            range(col, n),
            key=lambda row: abs(augmented[row][col])
        )

        if augmented[pivot][col] == 0:
            raise ValueError("역행렬이 존재하지 않습니다.")

        augmented[col], augmented[pivot] = (
            augmented[pivot], augmented[col]
        )
        divisor = augmented[col][col]
        augmented[col] = [
            value / divisor for value in augmented[col]
        ]

        for row in range(n):
            if row == col:
                continue

            factor = augmented[row][col]
            augmented[row] = [
                augmented[row][j] - factor * augmented[col][j]
                for j in range(2 * n)
            ]
    return [row[n:] for row in augmented]

def print_matrix(matrix):
    for row in matrix:
        print("  ".join(str(value) for value in row))

def multiply_matrices(a, b):
    n = len(a)

    return [
        [
            sum(a[i][k] * b[k][j] for k in range(n))
            for j in range(n)
        ]
        for i in range(n)
    ]


def verify_inverse(matrix, inverse):
    n = len(matrix)
    product = multiply_matrices(matrix, inverse)

    identity = [
        [Fraction(i == j) for j in range(n)]
        for i in range(n)
    ]

    print("원본 행렬 × 역행렬:")
    print_matrix(product)

    if product == identity:
        print("검증 성공: 곱이 단위행렬이므로 올바른 역행렬입니다.")
    else:
        print("검증 실패: 곱이 단위행렬이 아닙니다.")

def main():
    try:
        n = int(input("행렬의 크기 n을 입력하세요: "))

        if n <= 0:
            raise ValueError("n은 양의 정수여야 합니다.")

        matrix = []

        print("각 행의 원소를 공백으로 구분하여 입력하세요.")

        for i in range(n):
            values = input(f"{i + 1}행: ").split()

            if len(values) != n:
                raise ValueError(f"각 행에는 {n}개의 원소가 필요합니다.")

            matrix.append([Fraction(value) for value in values])

    except (ValueError, ZeroDivisionError) as error:
        print(f"입력 오류: {error}")
        return

    result_det = None
    result_gauss = None

    print("\n[행렬식을 이용한 역행렬]")
    try:
        result_det = inverse_determinant(matrix)
        print_matrix(result_det)
    except ValueError as error:
        print(f"오류: {error}")

    print("\n[가우스-조던 소거법을 이용한 역행렬]")
    try:
        result_gauss = inverse_gauss_jordan(matrix)
        print_matrix(result_gauss)
    except ValueError as error:
        print(f"오류: {error}")

    print("\n[결과 비교]")
    if result_det is None or result_gauss is None:
        print("역행렬이 존재하지 않아 비교할 수 없습니다.")
    elif result_det == result_gauss:
        print("두 방법으로 계산한 역행렬이 동일합니다.")
    else:
        print("두 방법으로 계산한 역행렬이 다릅니다.")

    print("\n[추가 기능: 역행렬 정확성 검증]")

    if result_det is not None:
        print("\n행렬식 방법 검증")
        verify_inverse(matrix, result_det)

    if result_gauss is not None:
        print("\n가우스-조던 방법 검증")
        verify_inverse(matrix, result_gauss)

    if result_det is None and result_gauss is None:
        print("역행렬이 존재하지 않아 검증할 수 없습니다.")


if __name__ == "__main__":
    main()
