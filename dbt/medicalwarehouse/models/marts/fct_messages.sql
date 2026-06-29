SELECT

    message_id,

    channel_name,

    CAST(message_date AS DATE) AS message_date,

    message_text,

    message_length,

    views,

    forwards,

    has_media,

    has_image,

    image_path

FROM {{ ref('stg_telegram_messages') }}