import argparse
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from anthropic import Anthropic

client = Anthropic()

def summarize_video(url: str, model: str):
    video_id = parse_qs(urlparse(url).query).get('v')[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=("en", ))
    # for i in range(0, len(transcript), 5000):
    # context = "\n".join([t["text"] for t in transcript[i:i+5000]])
    context = "\n".join([t["text"] for t in transcript])
    prompt = f"Summarize this youtube video section's transcript with bullet points:\n---\n{context}"
    summary = client.messages.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=4096).content[0].text
    print(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize YouTube video transcripts.")
    parser.add_argument("url", help="URL of the YouTube video to summarize.")
    parser.add_argument("model", help="Model name", default="claude-3-haiku-20240307", nargs="?")
    args = parser.parse_args()

    summarize_video(args.url, args.model)
