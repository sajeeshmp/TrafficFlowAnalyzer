import streamlit as st
import numpy as np
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Traffic Flow Analyzer",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Traffic Flow Analyzer")
st.markdown("### Solve Traffic Flow Equations using Numerical Methods")

st.write(
    "This application calculates traffic flow using "
    "Gauss Elimination, Jacobi Method, and Gauss-Seidel Method."
)

# Number of variables
n = st.number_input(
    "Number of Roads (Variables)",
    min_value=2,
    max_value=10,
    value=3
)

st.subheader("Enter Coefficient Matrix (A)")

A = []

for i in range(n):
    row = st.text_input(
        f"Equation {i+1} Coefficients (space-separated)",
        key=f"row{i}"
    )
    A.append(row)

st.subheader("Enter Constant Terms (b)")

b = []

for i in range(n):
    value = st.number_input(
        f"b[{i+1}]",
        value=0.0,
        key=f"b{i}"
    )
    b.append(value)

method = st.selectbox(
    "Choose Numerical Method",
    ["Gauss Elimination", "Jacobi", "Gauss-Seidel"]
)

if st.button("🚀 Solve"):

    try:
        A_matrix = []

        for row in A:
            values = list(map(float, row.split()))

            if len(values) != n:
                st.error(
                    f"Each equation must contain exactly {n} coefficients."
                )
                st.stop()

            A_matrix.append(values)

        A_matrix = np.array(A_matrix)
        b_vector = np.array(b)

        # Gauss Elimination
        if method == "Gauss Elimination":
            solution = np.linalg.solve(A_matrix, b_vector)

        # Jacobi Method
        elif method == "Jacobi":

            solution = np.zeros(n)

            for _ in range(50):

                new_solution = np.copy(solution)

                for i in range(n):
                    s = sum(
                        A_matrix[i][j] * solution[j]
                        for j in range(n)
                        if j != i
                    )

                    new_solution[i] = (
                        b_vector[i] - s
                    ) / A_matrix[i][i]

                solution = new_solution

        # Gauss-Seidel
        elif method == "Gauss-Seidel":

            solution = np.zeros(n)

            for _ in range(50):

                for i in range(n):

                    s = sum(
                        A_matrix[i][j] * solution[j]
                        for j in range(n)
                        if j != i
                    )

                    solution[i] = (
                        b_vector[i] - s
                    ) / A_matrix[i][i]

        st.success("Solution Found Successfully ✅")

        result_df = pd.DataFrame({
            "Road": [f"Road {i+1}" for i in range(n)],
            "Traffic Flow": solution
        })

        st.subheader("Traffic Flow Results")
        st.dataframe(result_df)

        st.subheader("Traffic Flow Visualization")
        st.bar_chart(
            result_df.set_index("Road")
        )

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.markdown(
    "Developed using Streamlit, NumPy, and Numerical Methods 🚦"
)
