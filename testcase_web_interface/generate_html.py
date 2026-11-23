
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

            :root {{
                --background: #0b1120;
                --surface: #111827;
                --surface-secondary: #1f2937;
                --border: #374151;
                --text: #f3f4f6;
                --muted: #9ca3af;
                --accent: #293548;
                --green: #22c55e;
                --red: #ef4444;
            }}

            * {{
                box-sizing: border-box;
            }}

            body {{
                font-family: Arial, sans-serif;
                background-color: var(--background);
                color: var(--text);
                margin: 0;
                padding: 12px;
            }}

            .container {{
                width: 99%;
                margin: auto;
                background: var(--surface);
                padding: 20px;
                border: 1px solid var(--border);
                border-radius: 16px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.25);
            }}

            h1 {{
                text-align: center;
                color: var(--text);
                margin-top: 5px;
                margin-bottom: 25px;
            }}

            .packet-table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-bottom: 22px;
                table-layout: fixed;
                border-radius: 10px;
                overflow: hidden;
            }}

            .packet-table tr:first-child td:first-child {{
                border-top-left-radius: 10px;
            }}

            .packet-table tr:first-child td:last-child {{
                border-top-right-radius: 10px;
            }}

            .packet-table tr:last-child td:first-child {{
                border-bottom-left-radius: 10px;
            }}

            .packet-table tr:last-child td:last-child {{
                border-bottom-right-radius: 10px;
            }}

            .packet-table td {{
                border: 1px solid var(--border);
                padding: 7px 12px;
                vertical-align: middle;
                color: var(--text);
            }}

            .packet-heading td {{
                background-color: var(--accent);
                color: var(--text);
                font-weight: bold;
                font-size: 15px;
                padding: 9px 12px;
            }}

            <!--tbody {{
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}-->

            .field-name {{
                width: 35%;
                font-weight: 500;
                background-color: var(--surface-secondary);
            }}

            .field-input {{
                width: 65%;
                background-color: var(--surface);
            }}

            .field-input input {{
                width: 100%;
                padding: 7px 9px;
                background-color: var(--surface-secondary);
                color: var(--text);
                border: 1px solid var(--border);
                border-radius: 4px;
                font-size: 14px;
            }}

            .field-input input::placeholder {{
                color: var(--muted);
            }}

            .field-input input:focus {{
                outline: none;
                border-color: #64748b;
                box-shadow: 0 0 0 2px rgba(100,116,139,0.2);
            }}

            button {{
                display: block;
                width: 100%;
                margin-bottom: 25px;
                padding: 12px;
                background-color: var(--accent);
                color: var(--text);
                border: 1px solid var(--border);
                border-radius: 15px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.2s ease;
            }}

            button:hover {{
                background-color: #37465d;
            }}

            button:disabled {{
                background-color: #374151;
                color: var(--muted);
                cursor: not-allowed;
            }}

            #status {{
                text-align: center;
                margin-bottom: 12px;
                font-weight: bold;
                color: var(--text);
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>Packet Testcase Configuration</h1>
            
            <form id="testcase-form">

                <button type="submit" id="run-button" autofocus>
                    Run Testcase
                </button>

                <div id="status"></div>

                {packet_tables}

                

            </form>

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

                    status.textContent = "Testcases saved successfully! You can close the tab now if it doesn't close automatically...";
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
