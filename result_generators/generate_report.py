
import html
import webbrowser
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
output_folder = project_root / "reports"


def _escape(value):
    if value is None:
        return "—"
    return html.escape(str(value))


def _generate_field_table(packet_name, expected_fields, extracted_fields, definition):
    rows = []

    passed = 0
    failed = 0

    for field in definition.get("fields", []):
        field_name = field["field_name"]

        expected = expected_fields.get(packet_name, {}).get(field_name)
        observed = extracted_fields.get(packet_name, {}).get(field_name)

        # A missing expected or observed field is considered a failure.
        status = (
            expected == observed
            and field_name in expected_fields.get(packet_name, {})
            and field_name in extracted_fields.get(packet_name, {})
        )

        if status:
            passed += 1
            status_class = "pass"
            status_text = "PASS"
        else:
            failed += 1
            status_class = "fail"
            status_text = "FAIL"

        rows.append(f"""
            <tr>
                <td>{_escape(field_name)}</td>
                <td>{_escape(expected)}</td>
                <td>{_escape(observed)}</td>
                <td class="{status_class}">{status_text}</td>
            </tr>
        """)

    table = f"""
        <table class="report-table">
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Expected</th>
                    <th>Observed</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
    """

    return table, passed, failed


def _generate_frame_metadata(frames):
    if not frames:
        return ""

    labels = {
        "frame.time": "Frame Time",
        "frame.number": "Frame Number",
        "ip.src": "Source IP",
        "ip.dst": "Destination IP",
        "tcp.srcport": "Source Port",
        "tcp.dstport": "Destination Port",
        "tcp.len": "TCP Length"
    }

    frame_sections = []

    for frame in frames:
        frame_number = frame.get("frame.number", "Unknown")

        rows = []

        for key, value in frame.items():
            label = labels.get(key, key)

            rows.append(f"""
                <tr>
                    <td>{_escape(label)}</td>
                    <td>{_escape(value)}</td>
                </tr>
            """)

        frame_sections.append(f"""
            <div class="frame-observation">
                <h4>Frame #{_escape(frame_number)}</h4>

                <table class="metadata-table">
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        """)

    return f"""
        <div class="frame-metadata">
            <h3>Frame Observation Details</h3>

            <p class="section-description">
                Wireshark metadata for the frames in which this
                packet was observed.
            </p>

            {"".join(frame_sections)}
        </div>
    """


def generate_report(expected_fields, extracted_fields, packet_definitions, metadata, launch=True):

    # ---------------------------------------------------------
    # 1. Generate individual packet sections
    # ---------------------------------------------------------

    packet_sections = []

    total_packets = 0
    passed_packets = 0
    failed_packets = 0

    for index, definition in enumerate(packet_definitions, start=1):

        packet_name = definition["name"]

        total_packets += 1

        # Generate field comparison table
        field_table, passed_fields, failed_fields = _generate_field_table(
            packet_name,
            expected_fields,
            extracted_fields,
            definition
        )

        total_fields = passed_fields + failed_fields

        passed_percentage = (
            (passed_fields / total_fields) * 100
            if total_fields else 0
        )

        failed_percentage = 100 - passed_percentage

        packet_status = "PASS" if failed_fields == 0 else "FAIL"
        status_class = packet_status.lower()

        if packet_status == "PASS":
            passed_packets += 1
        else:
            failed_packets += 1

        # Fetch frame metadata for this packet
        frames = metadata.get(packet_name, [])

        frame_metadata = _generate_frame_metadata(frames)

        # Additional packet definition information
        reference_section = definition.get("reference_section")
        total_size = definition.get("total_size_in_bytes")

        assumptions = definition.get("assumptions", [])

        assumptions_html = ""

        if assumptions:
            assumptions_html = f"""
                <div class="assumptions">
                    <h4>Assumptions</h4>
                    <ul>
                        {"".join(
                            f"<li>{_escape(item)}</li>"
                            for item in assumptions
                        )}
                    </ul>
                </div>
            """

        packet_sections.append(f"""
            <section class="packet-section" id="packet-{index}">

                <div class="packet-header">

                    <div>
                        <h2>{_escape(packet_name)}</h2>

                        <p class="packet-subtitle">
                            Reference Section: {_escape(reference_section)}
                            &nbsp; | &nbsp;
                            Packet Size: {_escape(total_size)} bytes
                        </p>
                    </div>

                    <span class="status-badge {status_class}">
                        {packet_status}
                    </span>

                </div>

                <div class="packet-summary">

                    <div class="metric">
                        <span class="metric-label">Total Fields</span>
                        <span class="metric-value">{total_fields}</span>
                    </div>

                    <div class="metric">
                        <span class="metric-label">Passed Fields</span>
                        <span class="metric-value pass">{passed_fields}</span>
                    </div>

                    <div class="metric">
                        <span class="metric-label">Failed Fields</span>
                        <span class="metric-value fail">{failed_fields}</span>
                    </div>

                </div>

                <div class="progress-container">
                    <div
                        class="progress-passed"
                        style="width: {passed_percentage:.2f}%"
                    ></div>

                    <div
                        class="progress-failed"
                        style="width: {failed_percentage:.2f}%"
                    ></div>
                </div>

                <div class="progress-label">
                    <span>
                        Passed: {passed_percentage:.1f}%
                        ({passed_fields}/{total_fields})
                    </span>

                    <span>
                        Failed: {failed_percentage:.1f}%
                        ({failed_fields}/{total_fields})
                    </span>
                </div>

                <h3>Field Validation</h3>

                {field_table}

                {assumptions_html}

                {frame_metadata}

            </section>
        """)


    overall_pass_percentage = (
        (passed_packets / total_packets) * 100
        if total_packets else 0
    )

    overall_fail_percentage = 100 - overall_pass_percentage
    # ---------------------------------------------------------
    # 2. Generate report timestamp
    # ---------------------------------------------------------

    report_generated_on = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    # ---------------------------------------------------------
    # 3. Generate complete HTML
    # ---------------------------------------------------------

    report_html = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Packet Validation Report</title>

        <style>

            :root {{
                --background: #0b1120;
                --surface: #111827;
                --surface-secondary: #1f2937;
                --border: #374151;
                --text: #f3f4f6;
                --muted: #9ca3af;
                --green: #22c55e;
                --red: #ef4444;
            }}

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 30px;
                background: var(--background);
                color: var(--text);
                font-family: Arial, Helvetica, sans-serif;
                line-height: 1.6;
            }}

            .report-container {{
                width: 100%;
                max-width: 1500px;
                margin: auto;
            }}

            .report-header {{
                background: linear-gradient(135deg, #111827, #1e293b);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 30px;
                margin-bottom: 25px;
            }}

            .report-header h1 {{
                margin: 0;
                font-size: 30px;
            }}

            .subtitle {{
                color: var(--muted);
                margin-top: 5px;
            }}

            .report-info {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 15px;
                margin-top: 25px;
            }}

            .info-item {{
                background: var(--surface-secondary);
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 15px;
            }}

            .info-label {{
                display: block;
                color: var(--muted);
                font-size: 13px;
            }}

            .info-value {{
                font-weight: bold;
            }}

            .summary-section,
            .packet-section {{
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 25px;
                margin-bottom: 25px;
            }}

            .summary-grid,
            .packet-summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }}

            .summary-card,
            .metric {{
                background: var(--surface-secondary);
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 18px;
            }}

            .metric-label {{
                color: var(--muted);
                font-size: 14px;
            }}

            .metric-value {{
                display: block;
                font-size: 28px;
                font-weight: bold;
                margin-top: 5px;
            }}

            .pass {{
                color: var(--green);
            }}

            .fail {{
                color: var(--red);
            }}

            .packet-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 15px;
            }}

            .packet-header h2 {{
                margin: 0;
                overflow-wrap: anywhere;
            }}

            .packet-subtitle,
            .section-description {{
                color: var(--muted);
                font-size: 14px;
            }}

            .status-badge {{
                padding: 7px 16px;
                border-radius: 8px;
                font-weight: bold;
            }}

            .status-badge.pass {{
                background: #163323;
                color: #86efac;
            }}

            .status-badge.fail {{
                background: #3b1d26;
                color: #fca5a5;
            }}

            h3 {{
                margin-top: 25px;
            }}

            .report-table,
            .metadata-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                table-layout: auto;
            }}

            .report-table th,
            .report-table td,
            .metadata-table td {{
                border: 1px solid var(--border);
                padding: 12px;
                text-align: left;
                overflow-wrap: anywhere;
            }}

            .report-table th {{
                background: #293548;
                color: #f3f4f6;
            }}

            .report-table tbody tr:nth-child(odd),
            .metadata-table tr:nth-child(odd) {{
                background: #18212e;
            }}

            .report-table tbody tr:nth-child(even),
            .metadata-table tr:nth-child(even) {{
                background: #111827;
            }}

            .report-table td.pass,
            .report-table td.fail {{
                font-weight: bold;
            }}

            .frame-metadata {{
                border-top: 1px solid var(--border);
                margin-top: 30px;
                padding-top: 20px;
            }}

            .frame-observation {{
                margin-bottom: 25px;
            }}

            .frame-observation h4 {{
                background: #293548;
                border: 1px solid var(--border);
                border-radius: 8px 8px 0 0;
                padding: 10px 15px;
                margin: 0;
            }}

            .metadata-table {{
                margin-bottom: 0;
            }}

            .metadata-table td:first-child {{
                width: 30%;
                color: var(--muted);
                font-weight: bold;
            }}

            .assumptions {{
                background: var(--surface-secondary);
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 12px 20px;
                margin-top: 20px;
            }}

            .assumptions h4 {{
                margin: 0;
            }}

            .report-footer {{
                text-align: center;
                border-top: 1px solid var(--border);
                padding: 25px 10px;
                margin-top: 40px;
                color: var(--muted);
                font-size: 14px;
            }}

            /* Progress bars */

            .progress-container {{
                width: 100%;
                height: 12px;
                background: #374151;
                border-radius: 20px;
                overflow: hidden;
                display: flex;
                margin-top: 15px;
            }}

            .progress-passed {{
                height: 100%;
                background: #22c55e;
                transition: width 0.3s ease;
            }}

            .progress-failed {{
                height: 100%;
                background: #ef4444;
                transition: width 0.3s ease;
            }}

            .progress-label {{
                display: flex;
                justify-content: space-between;
                gap: 10px;
                margin-top: 8px;
                font-size: 13px;
                color: #9ca3af;
            }}

            /* Print styling */

            @media print {{
                .progress-container {{
                    background: #e5e7eb !important;
                    border: 1px solid #cbd5e1 !important;
                }}

                .progress-passed {{
                    background: #22c55e !important;
                }}

                .progress-failed {{
                    background: #ef4444 !important;
                }}

                .progress-label {{
                    color: #475569 !important;
                }}
            }}

            @media screen and (max-width: 700px) {{
                body {{
                    padding: 12px;
                }}

                .summary-section,
                .packet-section,
                .report-header {{
                    padding: 18px;
                }}

                .report-table th,
                .report-table td,
                .metadata-table td {{
                    padding: 8px;
                    font-size: 13px;
                }}
            }}

            @media print {{

                * {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}

                body {{
                    background: white !important;
                    color: #111827 !important;
                    padding: 0 !important;
                }}

                .report-header,
                .summary-section,
                .packet-section {{
                    background: white !important;
                    color: #111827 !important;
                    border: 1px solid #cbd5e1 !important;
                    border-radius: 0 !important;
                }}

                .report-header h1,
                .packet-section h2,
                .packet-section h3,
                .packet-section h4,
                .summary-section h2 {{
                    color: #111827 !important;
                }}

                .subtitle,
                .packet-subtitle,
                .section-description,
                .info-label,
                .metric-label,
                .report-footer {{
                    color: #475569 !important;
                }}

                .info-item,
                .summary-card,
                .metric,
                .assumptions,
                .frame-observation h4 {{
                    background: #f1f3f8 !important;
                    color: #111827 !important;
                    border-color: #cbd5e1 !important;
                }}

                .report-table tr:nth-child(odd) th,
                .report-table tr:nth-child(odd) td {{
                    background: #f1f3f8 !important;
                }}

                .report-table tr:nth-child(even) th,
                .report-table tr:nth-child(even) td {{
                    background: #fafbfc !important;
                }}

                .report-table th {{
                    color: #111827 !important;
                }}

                .report-table .pass,
                .pass {{
                    color: #16803c !important;
                }}

                .report-table .fail,
                .fail {{
                    color: #c62828 !important;
                }}

                .status-badge.pass {{
                    background: #e2f3e8 !important;
                    color: #16803c !important;
                }}

                .status-badge.fail {{
                    background: #fde8e8 !important;
                    color: #c62828 !important;
                }}

                .metadata-table tr:nth-child(odd) td {{
                    background: #f1f3f8 !important;
                }}

                .metadata-table tr:nth-child(even) td {{
                    background: #fafbfc !important;
                }}

                .metadata-table td {{
                    color: #111827 !important;
                }}

                .metadata-table td:first-child {{
                    color: #475569 !important;
                }}

                .packet-section,
                .frame-observation {{
                    break-inside: avoid;
                    page-break-inside: avoid;
                }}

                .report-footer {{
                    border-top: 1px solid #cbd5e1 !important;
                }}
            }}

        </style>
    </head>

    <body>

        <div class="report-container">

            <header class="report-header">

                <h1>Packet Validation Report</h1>

                <div class="subtitle">
                    Interface Testing &middot; Packet Analyzer
                </div>

                <div class="report-info">

                    <div class="info-item">
                        <span class="info-label">Report Generated On</span>
                        <span class="info-value">
                            {_escape(report_generated_on)}
                        </span>
                    </div>

                    <div class="info-item">
                        <span class="info-label">Total Packet Definitions</span>
                        <span class="info-value">{total_packets}</span>
                    </div>

                </div>

            </header>

            <section class="summary-section">

                <h2>Execution Summary</h2>

                <div class="summary-grid">

                    <div class="summary-card">
                        <span class="metric-label">Total Packets</span>
                        <span class="metric-value">{total_packets}</span>
                    </div>

                    <div class="summary-card">
                        <span class="metric-label">Passed Packets</span>
                        <span class="metric-value pass">{passed_packets}</span>
                    </div>

                    <div class="summary-card">
                        <span class="metric-label">Failed Packets</span>
                        <span class="metric-value fail">{failed_packets}</span>
                    </div>

                </div>

                <div class="progress-container">
                    <div
                        class="progress-passed"
                        style="width: {overall_pass_percentage:.2f}%"
                    ></div>

                    <div
                        class="progress-failed"
                        style="width: {overall_fail_percentage:.2f}%"
                    ></div>
                </div>

                <div class="progress-label">
                    <span>
                        Passed: {overall_pass_percentage:.1f}%
                        ({passed_packets}/{total_packets})
                    </span>

                    <span>
                        Failed: {overall_fail_percentage:.1f}%
                        ({failed_packets}/{total_packets})
                    </span>
                </div>

            </section>

            {"".join(packet_sections)}

            <footer class="report-footer">

                Automatically generated report &mdash;

                Developed by: Haard Shah &mdash;

                Under the Guidance of: K. Somashekar

            </footer>

        </div>

    </body>
    </html>
    """

    # ---------------------------------------------------------
    # 4. Save and launch report
    # ---------------------------------------------------------


    final_output_folder = output_folder / (report_generated_on.replace("-","_").replace(" ","_").replace(":","_"))
    final_output_folder.mkdir(parents=True, exist_ok=True)

    output_file = final_output_folder / "report.html"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(report_html)

    print(f"\nHTML report generated successfully: {output_file}")

    if launch:
        
        webbrowser.open(output_file.as_uri())

    return output_file
