SELECT

    channel_name,

    COUNT(*) AS total_messages,

    SUM(
        CASE
            WHEN has_image THEN 1
            ELSE 0
        END
    ) AS total_images,

    AVG(views) AS average_views,

    AVG(forwards) AS average_forwards,

    MAX(message_date) AS latest_message_date

FROM {{ ref('stg_telegram_messages') }}

GROUP BY channel_name