from tabulate import tabulate
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("taxcalc_user_data")
salaries = SHEET.worksheet("salaries")


def is_valid_input(input_string, input_type):
    """
    this method is used to check validation - if the input is
    valid; Either it is Y/N (for yes/no)
    OR SMP (for single/married/parent)
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


def validate_name(name):
    # scan number and special character
    if name.replace(" ", "").isalpha():
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
        This method is used to display the data
        """
        print(f"\nSalary Breakdown for {user_name} is:")
        print(f"\t\t\t\t\tWeekly\t\t\t\tMonthly\t\t\t\tYearly")
        print(
            f"Gross Salary: \t\t???{round(self.income / 52, 2)}\t\t\t\t??? \
            {round(self.income / 12, 2)}\t\t\t\t???{self.income}"
        )
        print(
            f"Tax: \t\t\t\t???{self.weekly_tax}\t\t\t\t??? \
            {self.monthly_tax}\t\t\t\t???{self.yearly_tax}"
        )
        print(
            f"COLA/Bonus: \t\t???{self.cola_bonus_weekly}**\t\t\t\t??? \
            {self.cola_bonus_monthly}**\t\t\t???{self.cola_bonus_yearly}**"
        )
        print(
            f"Net Salary: \t\t???{self.net_income_weekly}\t\t\t\t??? \
            {self.net_income_monthly}\t\t\t???{self.net_income_yearly}"
        )

    def store_data_in_google_sheet(self):

        # Insert row in google spreadsheet to store the user data
        row_data = [
            user_name,
            round(self.income / 52, 2),
            round(self.income / 12, 2),
            self.income,
            self.weekly_tax,
            self.monthly_tax,
            self.yearly_tax,
            self.cola_bonus_weekly,
            self.cola_bonus_monthly,
            self.cola_bonus_yearly,
            self.net_income_weekly,
            self.net_income_monthly,
            self.net_income_yearly,
        ]
        salaries.append_row(row_data)
        return

    def display_google_sheet_data(self):
        pass


class ParentTaxCalculator(TaxCalculator):
    """
    Child class that inherits from the Parent class,
    It is used to calculate the tax for a user
    with civil status parent
    """

    def __init__(self, income):
        """default values for the class"""
        self.income = income
        self.cola_bonus_weekly = 9.86
        self.cola_bonus_monthly = 42.71
        self.cola_bonus_yearly = 512.52

    def calculate_tax(self):
        """calculate the tax for the user with civil status parent"""

        # 0 tax for income less than or equal to ???10500
        if self.income <= 10500:
            self.tax = 0
        # 15% tax for income between 10501 - ???15800
        elif self.income >= 10501 and self.income <= 15800:
            self.tax = ((self.income) * 15 / 100) - 1575
        # 25% tax for income between 15801 - ???21200
        elif self.income >= 15801 and self.income <= 21200:
            self.tax = ((self.income) * 25 / 100) - 3155
        # 25% tax for income between 21201 - ???60000
        elif self.income >= 21201 and self.income <= 60000:
            self.tax = ((self.income) * 25 / 100) - 3050
        # 35% tax for income above ???60000
        elif self.income > 60000:
            self.tax = ((self.income) * 35 / 100) - 9050
        self.weekly_tax = round((self.tax / 52), 2)
        self.monthly_tax = round((self.tax / 12), 2)
        self.yearly_tax = round(self.tax, 2)

    def calculate_net_income(self):
        """calculate the net income for the user with civil status parent"""
        self.net_income_yearly = self.income - self.yearly_tax
        self.net_income_monthly = round(self.net_income_yearly / 12, 2)
        self.net_income_weekly = round(self.net_income_yearly / 52, 2)

    def calculate_gross_income(self):
        self.gross_income_yearly = self.income
        self.gross_income_monthly = round(self.gross_income_yearly / 12, 2)
        self.gross_income_weekly = round(self.gross_income_yearly / 52, 2)

    def display_data(self, user_name):
        """
        This method is used to display the data for the user
        """
        print(f"\nSalary Breakdown for {user_name} is:")
        data = [
            [
                "Gross Salary: ",
                self.gross_income_weekly,
                self.gross_income_monthly,
                self.gross_income_yearly,
            ],
            ["Tax: ", self.weekly_tax, self.monthly_tax, self.yearly_tax],
            [
                "COLA/Bonus: ",
                self.cola_bonus_weekly,
                self.cola_bonus_monthly,
                self.cola_bonus_yearly,
            ],
            [
                "Net Salary: ",
                self.net_income_weekly,
                self.net_income_monthly,
                self.net_income_yearly,
            ],
        ]
        print(
            tabulate(
                data,
                headers=[
                    "Weekly",
                    "Monthly",
                    "Yearly",
                ],
            )
        )

    def display_google_sheet_data(self):
        """
        This method is used to display the data from google spreadsheet
        """
        google_spread_sheet_data = salaries.get_all_values()
        print(f"\n\n{20*'*'}Google Spread Sheet Data:{20*'*'}")
        google_spread_sheet_data = google_spread_sheet_data[1:]

        for row in google_spread_sheet_data:
            print(f"\nSalary Breakdown for {row[0]} is:")
            data = [
                ["Gross Salary: ", row[1], row[2], row[3]],
                ["Tax: ", row[4], row[5], row[6]],
                ["COLA/Bonus: ", row[7], row[8], row[9]],
                ["Net Salary: ", row[10], row[11], row[12]],
            ]
            print(
                tabulate(
                    data,
                    headers=[
                        "Weekly",
                        "Monthly",
                        "Yearly",
                    ],
                ),
                "\n",
            )
        print(40 * "*")


class MarriedTaxCalculator(TaxCalculator):
    """
    Child class that inherits from the Parent class,
    It is used to calculate the tax for a user
    with civil status married
    """

    def __init__(self, income):
        """default values for the class"""
        self.income = income
        self.cola_bonus_weekly = 9.86
        self.cola_bonus_monthly = 42.71
        self.cola_bonus_yearly = 512.52

    def calculate_tax(self):
        """calculate the tax for the user with civil status parent"""
        self.tax = 0.0

        # 0 tax for income less than or equal to ???12700
        if self.income <= 12700:
            self.tax = 0
        # 15% tax for income between 12701 - ???21200
        elif self.income >= 12701 and self.income <= 21200:
            self.tax = ((self.income) * 15 / 100) - 1905
        # 25% tax for income between 21201 - ???28700
        elif self.income >= 21201 and self.income <= 28700:
            self.tax = ((self.income) * 25 / 100) - 4025
        # 25% tax for income between 28701 - ???60000
        elif self.income >= 28701 and self.income <= 60000:
            self.tax = ((self.income) * 25 / 100) - 3905
        # 35% tax for income above ???60000
        elif income > 60000:
            self.tax = ((self.income) * 35 / 100) - 9905
        self.weekly_tax = round((self.tax / 52), 2)
        self.monthly_tax = round((self.tax / 12), 2)
        self.yearly_tax = round(self.tax, 2)

    def calculate_net_income(self):
        """calculate the net income for the user with civil status married"""
        self.net_income_yearly = self.income - self.yearly_tax
        self.net_income_monthly = round(self.net_income_yearly / 12, 2)
        self.net_income_weekly = round(self.net_income_yearly / 52, 2)

    def calculate_gross_income(self):
        self.gross_income_yearly = self.income
        self.gross_income_monthly = round(self.gross_income_yearly / 12, 2)
        self.gross_income_weekly = round(self.gross_income_yearly / 52, 2)

    def display_data(self, user_name):
        """
        This method is used to display the data for the user
        """
        print(f"\nSalary Breakdown for {user_name} is:")
        data = [
            [
                "Gross Salary: ",
                self.gross_income_weekly,
                self.gross_income_monthly,
                self.gross_income_yearly,
            ],
            ["Tax: ", self.weekly_tax, self.monthly_tax, self.yearly_tax],
            [
                "COLA/Bonus: ",
                self.cola_bonus_weekly,
                self.cola_bonus_monthly,
                self.cola_bonus_yearly,
            ],
            [
                "Net Salary: ",
                self.net_income_weekly,
                self.net_income_monthly,
                self.net_income_yearly,
            ],
        ]
        print(
            tabulate(
                data,
                headers=[
                    "Weekly",
                    "Monthly",
                    "Yearly",
                ],
            )
        )

    def display_google_sheet_data(self):
        """
        This method is used to display the data from google spread sheet
        """
        google_spread_sheet_data = salaries.get_all_values()
        print(f"\n\n{20*'*'}Historical Data:{20*'*'}")
        google_spread_sheet_data = google_spread_sheet_data[1:]

        for row in google_spread_sheet_data:
            print(f"\nSalary Breakdown for {row[0]} is:")
            data = [
                ["Gross Salary: ", row[1], row[2], row[3]],
                ["Tax: ", row[4], row[5], row[6]],
                ["COLA/Bonus: ", row[7], row[8], row[9]],
                ["Net Salary: ", row[10], row[11], row[12]],
            ]
            print(
                tabulate(
                    data,
                    headers=[
                        "Weekly",
                        "Monthly",
                        "Yearly",
                    ],
                ),
                "\n",
            )
        print(40 * "*")


class SingleTaxCalculator(TaxCalculator):
    """
    Child class that inherits from the Parent class,
    It is used to calculate the tax for a user
    with civil status single
    """

    def __init__(self, income):
        """default values for the class"""
        self.income = income
        self.cola_bonus_weekly = 9.86
        self.cola_bonus_monthly = 42.71
        self.cola_bonus_yearly = 512.52

    def calculate_tax(self):
        """calculate the tax for the user with civil status single"""
        self.tax = 0.0

        # 0 tax for income less than or equal to ???9100
        if self.income <= 9100:
            self.tax = 0
        # 15% tax for income between 9101 - ???14500
        elif self.income > 9100 and self.income <= 14500:
            self.tax = ((self.income) * 15 / 100) - 1365
        # 25% tax for income between 14501 - ???19500
        elif self.income > 14500 and self.income <= 19500:
            self.tax = ((self.income) * 25 / 100) - 2815
        # 25% tax for income between 19501 - ???60000
        elif self.income > 19500 and self.income <= 60000:
            self.tax = ((self.income) * 25 / 100) - 2725
        # 35% tax for income above ???60000
        elif self.income > 60000:
            self.tax = ((self.income) * 35 / 100) - 8725
        self.weekly_tax = round((self.tax / 52), 2)
        self.monthly_tax = round((self.tax / 12), 2)
        self.yearly_tax = round(self.tax, 2)

    def calculate_net_income(self):
        """calculate the net income for the user with civil status single"""
        self.net_income_yearly = self.income - self.yearly_tax
        self.net_income_monthly = round(self.net_income_yearly / 12, 2)
        self.net_income_weekly = round(self.net_income_yearly / 52, 2)

    def calculate_gross_income(self):
        self.gross_income_yearly = self.income
        self.gross_income_monthly = round(self.gross_income_yearly / 12, 2)
        self.gross_income_weekly = round(self.gross_income_yearly / 52, 2)

    def display_data(self, user_name):
        """
        This method is used to display the data for the user
        """
        print(f"\nSalary Breakdown for {user_name} is:")
        data = [
            [
                "Gross Salary: ",
                self.gross_income_weekly,
                self.gross_income_monthly,
                self.gross_income_yearly,
            ],
            ["Tax: ", self.weekly_tax, self.monthly_tax, self.yearly_tax],
            [
                "COLA/Bonus: ",
                self.cola_bonus_weekly,
                self.cola_bonus_monthly,
                self.cola_bonus_yearly,
            ],
            [
                "Net Salary: ",
                self.net_income_weekly,
                self.net_income_monthly,
                self.net_income_yearly,
            ],
        ]
        print(
            tabulate(
                data,
                headers=[
                    "Weekly",
                    "Monthly",
                    "Yearly",
                ],
            )
        )

    def display_google_sheet_data(self):
        """
        This method is used to display the data from google spread sheet
        """
        google_spread_sheet_data = salaries.get_all_values()
        print(f"\n\n{20*'*'}Historical Data:{20*'*'}")
        google_spread_sheet_data = google_spread_sheet_data[1:]

        for row in google_spread_sheet_data:
            print(f"\nSalary Breakdown for {row[0]} is:")
            data = [
                ["Gross Salary: ", row[1], row[2], row[3]],
                ["Tax: ", row[4], row[5], row[6]],
                ["COLA/Bonus: ", row[7], row[8], row[9]],
                ["Net Salary: ", row[10], row[11], row[12]],
            ]
            print(
                tabulate(
                    data,
                    headers=[
                        "Weekly",
                        "Monthly",
                        "Yearly",
                    ],
                ),
                "\n",
            )
        print(40 * "*")

    # welcome message , description of the app


print(
    "\n\t\t\t********************************************************\n"
    "\n\t\t\tWelcome to Malta Tax Calculator. This app will calculate\n"
    "\t\t\tyour salary with income tax according to your input.\n"
    "\n\t\t\t**********************Disclaimer************************\n"
    "\t\t\tPlease note that the result may vary with your actual\n"
    "\t\t\tsalary due to other deductions i.e. national insurance,\n"
    "\t\t\tand/or other benefits i.e. allowances and bonuses.\n"
    "\n\t\t\t********************************************************\n"
)
# clear the selected cell ranges to empty historical
#  data from any previous app use if any
salaries.batch_clear(
    [
        "A2:A1007",
        "B2:B1007",
        "C2:C1007",
        "D2:D1007",
        "E2:E1007",
        "F2:F1007",
        "G2:G1007",
        "H2:H1007",
        "I2:I1007",
        "J2:I1007",
        "K2:I1007",
        "L2:L1007",
        "M2:M1007",
    ]
)


def ask_name():
    global user_name
    user_name = str(input("Enter name: ")).capitalize()
    # input validation
    if not validate_name(user_name):
        print(
            "\n\t\t\tInvalid input!\n"
            "\n\t\t\tPlease try again by entering name.\n"
            "\n\t\t\tDo not include special characters or digits.\n"
        )
        ask_name()


def studies_status():
    # ask the user for the student status
    is_student = str(input("Are you a Student ? (Y/N): ")).upper()
    # input validation
    if not is_valid_input(is_student, "YN"):
        print(
            "\n\t\t\tInvalid input!\n"
            "\n\t\t\tPlease try again..\n"
            "\n\t\t\tIf you are a student - Type Y"
            "\n\t\t\tOtherwise - Type N"
        )
        studies_status()


def ask_age():
    global is_over_18_years
    # ask the user for the age over 18
    is_over_18_years = str(input("Are you over 18 ? (Y/N): ")).upper()
    # input validation
    if not is_valid_input(is_over_18_years, "YN"):
        print(
            "\n\t\t\tInvalid input!\n"
            "\n\t\t\tPlease try again..\n"
            "\n\t\t\tIf you are over 18 years of age - Type Y"
            "\n\t\t\tOtherwise - Type N"
        )
        ask_age()


def ask_born_year():
    # if the under 18, skip to ask for before 1962 option
    if is_over_18_years == "Y":
        # ask the user for the born before 1962
        is_born_before_1962 = str(input("Born before 1962 ? (Y/N): ")).upper()
        if not is_valid_input(is_born_before_1962, "YN"):
            print(
                "\n\t\t\tInvalid input!\n"
                "\n\t\t\tPlease try again..\n"
                "\n\t\t\tIf you were born before 1962 - Type Y"
                "\n\t\t\tOtherwise - Type N"
            )
            ask_born_year()


def check_civil_status():
    global civil_status
    # ask the user for the civil status
    civil_status = str(input("Single, Married or Parent ? (S/M/P): ")).upper()
    # input validation
    if not is_valid_input(civil_status, "SMP"):
        print(
            "\n\t\t\tInvalid input!\n"
            "\n\t\t\tPlease try again..\n"
            "\n\t\t\tIf your status is Single - Type S"
            "\n\t\t\tIf your status is Married - Type M"
            "\n\t\t\tIf your status is Parent - Type P"
        )
        check_civil_status()
    return civil_status


def ask_income():
    global income
    # ask the user for the income
    try:
        income = float(input("Enter your income ? (Input amount): "))
    # input validation
    except ValueError:
        print(
            "\n\t\t\tInvalid input!\n"
            "\n\t\t\tPlease try again by entering your income..\n"
            "\n\t\t\tInclude only income amount in digits\n"
        )
        ask_income()


# print("Check 1")
def check_income_type():
    if isinstance(income, float) or isinstance(income, int):

        # income value validation
        if income <= 0:
            print("Income should be greater than 0. Please try again.")
    return


# print("Check 2")
def calculations():
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

        # calculate the gross income for the user
        instance.calculate_gross_income()

        # print the results
        instance.display_data(user_name)

        # store in google sheet
        instance.store_data_in_google_sheet()

        # show the results in a table from google sheet
        instance.display_google_sheet_data()


def ask_continue():
    continue_input = str(
        input("Would you like to calculate another salary?(Y/N):")
    ).upper()
    if continue_input == "N":
        # terminate the program - thank you message
        print(
            "\n\t\t\t*************************************************\n"
            "\n\t\t\t****Thank you for using Malta Tax Calculator!****\n"
            "\n\t\t\t*************************************************\n"
            "\n\t\t\t*************************************************\n"
        )
        # clear the selected cell ranges to empty historical data
        salaries.batch_clear(
            [
                "A2:A1007",
                "B2:B1007",
                "C2:C1007",
                "D2:D1007",
                "E2:E1007",
                "F2:F1007",
                "G2:G1007",
                "H2:H1007",
                "I2:I1007",
                "J2:I1007",
                "K2:I1007",
                "L2:L1007",
                "M2:M1007",
            ]
        )
        return
    elif continue_input == "Y":
        print("\n\n\n\n")
        main()
    # income value validation
    else:
        print(
            "\n\t\t\tInvalid input!\n"
            "\n\t\t\tPlease try again..\n"
            "\n\t\t\tIf you would like to calculate another salary - Type Y"
            "\n\t\t\tOtherwise - Type N to exit"
        )
        ask_continue()


# functions used in main
def main():
    ask_name()
    studies_status()
    ask_age()
    ask_born_year()
    check_civil_status()
    ask_income()
    check_income_type()
    calculations()
    ask_continue()


main()
