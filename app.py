from flask import Flask, render_template, request, send_file
from validators.phone_validator import validate_phone
from validators.date_validator import validate_date
from validators.payment_validator import validate_payment
from utils.csv_splitter import split_csv
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    # Read CSV
    df = pd.read_csv(file)

    # Split Large CSV
    split_csv(df)

    # Remove Duplicates
    clean_df = df.drop_duplicates()

    clean_df.to_csv(
        "outputs/clean_data.csv",
        index=False
    )

    errors = []
    invalid_rows = set()

    valid_rows = []
    invalid_rows_data = []

    # Validation Loop
    for index, row in df.iterrows():

        row_errors = []

        # Phone Validation
        if not validate_phone(
            row["phone"],
            row["country_code"]
        ):
            errors.append(
                f"Row {index + 1}: Invalid Phone Number"
            )

            row_errors.append(
                "Invalid Phone Number"
            )

            invalid_rows.add(index)

        # Date Validation
        if not validate_date(
            str(row["date"])
        ):
            errors.append(
                f"Row {index + 1}: Invalid Date"
            )

            row_errors.append(
                "Invalid Date"
            )

            invalid_rows.add(index)

        # Payment Validation
        if not validate_payment(
            row["payment_mode"]
        ):
            errors.append(
                f"Row {index + 1}: Invalid Payment Mode"
            )

            row_errors.append(
                "Invalid Payment Mode"
            )

            invalid_rows.add(index)

        # Store Valid / Invalid Records
        if len(row_errors) == 0:
            valid_rows.append(row)

        else:
            row_copy = row.copy()
            row_copy["Errors"] = ", ".join(row_errors)

            invalid_rows_data.append(row_copy)

    # Save Valid Records
    pd.DataFrame(valid_rows).to_csv(
        "outputs/valid_records.csv",
        index=False
    )

    # Save Invalid Records
    pd.DataFrame(invalid_rows_data).to_csv(
        "outputs/invalid_records.csv",
        index=False
    )

    # Save Error Report
    error_df = pd.DataFrame({
        "Errors": errors
    })

    error_df.to_csv(
        "reports/error_report.csv",
        index=False
    )

    # Dashboard Stats
    total_records = len(df)
    invalid_records = len(invalid_rows)
    valid_records = total_records - invalid_records

    return render_template(
        "result.html",
        total=total_records,
        valid=valid_records,
        invalid=invalid_records,
        errors=errors
    )


@app.route('/download-clean')
def download_clean():
    return send_file(
        "outputs/clean_data.csv",
        as_attachment=True
    )


@app.route('/download-error')
def download_error():
    return send_file(
        "reports/error_report.csv",
        as_attachment=True
    )


@app.route('/download-valid')
def download_valid():
    return send_file(
        "outputs/valid_records.csv",
        as_attachment=True
    )


@app.route('/download-invalid')
def download_invalid():
    return send_file(
        "outputs/invalid_records.csv",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)