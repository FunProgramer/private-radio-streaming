# Private Radio Station
This project is work in progress.

The aim of this project is to create a "website" on which
you can upload audio files in order to stream these audios
via the local network, e.g. to serve Internet radios.

You upload the audio files as "sources" and stream them through "channels".
To stream an audio you create a channel. To create a channel you need to 
specify a source to stream and an endpoint (stream_path) where the audio
stream will be served.

As soon as a device connects the stream will start. We will remember the position
in the audio file, while streaming the audio. If there is no listener left,
we stop streaming the audio. If a listener is connecting again we start from
the position in the audio file where we left of the streaming.

Later this project should also get the ability to download audio from telegram
to stream also that audio.
