from flask import Flask, jsonify, request, send_from_directory, send_file, render_template
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from flask_cors import CORS, cross_origin  # ✅ Added cross_origin import
import re  # ✅ For prefix stripping

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Explicitly allow all routes

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")  # Folder for uploads
RDL_FOLDER = os.path.join(BASE_DIR, "rdl_files")  # Folder for .rdl files
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RDL_FOLDER"] = RDL_FOLDER
file_path = os.path.join(BASE_DIR, "rdlfiles.xlsx")  # Path to original Excel file

ALLOWED_EXTENSIONS = {"xls", "xlsx"}

# Create necessary folders if they don’t exist
for folder in [UPLOAD_FOLDER, RDL_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_excel_file():
    """Load rdlfiles.xlsx into a pandas DataFrame."""
    if os.path.exists(file_path):
        print(f"📂 Loading file: {file_path}")
        df = pd.read_excel(file_path, engine="openpyxl")

        # Strip strings in each column
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

        return df
    print(f"⚠️ File not found: {file_path}, creating empty DataFrame")
    return pd.DataFrame()


df = load_excel_file()  # Initial load


def copy_column_widths(source_wb, target_wb):
    """Copy column widths from source workbook to target workbook."""
    source_ws = source_wb.active
    target_ws = target_wb.active

    for col in source_ws.columns:
        column_letter = get_column_letter(col[0].column)
        if column_letter in source_ws.column_dimensions:
            target_ws.column_dimensions[column_letter].width = source_ws.column_dimensions[column_letter].width


@app.route("/")
def home():
    return render_template("index.html")  # Load your HTML


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and merge into rdlfiles.xlsx while preserving column widths."""
    global df  # 🔥 Ensure df updates

    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only .xlsx files are allowed"}), 400

        file_path_uploaded = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path_uploaded)
        print(f"📂 File saved to: {file_path_uploaded}")

        try:
            new_wb = load_workbook(file_path_uploaded)
            new_ws = new_wb.active
        except Exception as e:
            os.remove(file_path_uploaded)  # Delete corrupted file
            return jsonify({"error": f"Failed to process file: {str(e)}"}), 400

        # Load existing Excel file
        if os.path.exists(file_path):
            existing_wb = load_workbook(file_path)
            existing_ws = existing_wb.active
        else:
            existing_wb = load_workbook(file_path_uploaded)
            existing_ws = existing_wb.active

        # Append data from new file to existing file
        for row in new_ws.iter_rows(values_only=True):
            existing_ws.append(row)

        # ✅ Preserve Column Widths
        copy_column_widths(new_wb, existing_wb)

        existing_wb.save(file_path)  # Save with original column widths
        new_wb.close()
        existing_wb.close()

        print("✅ Upload and merge successful!")

        # 🔥 **Reload the DataFrame after updating the Excel file**
        df = load_excel_file()
        print("🔄 DataFrame reloaded after upload!")

        return jsonify({"message": "File uploaded and merged successfully!"}), 200

    except Exception as e:
        print("❌ ERROR in upload:", str(e))
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500


@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    """Serve the corresponding .RDL file for the given filename."""
    try:
        # ✅ Dynamically strip "XX - " or similar prefixes
        filename = re.sub(r"^\d+\s*-\s*", "", filename)

        # Ensure filename has .rdl extension
        if not filename.lower().endswith(".rdl"):
            filename += ".rdl"

        # Full path check
        file_path = os.path.join(RDL_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(RDL_FOLDER, filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Failed to download the file: {str(e)}"}), 500


@app.route("/download-excel", methods=["GET"])
def download_excel():
    """Serve the Excel file for direct download."""
    try:
        if not os.path.exists(file_path):
            return jsonify({"error": "Excel file not found"}), 404

        return send_file(file_path, as_attachment=True, download_name="rdlfiles.xlsx")

    except Exception as e:
        return jsonify({"error": f"Failed to download the file: {str(e)}"}), 500


@app.route("/search", methods=["GET"])
@cross_origin()  # ✅ Explicitly allow CORS for this route
def search():
    """Search for matching rows in the dataframe."""
    global df  # 🔥 Ensure we use the latest df

    try:
        query = request.args.get("query", "").strip().lower()
        if not query:
            return jsonify({"results": []})

        # Search for matching rows in the dataframe
        results = df[
            df.astype(str).apply(lambda row: row.str.contains(query, case=False, na=False).any(), axis=1)
        ]

        # Convert the results to a valid JSON object and remove any NaN values by replacing them with None
        results_clean = results.where(pd.notnull(results), None)

        return jsonify({"results": results_clean.to_dict(orient="records")})

    except Exception as e:
        print(f"❌ Error in search route: {e}")  # Log the error
        return jsonify({"error": f"An error occurred while processing your request: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
