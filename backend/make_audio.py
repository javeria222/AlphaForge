import asyncio, os, tempfile
import edge_tts

VOICE_A = "en-US-JennyNeural"
VOICE_B = "en-US-GuyNeural"

MEETINGS = {
    "meeting_1": [  # Kickoff - Architecture Planning
        ("A", "Welcome everyone. Today we need to choose a database for the project."),
        ("B", "Our data is structured. Meetings own segments, and segments belong to meetings."),
        ("A", "That points to a relational database. I think we should go with PostgreSQL for this."),
        ("B", "I agree. PostgreSQL gives us strong consistency and great tooling."),
        ("A", "Good. Next topic is deployment. Let's do Docker so every environment is consistent."),
        ("B", "Agreed. Docker keeps our setup simple."),
        ("A", "Great. We will review the frontend design next week."),
    ],
    "meeting_2": [  # Backend Sync - Database Discussion
        ("A", "Let's revisit the database decision from last week."),
        ("B", "I have been prototyping, and our transcript data is loosely structured and keeps changing shape."),
        ("A", "In that case, let's switch from PostgreSQL to MongoDB."),
        ("B", "Agreed. MongoDB gives us more flexibility here."),
        ("A", "Okay, the decision is MongoDB. Any concerns about deployment?"),
        ("B", "None. We are still using Docker."),
        ("A", "Great. We will keep Docker for deployment."),
    ],
    "meeting_3": [  # Final Review
        ("A", "Before the demo, we need to lock the database choice."),
        ("B", "I tested MongoDB, and similarity search across meetings was much harder than expected."),
        ("A", "Also, our data is relational after all. Meetings own segments."),
        ("B", "So I suggest we change back from MongoDB to PostgreSQL."),
        ("A", "I agree. The final decision is PostgreSQL."),
        ("B", "Confirmed. Deployment stays on Docker."),
        ("A", "Perfect. Let's finish the demo preparation."),
    ],
}

async def build(meeting_id, lines):
    out_path = os.path.join("data", "audio", f"{meeting_id}.mp3")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp, open(out_path, "wb") as out:
        for i, (speaker, text) in enumerate(lines):
            part = os.path.join(tmp, f"{i}.mp3")
            voice = VOICE_A if speaker == "A" else VOICE_B
            await edge_tts.Communicate(text, voice).save(part)
            with open(part, "rb") as f:
                out.write(f.read())
    print(f"wrote {out_path}")

async def main():
    for meeting_id, lines in MEETINGS.items():
        await build(meeting_id, lines)

asyncio.run(main())