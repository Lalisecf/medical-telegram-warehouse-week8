from api.schemas import Channel

channel = Channel(
    channel_key=1,
    channel_name="CheMed"
)

print(channel.model_dump())