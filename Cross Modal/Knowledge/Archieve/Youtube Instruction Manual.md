
YouTube’s **Custom Feeds** feature lets you describe the videos you want in natural language, then creates a dedicated, automatically refreshed recommendation feed on your Home page. The best instruction is not a list of keywords—it is a short viewing brief: *what you want, when/why you’ll watch it, what format to prefer, and what to avoid.* [blog](https://blog.youtube/news-and-events/made-on-youtube-viewer-custom-feeds-shopping-tools/)

## What YouTube officially supports

YouTube’s own examples frame Custom Feeds around a **mood, routine, or interest**, such as “Witty podcasts for my daily 30-minute commute,” “Evening wind down with long documentaries,” and “Help me discover new DIY creators.” You can save multiple feeds and they refresh with fresh recommendations. [blog](https://blog.youtube/news-and-events/made-on-youtube-viewer-custom-feeds-shopping-tools/)

The rollout situation is still evolving:

- YouTube’s earlier Help documentation describes the experimental version as English-only for signed-in U.S. users, with watch and search history enabled; it initially allowed one feed, and inactive prompts could expire after 30 days. [support.google](https://support.google.com/youtube/answer/17081258?hl=en)
- YouTube’s newer September announcement says multiple saved Custom Feeds are coming to U.S. users on web, mobile, and TV. An official experiment notice says some users can keep up to eight active feeds. [blog](https://blog.youtube/news-and-events/made-on-youtube-viewer-custom-feeds-shopping-tools/)
- If you are outside the U.S.—including Bangladesh or the Netherlands—you may not see it yet, because the official rollout announcements still describe U.S. availability. [blog](https://blog.youtube/news-and-events/made-on-youtube-viewer-custom-feeds-shopping-tools/)

## What to include in an instruction

Use these six elements, in roughly this order:


| Element         | What to state                                  | Example                                                                     |
| ----------------- | ------------------------------------------------ | ----------------------------------------------------------------------------- |
| Viewing purpose | What you are trying to accomplish or your mood | “Help me study for my AI thesis”                                          |
| Main topics     | Specific subjects, subfields, or problems      | “multimodal agents, RAG evaluation, open-weight LLMs”                     |
| Video format    | The types of videos you want                   | “technical lectures, conference talks, code walkthroughs”                 |
| Time/length     | Your available time or preferred duration      | “20–45 minutes” or “long-form only”                                    |
| Quality signals | What makes a recommendation useful             | “prioritize primary sources, papers, maintainers, and reproducible demos” |
| Exclusions      | Content you do not want                        | “exclude hype, reaction videos, beginner explainers, and Shorts”          |

A strong instruction is **specific enough to define a selection rule**, but not so narrow that YouTube has almost no eligible videos to recommend. For example, “AI videos” is overly broad; “new papers only from one niche, in Bangla, under eight minutes, with full code” may be too restrictive.

## How to write it well

### 1. Write a feed objective, not a search query

This feature is meant to create an ongoing recommendation space, not return one exact video. Describe the kind of feed you want to revisit.

- Weak: `AI, Python, coding`
- Better: `A practical feed for improving my Python AI engineering skills through recent tutorials and implementation walkthroughs.`

The second version tells YouTube both the topic and the intended use.

### 2. Name your priorities explicitly

If you care about recency, depth, source quality, language, creator discovery, or a balance between familiar and new channels, say so. YouTube specifically positions Custom Feeds as a way to explore interests and discover creators, not merely duplicate your ordinary Home recommendations. [blog](https://blog.youtube/news-and-events/made-on-youtube-viewer-custom-feeds-shopping-tools/)

Useful priority phrases:

- “Prioritize videos published in the last 90 days.”
- “Prefer technical depth over broad introductions.”
- “Favor official channels, researchers, conference talks, and project maintainers.”
- “Include smaller credible creators and channels I have not watched before.”
- “Prefer English audio with clear visuals and captions.”
- “Choose videos that include code, benchmarks, papers, or demos.”

### 3. State exclusions clearly

Negative constraints are valuable when your normal recommendations are cluttered with formats you do not want. Say “exclude” or “avoid” directly.

Examples:

- “Exclude Shorts, reaction videos, AI-news summaries, and clickbait.”
- “Avoid low-effort tool lists and unverified ‘make money with AI’ content.”
- “Do not include gameplay, celebrity news, or unrelated consumer-tech reviews.”
- “Avoid content aimed at absolute beginners.”

Do not assume the feed will be perfectly filtered on the first attempt. Edit the instruction after seeing results; YouTube says you can change the prompt to generate a new feed, and refresh it for new recommendations. [support.google](https://support.google.com/youtube/answer/17081258?hl=en)

### 4. Use normal sentences

YouTube describes the feature as using **conversational prompts**. Full, plain-English instructions make it easier to communicate relationships between constraints than comma-separated keywords. [blog](https://blog.youtube/news-and-events/innovation-youtube-era-made-on-viewers-creators/)

- Less clear: `agents RAG videos no Shorts research coding`
- Clearer: `Show practical, research-oriented videos about AI agents and RAG systems, especially implementation walkthroughs and evaluations. Avoid Shorts, general AI news, and surface-level tool reviews.`

### 5. Keep one feed for one job

Because Custom Feeds can be saved separately, avoid mixing unrelated purposes in a single instruction—for example, thesis research, Formula 1 highlights, and cooking tutorials. Create distinct feeds with a stable reason for returning to each one. The newest official announcement specifically presents the feature as multiple dedicated tabs for different moods, routines, and interests. [blog](https://blog.youtube/news-and-events/made-on-youtube-viewer-custom-feeds-shopping-tools/)

## A reusable prompt template

Copy and adapt this:

> Create a feed for **[purpose or situation]**. Show **[topics]** in the form of **[formats]**, preferably **[duration]**. Prioritize **[recency, depth, source quality, language, creator type, novelty]**. Exclude **[formats/topics/quality issues]**.

A more detailed version:

> I want a dedicated YouTube feed for **[goal]**. Focus on **[specific subjects]**. Prefer **[video types]** that are **[length / pace / language]**. Prioritize **[credible sources, recent uploads, practical demonstrations, new creators, etc.]**. Avoid **[unwanted formats, topics, or styles]**.

## Ready-to-use examples for you

### AI/ML thesis research

> Create a research-focused feed for my undergraduate AI/ML thesis preparation. Show recent technical talks, paper explainers, conference presentations, reproducible demos, and implementation walkthroughs on multimodal AI, LLM agents, RAG evaluation, and open-weight models. Prefer English videos between 15 and 60 minutes from researchers, universities, conferences, and project maintainers. Prioritize uploads from the last 12 months and include new credible creators. Exclude Shorts, generic AI news, reaction videos, “top tools” lists, and hype without technical evidence.

### Practical AI engineering

> Build a feed for becoming a stronger Python AI engineer. Focus on FastAPI, model deployment, RAG applications, agent workflows, vector databases, evaluation, and clean production-oriented code. Prefer hands-on coding tutorials and architecture walkthroughs that include GitHub repositories or working examples. Favor videos between 20 and 50 minutes. Exclude beginner Python lessons, Shorts, vague productivity content, and unverified no-code AI claims.

### Open-source AI discovery

> Help me discover trustworthy open-source AI projects and developer walkthroughs. Show videos about new open-weight models, local inference, model benchmarking, multimodal tools, AI coding assistants, and self-hosted workflows on Windows. Prioritize maintainers, official project channels, detailed demos, and videos that explain hardware requirements, licensing, limitations, and setup steps. Avoid sponsored tool roundups, clickbait comparisons, and content that only repeats press releases.

### Focused study sessions

> Create a focused evening study feed with calm, technical long-form videos about machine learning, deep learning, and software engineering. Prefer lectures, conference talks, and in-depth tutorials lasting 30 to 90 minutes. Prioritize clear English explanations, diagrams, code demonstrations, and minimal interruptions. Exclude Shorts, reaction content, distracting news, motivational videos, and entertainment content.

## Practical refinement method

1. Start with one clear purpose and 3–5 constraints.
2. Inspect the first set of recommendations.
3. Identify the failure type: too broad, too beginner-focused, too old, too short, too commercial, or off-topic.
4. Add one direct corrective sentence rather than rewriting everything.
5. Refresh or edit the feed prompt. YouTube says prompt edits create a new recommendation space, and refresh generates another set of recommendations based on that prompt. [support.google](https://support.google.com/youtube/answer/17081258?hl=en)

For example:

- Initial: “Technical videos about AI agents and RAG.”
- If results are too superficial: “Prefer technical implementation and evaluation content for intermediate developers; exclude general AI news and tool-list videos.”
- If results are too long: “Keep most videos between 15 and 35 minutes.”
- If results repeat channels: “Include more credible creators and channels I have not watched before.”

## Limits and privacy

Custom Feed instructions must comply with YouTube’s Community Guidelines.  Also, YouTube requires search and watch history for the feature in the documented rollout, and videos you watch from the custom feed can affect your broader watch history and ordinary Home recommendations. [support.google](https://support.google.com/youtube/answer/17081258?hl=en)


Gemini appears to act as a **natural-language interpreter and recommendation-layer controller**, not as a system that independently crawls YouTube and manually picks videos. It interprets your instruction—such as topic, mood, duration, and exclusions—then YouTube’s recommendation system builds and ranks a dedicated stream of existing videos that it considers relevant to that request. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)

## The practical pipeline

Conceptually, the process likely works like this:

\[
\text{Your prompt} + \text{YouTube history/context} \rightarrow \text{prompt intent} \rightarrow \text{candidate videos} \rightarrow \text{ranking} \rightarrow \text{Custom Feed}
\]

### 1. Gemini interprets the prompt

You type a natural-language description such as:

> “Help me unwind after work with guided meditations under 10 minutes.”

YouTube’s official experiment page says that a prompt like this “instantly” generates a personalized feed. Gemini’s role is to translate vague human language—*unwind*, *after work*, *under 10 minutes*—into structured recommendation preferences. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)

In effect, it may infer constraints like:


| Your wording              | Likely interpretation                                                         |
| --------------------------- | ------------------------------------------------------------------------------- |
| “Unwind after work”     | Relaxing, low-intensity content; possibly meditation, calm music, mindfulness |
| “Guided meditations”    | Video topic/format preference                                                 |
| “Under 10 minutes”      | Duration filter or strong ranking preference                                  |
| “For beginners”         | Introductory explanations and less advanced material                          |
| “Avoid hype”            | Down-rank sensational, clickbait-like, or vague videos                        |
| “Discover new creators” | Increase diversity and reduce reliance on channels you already watch          |

YouTube has not publicly disclosed the exact Gemini model, embedding system, ranking formula, or weighting applied to each instruction. So this is the functional behavior YouTube describes, not a confirmed engineering architecture.

## How YouTube chooses videos

After interpreting the request, the platform likely retrieves candidate videos from YouTube’s catalog and ranks them using several signals:

- **Semantic relevance:** Does the video’s title, metadata, spoken content, captions/transcript, channel identity, and viewer-engagement patterns align with the prompt?
- **Your prompt constraints:** Topic, desired format, mood, runtime, language, and stated exclusions.
- **Your existing personalization:** YouTube says Custom Feeds require watch history to be turned on in the current experiment. Your watch and search history normally helps YouTube provide better recommendations. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)
- **Standard recommendation-quality and safety systems:** YouTube still determines what it believes best matches the request and how results are ordered; your instruction guides the system but does not override platform policies or turn the feed into an exact search filter. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)

So if you write:

> “Recent technical walkthroughs for intermediate Python developers on local LLM inference and RAG evaluation; prefer open-source projects and avoid Shorts or generic AI news.”

Gemini can convert that into something similar to:

- Topics: local LLMs, inference, RAG, evaluation
- Skill level: intermediate
- Format: technical walkthroughs
- Recency: recent
- Source/content preference: open source
- Negative preferences: Shorts and general news
- Viewer context: your normal YouTube history and behavior

Then the recommendation system finds potentially relevant videos and orders them based on fit and its usual ranking signals.

## It is a separate feed, not a separate identity

Custom Feeds are pinned near the top of Home and can be edited whenever you want. Changing the instruction causes YouTube to generate a recommendation space based on the new prompt; the experiment supports multiple saved feeds, with up to eight active feeds for eligible participants. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)

But the feed is **not fully isolated** from your normal account recommendations:

- YouTube’s privacy policy says watch and search history are used to personalize the experience and provide better recommendations. [youtube](https://www.youtube.com/t/privacy)
- Since the Custom Feed experiment requires watch history to be enabled, your established viewing patterns remain an input. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)
- In practical terms, videos you watch, skip, like, save, or ignore in that feed can become behavioral signals that influence future recommendations, potentially including your ordinary Home feed.

This means a Custom Feed is better understood as a **prompt-guided lens on YouTube’s existing recommender system**, rather than a clean, independent playlist or a fully user-programmable algorithm.

## Why instructions affect results

Gemini makes broad ideas usable as recommendation intent. Traditional YouTube topic chips might let you choose “Machine learning”; a Custom Feed lets you express a fuller rule such as:

> “Technical, evidence-based videos on multimodal AI and agent evaluation for an undergraduate thesis. Prefer university lectures, conference talks, research-paper explainers, and reproducible code demos from the last year. Avoid Shorts, AI news roundups, beginner tutorials, and exaggerated tool reviews.”

That gives the system substantially more context about:

- **The subject** — multimodal AI, agents, evaluation
- **The goal** — thesis research
- **The standard of quality** — evidence-based, research and reproducible code
- **The source types** — universities, conferences, researchers, maintainers
- **The exclusions** — Shorts, news, beginner material, hype

The result should be more focused than your general Home feed, although YouTube does not guarantee that every recommendation will satisfy every line of the prompt.

## Key limitation

Gemini does not appear to replace YouTube’s recommendation algorithm. It supplies a natural-language control layer: it understands what you want, but YouTube’s systems still retrieve, filter, apply policy/safety rules, and rank the available videos. The official documentation describes Custom Feeds as dedicated discovery spaces for one or more topics, created by prompting and adjustable by editing that prompt—not as direct access to manually set the ranking algorithm. [support.google](https://support.google.com/youtube/thread/18138167/youtube-test-features-and-experiments?hl=en)
