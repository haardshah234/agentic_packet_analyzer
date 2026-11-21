
from html import escape
import json
from pathlib import Path

testcases_relative_filepath = "jsons/testcases.json"
project_root = Path(__file__).parent.parent
testcases_filepath = project_root / testcases_relative_filepath


def generate_html(packet_definitions: list[dict]) -> str:

    # Load previously saved testcases, if available.
    if testcases_filepath.exists():
        try:
            saved_testcases = json.loads(
                testcases_filepath.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            saved_testcases = {}
    else:
        saved_testcases = {}

    packet_tables = ""

    for packet_index, packet in enumerate(packet_definitions):

        packet_name = str(packet["name"])
        safe_packet_name = escape(packet_name)

        # Get previously saved values for this packet.
        saved_fields = saved_testcases.get(packet_name, {})

        table_rows = f"""
            <tr class="packet-heading">
                <td colspan="2">{safe_packet_name}</td>
            </tr>
        """

        for field_index, field in enumerate(packet.get("fields", [])):

            field_name = str(field["field_name"])

            # Priority:
            # 1. Previously saved testcase value.
            # 2. Packet definition's fixed value.
            # 3. Empty string.

            if field_name in saved_fields:
                initial_value = saved_fields[field_name]
            else:
                initial_value = field.get("fixed_value")

            if initial_value is None:
                initial_value = ""

            # Convert value to string for HTML input.
            initial_value = str(initial_value)

            table_rows += f"""
                <tr>
                    <td class="field-name">
                        {escape(field_name)}
                    </td>

                    <td class="field-input">
                        <input
                            type="text"
                            class="testcase-field"
                            data-field-name="{escape(field_name, quote=True)}"
                            value="{escape(initial_value, quote=True)}"
                        >
                    </td>
                </tr>
            """

        packet_tables += f"""
            <table class="packet-table"
                   data-packet-name="{escape(packet_name, quote=True)}">

                {table_rows}

            </table>
        """

    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Packet Testcase Configuration</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 12px;
            }}

            .container {{
                width: 99%;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}

            h1 {{
                text-align: center;
                color: #2d3194;
                margin-top: 5px;
                margin-bottom: 25px;
            }}

            .packet-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 22px;
                table-layout: fixed;
            }}

            .packet-table td {{
                border: 1px solid #d5d5d5;
                padding: 7px 12px;
                vertical-align: middle;
            }}

            .packet-heading td {{
                background-color: #2d3194;
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding: 9px 12px;
            }}

            tbody {{
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}

            .field-name {{
                width: 35%;
                font-weight: 500;
                background-color: #f8f9fc;
            }}

            .field-input {{
                width: 65%;
            }}

            .field-input input {{
                width: 100%;
                padding: 7px 9px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }}

            .field-input input:focus {{
                outline: none;
                border-color: #2d3194;
            }}

            button {{
                display: block;
                width: 100%;
                margin-bottom: 25px;
                padding: 12px;
                background-color: #2d3194;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                cursor: pointer;
            }}

            button:hover {{
                background-color: #202570;
            }}

            button:disabled {{
                background-color: #888;
                cursor: not-allowed;
            }}

            #status {{
                text-align: center;
                margin-top: 12px;
                font-weight: bold;
            }}

        </style>
    </head>

    <body>

        <div class="container">

            <h1>Packet Testcase Configuration</h1>

            <form id="testcase-form">

                <button type="submit" id="run-button">
                    Run Testcase
                </button>

                {packet_tables}

                

            </form>

            <div id="status"></div>

        </div>

        <script>

            const form = document.getElementById("testcase-form");
            const status = document.getElementById("status");
            const runButton = document.getElementById("run-button");

            form.addEventListener("submit", async function(event) {{

                event.preventDefault();

                const testcaseData = {{}};

                document.querySelectorAll(".packet-table").forEach(table => {{

                    const packetName = table.dataset.packetName;
                    const fields = {{}};

                    table.querySelectorAll(".testcase-field").forEach(input => {{

                        let value = input.value;

                        if (value.trim() !== "" && !isNaN(value)) {{
                            value = Number(value);
                        }}

                        fields[input.dataset.fieldName] = value;

                    }});

                    testcaseData[packetName] = fields;

                }});

                runButton.disabled = true;
                status.textContent = "Saving testcases...";

                try {{

                    const response = await fetch("/run", {{

                        method: "POST",

                        headers: {{
                            "Content-Type": "application/json"
                        }},

                        body: JSON.stringify(testcaseData)

                    }});

                    const result = await response.json();

                    if (!response.ok) {{
                        throw new Error(result.message);
                    }}

                    status.textContent = "Testcases saved successfully! Closing tab...";
                    window.close();

                }}
                catch(error) {{

                    status.textContent = "Error: " + error.message;

                }}
                finally {{

                    runButton.disabled = false;

                }}

            }});

        </script>

    </body>
    </html>
    """

    return html_page
