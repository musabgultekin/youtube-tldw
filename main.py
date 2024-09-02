import argparse
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

client = OpenAI()

def summarize_video(url: str, model: str, language: str):
    video_id = parse_qs(urlparse(url).query).get('v')[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=(language, ))
    context = "\n".join([t["text"] for t in transcript])
    prompt = f"Summarize this youtube video transcript's important parts with bullet points:\n---\n{context}"
    response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=4096)
    summary = response.choices[0].message.content
    print("Usage:", response.usage.model_dump())
    print(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize YouTube video transcripts.")
    parser.add_argument("url", help="URL of the YouTube video to summarize.")
    parser.add_argument("model", help="Model name", default="gpt-4o-mini", nargs="?")
    parser.add_argument("language", help="Language of the video", default="en", nargs="?")
    args = parser.parse_args()

    summarize_video(args.url, args.model, args.language)
