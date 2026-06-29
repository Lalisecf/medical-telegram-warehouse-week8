SELECT

    message_id,

    channel_name,

    CAST(message_date AS TIMESTAMP) AS message_date,

    COALESCE(message_text, '') AS message_text,

    CAST(COALESCE(views, 0) AS INTEGER) AS views,

    CAST(COALESCE(forwards, 0) AS INTEGER) AS forwards,

    image_path,

    has_media,

    LENGTH(COALESCE(message_text, '')) AS message_length,

    CASE
        WHEN image_path IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS has_image

FROM raw.telegram_messages