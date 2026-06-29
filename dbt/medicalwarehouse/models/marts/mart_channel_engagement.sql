SELECT

    channel_name,

    message_id,

    message_date,

    views,

    forwards,

    message_length,

    has_image,

    CASE
        WHEN views = 0 THEN 0
        ELSE ROUND((forwards::NUMERIC / views) * 100, 2)
    END AS engagement_rate

FROM {{ ref('stg_telegram_messages') }}