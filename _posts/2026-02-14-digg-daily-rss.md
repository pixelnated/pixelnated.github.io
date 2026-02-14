---
tags: Other
---

## Scratching an Itch: Digg Daily as a Podcast

I recently released a small project to solve a personal annoyance: I wanted to listen to Digg Daily's AI-generated news summaries on the go, but they're only available on the Digg website. So I built a solution.

### Introducing digg-daily-rss

[digg-daily-rss](https://github.com/pixelnated/digg-daily-rss) is a simple tool that wraps Digg Daily's audio episodes into a standard podcast RSS feed. This means you can subscribe to it in your podcast player of choice—Apple Podcasts, Pocket Casts, Overcast, AntennaPod, or whatever you prefer—and listen to the daily news digest during your commute, workout, or whenever.

**[Subscribe here](https://pixelnated.github.io/digg-daily-rss/)** or grab the direct feed URL:

```plaintext
https://pixelnated.github.io/digg-daily-rss/feed.xml
```

### How It Works

The feed is automatically updated daily via GitHub Actions:

1. Fetches episodes from Digg's official API
2. Constructs direct audio URLs from their CDN
3. Generates a podcast-compatible RSS feed
4. Publishes to GitHub Pages

There's also a Chrome extension included if you prefer quick one-click access from your browser.

### Built in 30 Minutes with Copilot

Here's the fun part: most of this project came together in about 30 minutes. I started with a clear plan of what I wanted—an RSS feed that podcast apps could understand, pointing to Digg's existing audio files—and used GitHub Copilot to help implement it. Having a well-defined goal made all the difference; Copilot handled the boilerplate while I focused on the logic.

### Playing with GitHub Pages and Actions

Part of the motivation here was exploring what you can automate and host for free using GitHub's tooling. GitHub Actions runs the daily feed updates on a schedule—no server to manage, no cron job to babysit. GitHub Pages hosts the RSS feed itself as a static file. For proof-of-concept work like this, it's a fantastic setup: zero hosting costs, minimal maintenance, and everything lives in the repo.

If you've been curious about what's possible with Actions and Pages beyond static sites, this kind of project is a great way to experiment.

### Important Notes

This is an **unofficial, community-created** project—I'm not affiliated with Digg. The tool doesn't create or host any audio content; it simply wraps publicly available audio files into an RSS format. All the actual AI-generated content is produced and hosted by Digg.

At the end of the day it was just a low stakes way to play with copilot and scratch my own itch.