import streamlit as st
from pulp import *
from PIL import Image

# Function to align input fields to the left
def left_align():
    st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Function to align output to the right
def right_align():
    st.markdown('<style>div.row-widget.stButton > button{margin-left:auto}</style>', unsafe_allow_html=True)

def solve_integer_programming(obj_coefficients, num_vars, restricted_vars, constraint_coeffs, constraint_signs, rhs_entries, optimization_mode):
    # Create the problem variable
    prob = LpProblem("Integer_Programming_Problem", LpMaximize if optimization_mode == "Maximize" else LpMinimize)

    # Define the decision variables
    decision_vars = []
    for i in range(num_vars):
        var_name = f"x{i+1}"
        var_type = 'Integer' if restricted_vars[i] else 'Continuous'
        var = LpVariable(var_name, lowBound=0, cat=var_type)
        decision_vars.append(var)

    # Define the objective function
    objective = lpSum(obj_coefficients[i] * decision_vars[i] for i in range(len(decision_vars)))
    if any(val < 0 for val in obj_coefficients):
        negative_value=0
    else:
        negative_value=1
    if negative_value==0:
        if optimization_mode == "Maximize":
            prob += (objective)*-1
        else:
            prob += objective
    else:
        if optimization_mode=="Maximize":
            prob += objective
        else:
            prob += -(objective)
    # Define the constraints
    for i in range(len(constraint_coeffs)):
        constraint_expr = lpSum(constraint_coeffs[i][j] * decision_vars[j] for j in range(len(decision_vars)))
        if constraint_signs[i] == "<=":
            prob += constraint_expr <= float(rhs_entries[i])
        elif constraint_signs[i] == "=":
            prob += constraint_expr == float(rhs_entries[i])
        else:
            prob += constraint_expr >= float(rhs_entries[i])

    # Solve the problem
    prob.solve()

    # Print the results
    result = "Optimal Solution:\n"
    for var in decision_vars:
        result += f"{var.name} = {var.varValue}\n"
    result += f"Objective Value: {int(prob.objective.value())}"
    return result


# Login page
def login():
    st.write("Login")
    form = st.form(key='login_form')
    email = form.text_input("Email", value='', key='email_input')
    password = form.text_input("Password", value='', type="password", key='password_input')
    submit = form.form_submit_button("Submit")

    if submit:
        if email.strip() == '' or password.strip() == '':
            st.error("Email and password are required.")
        else:
            # Add your login validation code here
            if email == "example@example.com" and password == "password":
                st.success("Logged in successfully!")
                # Set the logged_in session state variable to True
                st.session_state.logged_in = True
                # Set the email session state variable
                st.session_state.email = email
                # Redirect to the calculator page
                st.experimental_rerun()
            else:
                st.error("Invalid credentials!")


# Streamlit app
def main():
    # Add a red border to the sidebar
    st.sidebar.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            border-right: 12px solid red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
        .title-wrapper {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <style>
    .dual-color-title {
        background: linear-gradient(90deg, #ff0000, #0000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.markdown("<h1><span class='dual-color-title'>Integer Programming Solver</span></h1>", unsafe_allow_html=True)

   # Add rounded image
    image_path = Image.open("srixlogo2 (2).png")
    st.sidebar.image(image_path, width=150, caption="Srix", use_column_width=False, output_format="PNG", clamp=False)
    
    # Add text below the image

    menu = st.sidebar.selectbox("Menu", ["Homepage", "Calculator","Formulation"])
    if st.session_state.logged_in:
        email = st.session_state.email
        st.sidebar.write("Logged in as:", email)  # Display horizontally

    if menu == "Homepage":
        st.title("Home")
        col1, col2 = st.columns([2, 4])
        with col1:
            image = Image.open('inventory_1.jpg')
            st.image(image, use_column_width=True)
        with col2:
            st.write("Integer programming is used in real life because it provides a powerful tool for solving optimization problems that involve discrete decision-making. Here are some reasons why integer programming is widely used in various real-world applications:")
        st.write("1.  Resource Allocation: Integer programming is used for optimizing the allocation of limited resources, such as personnel, machines, or funds, to different tasks or projects. By considering integer constraints, it ensures that resources are allocated in an efficient and practical manner, taking into account discrete units or availability.")
        st.write("2.  Production Planning: Integer programming helps in optimizing production plans, including determining the quantities and types of products to produce, scheduling production activities, and managing inventory levels. Integer constraints are often used to represent the discrete nature of production quantities or setup decisions.")
        st.write("3.  Network Design and Routing: Integer programming is applied to solve problems related to network design and routing, such as determining the optimal layout of transportation or telecommunication networks, selecting routes for vehicles or data transmission, or locating facilities. Integer variables can represent discrete decisions, such as the presence or absence of connections or the assignment of resources to specific locations.")
        st.write("4.  Project Scheduling: Integer programming is utilized in project management for optimizing project schedules, taking into account task dependencies, resource constraints, and other project-specific requirements. Integer variables help represent discrete decisions such as the start or end times of activities or the assignment of tasks to specific resources.")
        st.write("5.  Location Planning: Integer programming is useful in determining the optimal locations for facilities, warehouses, or distribution centers to minimize transportation costs, satisfy customer demand, or maximize coverage. Integer variables represent discrete decisions about the presence or absence of facilities at specific locations.")
        st.write("6.  Cutting Stock Problems: Integer programming is applied to solve cutting stock problems, where a set of items needs to be cut from larger stock items with minimal waste. Integer variables are used to represent the number of times a pattern is used for cutting.")
        st.write("These are just a few examples of the many real-life applications of integer programming. Its ability to handle discrete decisions makes it a valuable tool for optimizing complex systems and decision-making processes in various domains.")
    if menu == "Formulation":
        st.title("Formulation")
        col3, col4 = st.columns([4, 3])
        with col4:
            image = Image.open('transport.jpeg')
            st.image(image, use_column_width=True)
        with col3:
            st.write("Integer programming is a mathematical optimization technique used to solve optimization problems where the decision variables are required to take integer values. It is an extension of linear programming, which deals with continuous variables.")
            st.write("In integer programming, the objective is to find the optimal values of decision variables that satisfy a given set of constraints and optimize an objective function, while also ensuring that the variables are restricted to integer values.")
        st.write("""

The general form of an integer programming problem can be stated as follows:

Minimize (or maximize) Z = c₁x₁ + c₂x₂ + ... + cₙxₙ

subject to:

a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ ≤ b₁

a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ ≤ b₂

...

aₘ₁x₁ + aₘ₂x₂ + ... + aₘₙxₙ ≤ bₘ

x₁, x₂, ..., xₙ are integer variables (xᵢ ∈ ℤ), and c₁, c₂, ..., cₙ, b₁, b₂, ..., bₘ, a₁₁, a₁₂, ..., aₘₙ are known coefficients.

The main challenge in integer programming is that the inclusion of integer variables introduces a discrete and combinatorial aspect to the problem, making it more difficult to solve compared to continuous optimization problems. While linear programming problems can be solved using efficient algorithms like the simplex method, integer programming problems often require specialized algorithms such as branch and bound, cutting plane methods, or mixed-integer linear programming (MILP) techniques.

Integer programming finds applications in various fields, including operations research, logistics, production planning, scheduling, network design, and many other areas where decisions need to be made using discrete values rather than continuous ones.

""")
        # Add your model code here
    elif menu == "Calculator":
        if st.session_state.logged_in:
            st.write("Calculator")

            # Get the number of variables and constraints
            num_vars = st.number_input("Enter the number of variables:", value=1, step=1)
            num_constraints = st.number_input("Enter the number of constraints:", value=1, step=1)

            if st.button("Reset"):
                st.experimental_rerun()

            if num_vars > 0 and num_constraints > 0:
                left_align()

                # Move objective function coefficients below the number of constraints
                st.write("---")
                st.header("Objective Function Coefficients")

                # Get the objective function coefficients
                obj_coefficients = []
                for i in range(num_vars):
                    coeff = st.number_input(f"Enter the coefficient for x{i+1}:")
                    obj_coefficients.append(coeff)

                # Get the restricted variables
                restricted_vars = []
                for i in range(num_vars):
                    value2 = st.selectbox(f"Select the restriction for x{i+1}:", options=["Unrestricted", "Restricted"])
                    restricted_vars.append(value2 == "Restricted")

                # Get the constraint coefficients and right-hand sides
                constraint_coeffs = []
                constraint_signs = []
                rhs_entries = []
                st.write("---")
                st.header("Constraints")
                for i in range(num_constraints):
                    constraint_coefficients = []
                    for j in range(num_vars):
                        coeff = st.number_input(f"Enter the coefficient for x{j+1} in constraint {i+1}:")
                        constraint_coefficients.append(coeff)
                    constraint_coeffs.append(constraint_coefficients)

                    sign = st.selectbox(f"Select the sign for constraint {i+1}:", options=["<=", ">=", "="])
                    constraint_signs.append(sign)

                    rhs = st.number_input(f"Enter the right-hand side for constraint {i+1}:")
                    rhs_entries.append(rhs)

                # Get the optimization mode
                optimization_mode = st.selectbox("Select the optimization mode:", options=["Maximize", "Minimize"])

                if st.button("Solve"):
                    result = solve_integer_programming(obj_coefficients, num_vars, restricted_vars, constraint_coeffs, constraint_signs, rhs_entries, optimization_mode)
                    st.text(result)
            else:
                if st.sidebar.button("Login", key="login_button", on_click=login):
                    st.session_state.logged_in = True
        else:
            # Display login form
            login()

    # Display login button in the sidebar
    if not st.session_state.logged_in:
        st.sidebar.title("User")
        if st.sidebar.button("Login"):
            login()


# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'email' not in st.session_state:
    st.session_state.email = ''

if __name__ == "__main__":
    main()
    right_align()
