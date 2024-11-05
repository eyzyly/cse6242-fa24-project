{% macro convert_byte_string_to_wkt(byte_string) %}
    -- Convert the input to bytes and then to hex format
    {{ "TO_HEX(CAST(" ~ byte_string ~ " AS BYTES))" }}
{% endmacro %}
