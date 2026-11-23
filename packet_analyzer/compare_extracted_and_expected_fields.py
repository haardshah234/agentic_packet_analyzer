def compare_extracted_and_expected_fields(
    extracted_fields,
    expected_fields
):
    results = {}

    for packet_name, extractions in extracted_fields.items():

        expected = expected_fields.get(packet_name, {})
        results[packet_name] = []

        for extraction in extractions:

            passed = (
                bool(expected)
                and all(
                    field_name in extraction
                    and extraction[field_name] == expected_value
                    for field_name, expected_value in expected.items()
                )
            )

            results[packet_name].append(passed)

    return results