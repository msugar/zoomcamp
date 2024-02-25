{% macro safe_cast_to_int(column_name) %}
    SAFE_CAST(SAFE_CAST({{ column_name }} AS FLOAT64) AS INT64) -- api.Column.translate_type("integer")
{% endmacro %}
