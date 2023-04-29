import sys
import argparse
from urllib.parse import parse_qs, urlparse

import openai
from youtube_transcript_api import YouTubeTranscriptApi

def summarize_video(url):
    transcript = YouTubeTranscriptApi.get_transcript(parse_qs(urlparse(url).query).get('v')[0])

    for i in range(0, len(transcript), 1000):
        context = "\n".join([t["text"] for t in transcript[i:i+1000]])
        prompt = f"Summarize this youtube video section:\n---\n{context}" # @param {type: "string"}
        summary = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]).choices[0].message["content"]
        print(summary)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize YouTube video transcripts.")
    parser.add_argument("url", help="URL of the YouTube video to summarize.")
    args = parser.parse_args()

    summarize_video(args.url)
