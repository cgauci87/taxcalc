def is_valid_input(input_string, input_type):
    """
    this method is used to check if the input is
    valid Either it is Y/N (for yes/no)
    OR SMP (for single/married/parient)
    """
    if input_type == "YN":
        if input_string == "Y" or input_string == "N":
            return True
        else:
            return False
    elif input_type == "SMP":
        if input_string == "S" or input_string == "M" or input_string == "P":
            return True
        else:
            return False


class TaxCalculator:
    """
    Base class that will be inherited by the other classes
    """

    def __init__(self):
        self.income = 0
        self.tax = 0
        self.weekly_tax = 0
        self.monthly_tax = 0
        self.yearly_tax = 0

        self.cola_bonus_weekly = 0
        self.cola_bonus_monthly = 0
        self.cola_bonus_yearly = 0

        self.net_income_weekly = 0
        self.net_income_monthly = 0
        self.net_income_yearly = 0

    def calculate_tax(self):
        """
        This method is used to calculate the tax for the user
        """
        pass

    def calculate_net_income(self):
        """
        This method is used to calculate the net income for the user
        """
        pass

    def display_data(self, user_name):
        """
        This method is used to display the data for the user
        """
        print(f"\nGross Salary Breakdown for {user_name} is:")
        print(f"\t\t\t\t\tWeekly\t\t\t\tMonthly\t\t\t\tYearly")
        print(
            f"Gross Salary: \t\t€{round(self.income/52,2)}\t\t\t\t€ \
            {round(self.income/12,2)}\t\t\t\t€{self.income}"
        )
        print(
            f"Tax: \t\t\t\t€{self.weekly_tax}\t\t\t\t€ \
            {self.monthly_tax}\t\t\t\t€{self.yearly_tax}"
        )
        print(
            f"COLA/Bonus: \t\t€{self.cola_bonus_weekly}**\t\t\t\t€ \
            {self.cola_bonus_monthly}**\t\t\t€{self.cola_bonus_yearly}**"
        )
        print(
            f"Net Salary: \t\t€{self.net_income_weekly}\t\t\t\t€ \
            {self.net_income_monthly}\t\t\t€{self.net_income_yearly}"
        )


class ParentTaxCalculator(TaxCalculator):
    """
    Child class that inherits from the Parent class,
    It is used to calculate the tax for the user
    with civil status parent
    """

    def __init__(self, income):
        """ default values for the class """
        self.income = income
        self.cola_bonus_weekly = 9.86
        self.cola_bonus_monthly = 42.71
        self.cola_bonus_yearly = 512.52

    def calculate_tax(self):
        """ calculate the tax for the user with civil status parent """

        # 0 tax for income less than or equal to €10500
        if self.income <= 10500:
            self.tax = 0

        # 15% tax for income between 10501 - €15800
        elif self.income >= 10501 and self.income <= 15800:
            self.tax = ((self.income) * 15 / 100) - 1575

        # 25% tax for income between 15801 - €21200
        elif self.income >= 15801 and self.income <= 21200:
            self.tax = ((self.income) * 25 / 100) - 3155

        # 25% tax for income between 21201 - €60000
        elif self.income >= 21201 and self.income <= 60000:
            self.tax = ((self.income) * 25 / 100) - 3050

        # 35% tax for income above €60000
        elif self.income > 60000:
            self.tax = ((self.income) * 35 / 100) - 9050

        self.weekly_tax = round((self.tax / 52), 2)
        self.monthly_tax = round((self.tax / 12), 2)
        self.yearly_tax = round(self.tax, 2)

    def calculate_net_income(self):
        """ calculate the net income for the user with civil status parent """
        self.net_income_yearly = self.income - self.yearly_tax
        self.net_income_monthly = round(self.net_income_yearly / 12, 2)
        self.net_income_weekly = round(self.net_income_yearly / 52, 2)


class MarriedTaxCalculator(TaxCalculator):
    """
    Child class that inherits from the Parent class,
    It is used to calculate the tax for the user
    with civil status married
    """

    def __init__(self, income):
        """ default values for the class """
        self.income = income
        self.cola_bonus_weekly = 9.86
        self.cola_bonus_monthly = 42.71
        self.cola_bonus_yearly = 512.52

    def calculate_tax(self):
        """ calculate the tax for the user with civil status parent """
        self.tax = 0.0

        # 0 tax for income less than or equal to €12700
        if self.income <= 12700:
            self.tax = 0

        # 15% tax for income between 12701 - €21200
        elif self.income >= 12701 and self.income <= 21200:
            self.tax = ((self.income) * 15 / 100) - 1905

        # 25% tax for income between 21201 - €28700
        elif self.income >= 21201 and self.income <= 28700:
            self.tax = ((self.income) * 25 / 100) - 4025

        # 25% tax for income between 28701 - €60000
        elif self.income >= 28701 and self.income <= 60000:
            self.tax = ((self.income) * 25 / 100) - 3905

        # 35% tax for income above €60000
        elif income > 60000:
            self.tax = ((self.income) * 35 / 100) - 9905

        self.weekly_tax = round((self.tax / 52), 2)
        self.monthly_tax = round((self.tax / 12), 2)
        self.yearly_tax = round(self.tax, 2)

    def calculate_net_income(self):
        """ calculate the net income for the user with civil status married """
        self.net_income_yearly = self.income - self.yearly_tax
        self.net_income_monthly = round(self.net_income_yearly / 12, 2)
        self.net_income_weekly = round(self.net_income_yearly / 52, 2)


class SingleTaxCalculator(TaxCalculator):
    """
    Child class that inherits from the Parent class,
    It is used to calculate the tax for the user
    with civil status single
    """

    def __init__(self, income):
        """ default values for the class """
        self.income = income
        self.cola_bonus_weekly = 9.86
        self.cola_bonus_monthly = 42.71
        self.cola_bonus_yearly = 512.52

    def calculate_tax(self):
        """ calculate the tax for the user with civil status single """
        self.tax = 0.0

        # 0 tax for income less than or equal to €9100
        if self.income <= 9100:
            self.tax = 0

        # 15% tax for income between 9101 - €14500
        elif self.income > 9100 and self.income <= 14500:
            self.tax = ((self.income) * 15 / 100) - 1365

        # 25% tax for income between 14501 - €19500
        elif self.income > 14500 and self.income <= 19500:
            self.tax = ((self.income) * 25 / 100) - 2815

        # 25% tax for income between 19501 - €60000
        elif self.income > 19500 and self.income <= 60000:
            self.tax = ((self.income) * 25 / 100) - 2725

        # 35% tax for income above €60000
        elif self.income > 60000:
            self.tax = ((self.income) * 35 / 100) - 8725

        self.weekly_tax = round((self.tax / 52), 2)
        self.monthly_tax = round((self.tax / 12), 2)
        self.yearly_tax = round(self.tax, 2)

    def calculate_net_income(self):
        """ calculate the net income for the user with civil status single """
        self.net_income_yearly = self.income - self.yearly_tax
        self.net_income_monthly = round(self.net_income_yearly / 12, 2)
        self.net_income_weekly = round(self.net_income_yearly / 52, 2)

    # welcome message , description of the app


print(
    "\n\t\t\t***************************************************************\n"
    "\n\t\t\tWelcome to Malta Tax Calculator. This app will calculate your\n"
    "\t\t\tsalary with income tax according to your input.\n"
    "\t\t\tPlease note that result may vary with your actual salary\n"
    "\t\t\tdue to other deductions such as national insurance,\n"
    "\t\t\tand/or other benefits i.e. allowances and bonuses.\n"
    "\n\t\t\t**************************************************************\n"
)

while True:
    user_name = str(input("Enter your name: ")).capitalize()
    if not validate_name(user_name):
        print("Digits or special characters should not be in name")
        continue
    break
while True:
    instance = None

    # ask the user for the student status
    is_student = str(input("Are you a student? (Y/N): ")).upper()
    if not is_valid_input(is_student, "YN"):
        print(
            "Invalid input! Please try again.. \
        If you are a student - type Y , if not - type N"
        )
        continue
    break
while True:

    # ask the user for the age over 18
    is_over_18_years = str(input("Are you over 18? (Y/N): ")).upper()
    if not is_valid_input(is_over_18_years, "YN"):
        print(
            "Invalid input! Please try again.. \
           If you are over 18 years of age - type Y, if not - type N"
        )
        continue
    break
while True:
    # if the under 18, skip to ask for before 1962 option
    if is_over_18_years == "Y":
        # ask the user for the born before 1962
        is_born_before_1962 = str(input("Are you born before 1962? (Y/N): ")).upper()
        if not is_valid_input(is_born_before_1962, "YN"):
            print(
                "Invalid input! Please try again.. \
           if you were born before 1962 - type Y , if not - type N"
            )
            continue
    break
while True:
    # ask the user for the civil status
    civil_status = str(input("Are you single, married or parent? (S/M/P): ")).upper()
    if not is_valid_input(civil_status, "SMP"):
        print(
            "Invalid input! Please try again.. \
        if your status is Single - type S , \
        if Married - type M , if Parent - type P"
        )
        continue
    break
while True:
    # ask the user for the income
    try:
        income = float(input("Enter your income: "))
    except ValueError:
        print(
            "Invalid input! Please try again by entering your income.\
             Do not include special characters"
        )
        continue
    break
while True:
    if isinstance(income, float) or isinstance(income, int):

        # income value validation
        if income <= 0:
            print("Income should be greater than 0. Please try again.")
        continue
    break

while True:
    # create an instance of the class based on the user input
    if civil_status == "S":
        instance = SingleTaxCalculator(income)
    elif civil_status == "M":
        instance = MarriedTaxCalculator(income)
    elif civil_status == "P":
        instance = ParentTaxCalculator(income)
    if instance:

        # calculate the tax for the user
        instance.calculate_tax()

        # calculate the net income for the user
        instance.calculate_net_income()

        # print the results
        instance.display_data()

        # Want to continue?
        continue_input = str(
            input("Would you like to calculate other salary?(Y/N):")
        ).upper()
        if not is_valid_input(continue_input, "YN"):
            print("Invalid input! Please try again, by either type Y or N.")
            continue

        if continue_input == "N":
            # terminate the program
            print(f"Thank you for using this app, {user_name}!")
            break
        else:
            # continue the program - OK
            print("\n\n")
            continue
    else:
        # if there is an unexpected error in the input
        print("Oops! Something went wrong..")
        continue
