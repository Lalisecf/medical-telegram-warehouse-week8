{{ config(
    materialized='table'
) }}

WITH detections AS (

    SELECT *
    FROM {{ ref('stg_image_detections') }}

),

messages AS (

    SELECT *
    FROM {{ ref('fct_messages') }}

)

SELECT

    d.message_id,

    m.channel_name,

    m.message_date,

    m.message_text,

    m.views,

    m.forwards,

    d.detected_class,

    d.confidence_score,

    d.image_category

FROM detections d

INNER JOIN messages m
    ON d.message_id = m.message_id