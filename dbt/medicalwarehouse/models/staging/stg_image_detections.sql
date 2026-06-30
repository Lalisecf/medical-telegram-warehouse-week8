{{ config(materialized='view') }}

WITH source_data AS (

    SELECT *

    FROM {{ source('raw', 'image_detections') }}

),

cleaned AS (

    SELECT

        CAST(message_id AS BIGINT)             AS message_id,

        TRIM(channel_name)                     AS channel_name,

        LOWER(TRIM(detected_class))            AS detected_class,

        CAST(confidence_score AS NUMERIC(5,3)) AS confidence_score,

        LOWER(TRIM(image_category))            AS image_category

    FROM source_data

)

SELECT *

FROM cleaned

WHERE message_id IS NOT NULL