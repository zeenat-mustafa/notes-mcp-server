import json
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-manager")

# --- Simple storage: one JSON file next to this script ---
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_data.json")


def load_notes() -> list[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_notes(notes: list[dict]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def next_id(notes: list[dict]) -> int:
    if not notes:
        return 1
    return max(note["id"] for note in notes) + 1


@mcp.tool()
def create_note(title: str, body: str) -> str:
    """Create a new note with a title and a body of text.

    Args:
        title: A short title for the note.
        body: The main text content of the note.
    """
    if not title.strip():
        return "Error: title cannot be empty."
    if not body.strip():
        return "Error: body cannot be empty."

    notes = load_notes()
    note = {"id": next_id(notes), "title": title.strip(), "body": body.strip()}
    notes.append(note)
    save_notes(notes)

    return f"Created note #{note['id']}: \"{note['title']}\""

@mcp.tool()
def list_notes() -> str:
    """List all notes, showing their id and title."""
    notes = load_notes()

    if not notes:
        return "No notes yet."

    lines = [f"#{note['id']}: {note['title']}" for note in notes]
    return "\n".join(lines)

@mcp.tool()
def get_note(note_id: int) -> str:
    """Get the full title and body of a single note by its id.

    Args:
        note_id: The id number of the note to retrieve.
    """
    notes = load_notes()

    for note in notes:
        if note["id"] == note_id:
            return f"#{note['id']}: {note['title']}\n\n{note['body']}"

    return f"Error: no note found with id {note_id}."

@mcp.tool()
def search_notes(query: str) -> str:
    """Search notes by keyword, matching against title or body.

    Args:
        query: The word or phrase to search for.
    """
    if not query.strip():
        return "Error: search query cannot be empty."

    notes = load_notes()
    query_lower = query.strip().lower()

    matches = [
        note for note in notes
        if query_lower in note["title"].lower() or query_lower in note["body"].lower()
    ]

    if not matches:
        return f"No notes found matching '{query}'."

    lines = [f"#{note['id']}: {note['title']}" for note in matches]
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run(transport="stdio")